"""Evaluasi AI per posisi close BARU saja (hemat limit free 50/hari)."""
import datetime, json, time, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

def log(*a):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), *a, flush=True)

def call_or(model, key, prompt):
    import urllib.request
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 1000, "temperature": 0.3}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json",
                                          "HTTP-Referer": "http://127.0.0.1:2026/", "X-Title": "JurnalMT5"})
    r = json.load(urllib.request.urlopen(req, timeout=60))
    if not r.get("choices"):
        raise RuntimeError(str(r.get("error", r))[:150])
    return (r["choices"][0]["message"].get("content") or "").strip()

def fmt_tape(t):
    wib = datetime.timezone(datetime.timedelta(hours=7))
    lines = []
    for i, (ts, (o, h, l, c)) in enumerate(zip(t["t"], t["c"])):
        mark = "E" if i == t.get("e") else ("X" if i == t.get("x") else "")
        hm = datetime.datetime.fromtimestamp(ts, wib).strftime("%H:%M")
        lines.append(f"{hm} {o} {h} {l} {c} {mark}".rstrip())
    return "\n".join(lines)

def build_prompt(r):
    arah = 'SL' if 'SL' in r['hasil'] else 'TP'
    op, cp, sl, tp = (round(r[k], 3) for k in ("open_price", "close_price", "sl", "tp"))
    p = (f"Kamu analis teknikal trading. Bahasa Indonesia, SATU paragraf saja, maks 80 kata, "
         f"tanpa markdown/bold, tanpa kalimat pembuka/penutup.\n"
         f"Posisi {r['symbol']} {r['type']} {r['volume']} lot, open {op} close {cp}, "
         f"SL {sl} TP {tp}, net {r['net']} USD, durasi {r['durasi_mnt']} mnt, hasil {r['hasil']}.\n")
    if r.get("tape"):
        p += (f"Tape M5 {r['symbol']} (O H L C per 5 mnt WIB, E=entry X=exit):\n{fmt_tape(r['tape'])}\n"
              f"Analisis dari tape: struktur gerak harga, posisi entry terhadap swing/high-low terlihat, "
              f"kualitas SL/TP terhadap struktur itu. DILARANG menyebut nama pola candle.\n")
    p += (f"Dalam paragraf itu sebut: kenapa hit {arah}, apa yang benar dari setup ini, "
          f"satu perbaikan konkret untuk trade berikutnya.")
    return p

def main():
    cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    key = (BASE / "private" / "openrouter_key.txt").read_text(encoding="utf-8").strip()
    closed = json.loads((DATA / "closed.json").read_text(encoding="utf-8")) if (DATA / "closed.json").exists() else []
    ai_path = DATA / "ai.json"
    ai = json.loads(ai_path.read_text(encoding="utf-8")) if ai_path.exists() else {}
    todo = [r for r in closed if r["position_id"] not in ai][:int(cfg.get("max_eval_per_run", 10))]
    if not todo:
        log("SKIP nothing-new")
        return 0
    for r in todo:
        prompt = build_prompt(r)
        err = None
        for model in (cfg["model_primary"], cfg.get("model_fallback")):
            if not model:
                continue
            try:
                txt = call_or(model, key, prompt)
                if not txt:
                    err = "empty"; continue
                ai[r["position_id"]] = {"evaluasi": txt, "model": model,
                                        "updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "hasil": r["hasil"]}
                log(f"OK {r['position_id']} via {model}")
                err = None
                break
            except Exception as e:
                err = str(e)[:150]
                if "429" in err:
                    time.sleep(15)
                continue
        if err:
            log(f"FAIL {r['position_id']}: {err}")
        ai_path.write_text(json.dumps(ai, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(3)
    return 0

if __name__ == "__main__":
    sys.exit(main())
