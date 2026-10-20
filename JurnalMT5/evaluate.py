"""Evaluasi AI AGREGAT per 1 jam + memori pola jangka panjang (hemat token).

Arsip & statistik dihitung lokal di Python (biaya token 0). Satu panggilan LLM
per jam menghasilkan LAPORAN bahasa awam + pembaruan MEMORI jangka panjang.
Output: data/ai_report.json, data/ai_memory.json, data/history.json.
"""
import datetime, json, time, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
WIB = datetime.timezone(datetime.timedelta(hours=7))

def log(*a):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), *a, flush=True)

def load_json(p):
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None

def call_llm(base, model, key, prompt, effort=None, max_tokens=2500):
    import urllib.request
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}],
               "max_tokens": max_tokens, "temperature": 0.3}
    if effort:
        payload["reasoning_effort"] = effort
    req = urllib.request.Request(base, data=json.dumps(payload).encode(),
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json",
                                          "User-Agent": "JurnalMT5/1.0"})
    r = json.load(urllib.request.urlopen(req, timeout=120))
    if not r.get("choices"):
        raise RuntimeError(str(r.get("error", r))[:150])
    return (r["choices"][0]["message"].get("content") or "").strip()

# ---------- bantu ----------
_SP = {"\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-", "\u2212": "-",
       "\u202f": " ", "\u00a0": " ", "\u2009": " ", "\u2007": " ", "\u2060": "", "\u200b": ""}

def clean(txt):
    for k, v in _SP.items():
        txt = txt.replace(k, v)
    return txt

def rnd(x, n=2):
    return round(float(x), n)

def dt_wib(ts):
    return datetime.datetime.fromtimestamp(ts, WIB)

def winrate(rows):
    return rnd(sum(1 for r in rows if r["net"] > 0) / len(rows) * 100) if rows else 0

def pfactor(rows):
    gp = sum(r["net"] for r in rows if r["net"] > 0)
    gl = -sum(r["net"] for r in rows if r["net"] < 0)
    if gl == 0:
        return 99.0 if gp > 0 else 0.0
    return rnd(gp / gl)

def rmult(r):
    if not r.get("sl") or not r.get("open_price"):
        return None
    risk = abs(r["open_price"] - r["sl"])
    if risk <= 0:
        return None
    move = (r["close_price"] - r["open_price"]) if r["type"] == "BUY" else (r["open_price"] - r["close_price"])
    return move / risk

def excursion(r):
    """(MFE_R, MAE_R) dari tape; None bila tidak tersedia."""
    t = r.get("tape")
    if not t or not r.get("sl"):
        return None
    try:
        e, x = t["e"], t["x"]
        cs = t["c"][e:x + 1]
        hi = max(c[1] for c in cs)
        lo = min(c[2] for c in cs)
        op = r["open_price"]
        risk = abs(op - r["sl"])
        if risk <= 0:
            return None
        if r["type"] == "BUY":
            mfe, mae = hi - op, op - lo
        else:
            mfe, mae = op - lo, hi - op
        return (mfe / risk, mae / risk)
    except Exception:
        return None

def get_exc(r):
    v = r.get("exc")
    if v:
        return (v[0], v[1])
    return excursion(r)

def slim(r):
    """Simpan record arsip tanpa tape (berat); simpan exc (MFE/MAE-R) yang ringan."""
    o = {k: v for k, v in r.items() if k != "tape"}
    if not o.get("exc"):
        e = excursion(r)
        if e:
            o["exc"] = [rnd(e[0]), rnd(e[1])]
    return o

def hour_wib(r):
    return dt_wib(r["open_time"]).hour

def session_wib(h):
    if 6 <= h < 11:
        return "Pagi 06-11"
    if 11 <= h < 16:
        return "Siang 11-16"
    if 16 <= h < 21:
        return "Sore 16-21"
    return "Malam 21-06"

def dur_bucket(mnt):
    if mnt < 15:
        return "a) <15m"
    if mnt < 60:
        return "b) 15-60m"
    if mnt < 240:
        return "c) 1-4j"
    return "d) >4j"

DOW = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# ---------- arsip kumulatif ----------
def merge_history(closed):
    """Gabung trade close ke arsip kumulatif (dedup by position_id). Kembalikan semua record."""
    hp = DATA / "history.json"
    hist = load_json(hp) or {}
    for r in closed:
        hist[str(r["position_id"])] = slim(r)
    hp.write_text(json.dumps(hist, ensure_ascii=False), encoding="utf-8")
    return list(hist.values())

# ---------- stat-pack ----------
def dim_line(rows):
    net = sum(r["net"] for r in rows)
    return f"{len(rows)} trade, menang {winrate(rows)}%, net {rnd(net)} USD, untung:rugi {pfactor(rows)}"

def group_lines(rows, keyfn, order=None):
    g = {}
    for r in rows:
        g.setdefault(keyfn(r), []).append(r)
    keys = order or sorted(g.keys(), key=lambda k: -sum(r["net"] for r in g[k]))
    return " | ".join(f"{k}: {dim_line(g[k])}" for k in keys if k in g)

def max_drawdown(rows):
    run = peak = dd = 0.0
    for r in sorted(rows, key=lambda r: r["close_time"]):
        run += r["net"]
        peak = max(peak, run)
        dd = min(dd, run - peak)
    return dd

def streaks(rows):
    bw = bl = cw = cl = 0
    for r in sorted(rows, key=lambda r: r["close_time"]):
        if r["net"] > 0:
            cw += 1; cl = 0
        else:
            cl += 1; cw = 0
        bw, bl = max(bw, cw), max(bl, cl)
    return bw, bl

def build_pack(rows, cfg):
    rows = sorted(rows, key=lambda r: r["close_time"])
    n = len(rows)
    wins = [r for r in rows if r["net"] > 0]
    loss = [r for r in rows if r["net"] < 0]
    net = sum(r["net"] for r in rows)
    rs = [x for x in (rmult(r) for r in rows) if x is not None]
    dd = max_drawdown(rows)
    bw, bl = streaks(rows)

    conc = []
    for p in (1, 5, 10):
        k = max(1, round(n * p / 100))
        rest = sorted(rows, key=lambda r: r["net"], reverse=True)[k:]
        conc.append(f"tanpa top{p}% = {rnd(sum(r['net'] for r in rest))}")

    def avg_exc(lst):
        vals = [get_exc(r) for r in lst]
        vals = [v for v in vals if v]
        if not vals:
            return None
        return (rnd(sum(v[0] for v in vals) / len(vals)), rnd(sum(v[1] for v in vals) / len(vals)))

    ew, el = avg_exc(wins), avg_exc(loss)
    exc_txt = ""
    if ew or el:
        parts = []
        if ew:
            parts.append(f"trade menang MFE {ew[0]}R / MAE {ew[1]}R")
        if el:
            parts.append(f"trade kalah MFE {el[0]}R / MAE {el[1]}R")
        exc_txt = " | ".join(parts)

    losses_ts = [r["close_time"] for r in rows if r["net"] < 0]
    rev = [r for r in rows if any(0 <= r["open_time"] - t <= 900 for t in losses_ts)]

    aw = [r["durasi_mnt"] for r in wins]
    al = [r["durasi_mnt"] for r in loss]
    avg_dw = rnd(sum(aw) / len(aw), 0) if aw else 0
    avg_dl = rnd(sum(al) / len(al), 0) if al else 0

    first = dt_wib(min(r["open_time"] for r in rows)).strftime("%d/%m/%Y")
    last = dt_wib(max(r["close_time"] for r in rows)).strftime("%d/%m/%Y")

    L = []
    L.append(f"# DATA ALL-TIME: {n} transaksi ({first} s/d {last})")
    L.append(
        f"# RINGKASAN: menang {len(wins)} ({winrate(rows)}%), kalah {len(loss)}, net {rnd(net)} USD, "
        f"rata2 per transaksi {rnd(net / n)} USD, banding untung:rugi {pfactor(rows)}, "
        f"rata2 menang {rnd(sum(r['net'] for r in wins) / len(wins)) if wins else 0} USD, "
        f"rata2 kalah {rnd(sum(r['net'] for r in loss) / len(loss)) if loss else 0} USD, "
        f"drawdown terburuk {rnd(dd)} USD, beruntun menang {bw}x kalah {bl}x, "
        f"rata2 durasi menang {avg_dw} mnt vs kalah {avg_dl} mnt, "
        f"rata2 R {rnd(sum(rs) / len(rs)) if rs else 0} (dari {len(rs)} trade ber-SL)"
    )
    cut7 = (datetime.datetime.now() - datetime.timedelta(days=7)).timestamp()
    r7 = [r for r in rows if r["close_time"] >= cut7]
    if r7:
        L.append(f"# 7 HARI TERAKHIR: {dim_line(r7)}")
    L.append(f"# KONSENTRASI: {' | '.join(conc)}")
    if exc_txt:
        L.append(f"# EXCURSION: {exc_txt}")
    L.append(f"# PER JAM buka (WIB): {group_lines(rows, hour_wib, order=sorted({hour_wib(r) for r in rows}))}")
    L.append(f"# PER HARI: {group_lines(rows, lambda r: DOW[dt_wib(r['open_time']).weekday()], order=DOW)}")
    L.append(f"# PER PAIR: {group_lines(rows, lambda r: r['symbol'])}")
    L.append(f"# PER SISI: {group_lines(rows, lambda r: r['type'], order=['BUY', 'SELL'])}")
    L.append(f"# PER DURASI: {group_lines(rows, lambda r: dur_bucket(r['durasi_mnt']))}")
    L.append(f"# PER SESI: {group_lines(rows, lambda r: session_wib(hour_wib(r)), order=['Pagi 06-11', 'Siang 11-16', 'Sore 16-21', 'Malam 21-06'])}")
    L.append(f"# PER HASIL: {group_lines(rows, lambda r: r['hasil'])}")
    top_w = sorted(rows, key=lambda r: r["net"], reverse=True)[:3]
    top_l = sorted(rows, key=lambda r: r["net"])[:3]
    fmt = lambda r: f"{dt_wib(r['open_time']).strftime('%d/%m %H:%M')} {r['symbol']} {r['type']} {rnd(r['net'])} USD ({r['durasi_mnt']}m, {r['hasil']})"
    L.append("# TOP MENANG: " + " | ".join(fmt(r) for r in top_w))
    L.append("# TOP RUGI: " + " | ".join(fmt(r) for r in top_l))
    L.append(f"# REVENGE (buka <=15m setelah loss sebelumnya): {len(rev)} trade, net {rnd(sum(r['net'] for r in rev))} USD")
    return "\n".join(L)

def build_prompt(pack, mem_text, mem_max):
    mem_block = mem_text.strip() if mem_text and mem_text.strip() else "(belum ada memori — ini sesi pertama)"
    return (
        "Kamu coach trading yang menjelaskan ke ORANG AWAM dan mengingat pola jangka panjang. "
        "Bahasa Indonesia sangat sederhana, kalimat pendek, tanpa istilah teknis (kalau terpaksa pakai, "
        "jelaskan 1 kalimat dalam tanda kurung). Angka dibulatkan, pakai USD dan jam (contoh 14:00 WIB) atau nama hari. "
        "Pakai karakter biasa saja ('-', titik, koma, kurung, persen, ':'), JANGAN karakter aneh, JANGAN tabel.\n\n"
        "Kerjakan 2 hal: (A) LAPORAN untuk trader, (B) perbarui MEMORI pola jangka panjang.\n\n"
        "Balas PERSIS dengan format ini, tanpa teks pembuka/penutup lain:\n"
        "===LAPORAN===\n"
        "**RINGKASAN** (2-3 kalimat: jumlah transaksi, menang/kalah, untung atau rugi berapa USD)\n"
        "**YANG SUDAH BAGUS** (3-5 bullet '-', sebut jam/hari/pair + angkanya)\n"
        "**YANG BIKIN RUGI** (3-5 bullet, sebut jumlah transaksinya)\n"
        "**SARAN PERBAIKAN** (3-5 bullet perintah praktis)\n"
        "===MEMORI===\n"
        f"(maksimal {mem_max} kata; baris 'POLA:' lalu bullet '- [keyakinan: tinggi/sedang/rendah] pola - bukti: N transaksi, net X USD', "
        "lalu baris 'TREN:' 1-2 kalimat, lalu baris 'CATATAN:' 1 kalimat. "
        "Gabungkan MEMORI SEBELUMNYA dengan data baru: perkuat pola yang konsisten, pensiunkan yang tak berlaku, "
        "tambah pola baru bila bukti cukup. Ini yang membuatmu terus memahami pola sampai kapan pun.)\n"
        "Hanya 4 judul bagian LAPORAN yang boleh dibold. JANGAN bold kata/angka lain.\n"
        "LAPORAN maksimal ~250 kata. WAJIB menulis KEDUA blok (===LAPORAN=== dan ===MEMORI===) sampai selesai.\n"
        "Bila total transaksi < 20, ingatkan bahwa kesimpulan belum kuat.\n\n"
        f"MEMORI SEBELUMNYA:\n{mem_block}\n\n"
        f"DATA HASIL HITUNGAN (lokal, akurat):\n{pack}"
    )

def split_blocks(txt):
    rep, mem = txt, None
    if "===MEMORI===" in txt:
        a, b = txt.split("===MEMORI===", 1)
        rep, mem = a, b
    rep = rep.replace("===LAPORAN===", "").strip()
    mem = mem.strip() if mem else None
    return rep, mem

def main():
    cfg = load_json(BASE / "config.json") or {}
    key = (BASE / "private" / cfg.get("key_file", "groq_key.txt")).read_text(encoding="utf-8").strip()
    api_base = cfg.get("api_base", "https://api.groq.com/openai/v1/chat/completions")
    closed = load_json(DATA / "closed.json") or []
    if not closed:
        log("SKIP no-closed")
        return 0

    hist = merge_history(closed)

    rep_path, mem_path = DATA / "ai_report.json", DATA / "ai_memory.json"
    rep = load_json(rep_path) or {}
    mem = load_json(mem_path) or {}
    now = datetime.datetime.now()
    interval = int(cfg.get("eval_interval_minutes", 60))

    last = None
    if rep.get("updated"):
        try:
            last = datetime.datetime.strptime(rep["updated"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            last = None
    if last and (now - last).total_seconds() < interval * 60:
        log(f"SKIP interval ({(now - last).total_seconds() / 60:.0f}/{interval} mnt)")
        return 0

    max_close = max(r["close_time"] for r in hist)
    if cfg.get("eval_skip_if_unchanged", True) and rep.get("last_close_time") and max_close <= rep["last_close_time"]:
        log("SKIP nothing-new")
        return 0

    pack = build_pack(hist, cfg)
    mem_max = int(cfg.get("memory_max_words", 200))
    prompt = build_prompt(pack, mem.get("text", ""), mem_max)
    max_tokens = int(cfg.get("max_tokens", 2500))
    err = None
    for model in (cfg.get("model_primary"), cfg.get("model_fallback")):
        if not model:
            continue
        try:
            txt = clean(call_llm(api_base, model, key, prompt, cfg.get("reasoning_effort"), max_tokens))
            if not txt:
                err = "empty"; continue
            if "===MEMORI===" not in txt:
                err = "no-memori-block"; continue
            rpt, newmem = split_blocks(txt)
            if not rpt or not newmem:
                err = "bad-blocks"; continue
            mem_text = (newmem or mem.get("text", "")).strip()
            if len(mem_text) > mem_max * 9:
                mem_text = mem_text[:mem_max * 9].rsplit("\n", 1)[0]
            ts = now.strftime("%Y-%m-%d %H:%M:%S")
            rep_path.write_text(json.dumps({"updated": ts, "model": model, "n_trades": len(hist),
                                            "last_close_time": max_close, "eval": rpt, "data": pack},
                                           ensure_ascii=False, indent=1), encoding="utf-8")
            if mem_text:
                mem_path.write_text(json.dumps({"updated": ts, "model": model, "trades_seen": len(hist),
                                                "text": mem_text}, ensure_ascii=False, indent=1), encoding="utf-8")
            log(f"OK report {len(hist)} trade, memori {len(mem_text)} char via {model}")
            return 0
        except Exception as e:
            err = str(e)[:150]
            if "429" in err:
                time.sleep(15)
            continue
    log("FAIL report: " + str(err))
    return 0

if __name__ == "__main__":
    sys.exit(main())
