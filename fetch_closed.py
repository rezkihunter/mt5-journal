"""Snapshot posisi close dari MT5 + gabung SL/TP. Dijalankan tiap 5 mnt via Scheduled Task."""
import datetime, json, sys, time
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
TERMINAL_PATH = r"C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe"

def log(*a):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), *a, flush=True)

def get_tape(mt5, symbol, t_open, t_close):
    """Tape M5 riil open-3j s/d close+15m, maks 48 candle + indeks entry/exit."""
    import datetime as dt
    try:
        frm = dt.datetime.fromtimestamp(t_open - 3 * 3600, dt.timezone.utc)
        to = dt.datetime.fromtimestamp(t_close + 15 * 60, dt.timezone.utc)
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, frm, to)
        if rates is None or len(rates) == 0:
            return None
        idx = range(len(rates))
        if len(rates) > 48:
            step = -(-len(rates) // 48)
            idx = range(0, len(rates), step)
        ts = [int(rates[i][0]) for i in idx]
        cs = [[round(float(rates[i][j]), 3) for j in (1, 2, 3, 4)] for i in idx]
        e = min(range(len(ts)), key=lambda i: abs(ts[i] - t_open))
        x = min(range(len(ts)), key=lambda i: abs(ts[i] - t_close))
        return {"tf": "M5", "t": ts, "c": cs, "e": e, "x": x}
    except Exception:
        return None

def init_mt5(mt5, cfg):
    cands = [{"path": cfg.get("terminal_path") or TERMINAL_PATH}, {}]
    last = None
    for _ in range(3):
        for kw in cands:
            try:
                if mt5.initialize(**kw):
                    return True
            except Exception as e:
                last = str(e)
                continue
            last = str(mt5.last_error())
            time.sleep(5)
    log("INIT_FAIL", last)
    return False

def save(name, obj):
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")

def main():
    import MetaTrader5 as mt5
    cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    if not init_mt5(mt5, cfg):
        return 1
    try:
        days = int(cfg.get("days_back", 120))
        now = datetime.datetime.now()
        frm = now - datetime.timedelta(days=days)
        to = now + datetime.timedelta(days=1)

        acc = mt5.account_info()
        save("account.json", acc._asdict() if acc else {})

        snap_path = DATA / "sl_snapshot.json"
        snap = json.loads(snap_path.read_text(encoding="utf-8")) if snap_path.exists() else {}

        opens = mt5.positions_get() or []
        open_list = []
        for p in opens:
            d = p._asdict()
            open_list.append(d)
            snap[str(d["ticket"])] = {"sl": d.get("sl", 0.0), "tp": d.get("tp", 0.0),
                                      "price_open": d.get("price_open"), "symbol": d.get("symbol"),
                                      "type": d.get("type"), "volume": d.get("volume"),
                                      "time": d.get("time"), "updated": now.strftime("%Y-%m-%d %H:%M:%S")}
        save("open.json", open_list)
        keep = {str(d.get("ticket")) for d in open_list}
        snap = {k: v for k, v in snap.items() if k in keep}
        snap_path.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")

        deals = mt5.history_deals_get(frm, to) or []
        groups = {}
        for x in deals:
            d = x._asdict()
            if d.get("position_id", 0) == 0:
                continue
            groups.setdefault(str(d["position_id"]), []).append(d)

        orders = mt5.history_orders_get(frm, to) or []
        osl = {}
        for x in orders:
            d = x._asdict()
            pid = str(d.get("position_id", 0))
            if (d.get("sl", 0.0) or d.get("tp", 0.0)) and pid not in osl:
                osl[pid] = {"sl": d.get("sl", 0.0), "tp": d.get("tp", 0.0)}

        closed = []
        for pid, ds in groups.items():
            ins = [d for d in ds if d.get("entry") == 0]
            outs = [d for d in ds if d.get("entry") == 1]
            if not outs:
                continue
            ins.sort(key=lambda d: d["time"])
            outs.sort(key=lambda d: d["time"])
            o, c = ins[0] if ins else outs[0], outs[-1]
            s = snap.get(pid, {})
            sl = s.get("sl", 0.0) or osl.get(pid, {}).get("sl", 0.0)
            tp = s.get("tp", 0.0) or osl.get(pid, {}).get("tp", 0.0)
            net = round(sum(d.get("profit", 0.0) + d.get("commission", 0.0) + d.get("swap", 0.0) + d.get("fee", 0.0) for d in ds), 2)
            is_buy = (o.get("type") == 0)
            cp, slv, tpv = c.get("price", 0.0), sl or 0.0, tp or 0.0
            if slv and ((is_buy and cp <= slv * 1.0005) or ((not is_buy) and cp >= slv * 0.9995)):
                hasil = "SL"
            elif tpv and ((is_buy and cp >= tpv * 0.9995) or ((not is_buy) and cp <= tpv * 1.0005)):
                hasil = "TP"
            elif net > 0:
                hasil = "TP/manual-profit"
            elif net < 0:
                hasil = "SL/manual-loss"
            else:
                hasil = "flat"
            closed.append({"position_id": pid, "symbol": o.get("symbol"), "type": "BUY" if is_buy else "SELL",
                           "volume": o.get("volume"), "open_price": o.get("price"), "open_time": o.get("time"),
                           "close_price": c.get("price"), "close_time": c.get("time"),
                           "sl": slv, "tp": tpv, "profit": round(c.get("profit", 0.0), 2), "net": net,
                           "hasil": hasil, "durasi_mnt": round((c.get("time", 0) - o.get("time", 0)) / 60, 1)})
        closed.sort(key=lambda r: r["close_time"], reverse=True)
        tape_path = DATA / "tapes.json"
        tapes = json.loads(tape_path.read_text(encoding="utf-8")) if tape_path.exists() else {}
        ids = {r["position_id"] for r in closed}
        tapes = {k: v for k, v in tapes.items() if k in ids}
        for r in closed:
            tp = tapes.get(r["position_id"])
            if tp is None:
                tp = get_tape(mt5, r["symbol"], r["open_time"], r["close_time"])
                if tp:
                    tapes[r["position_id"]] = tp
                else:
                    log("TAPE_MISS", r["position_id"], r["symbol"])
            if tp:
                r["tape"] = tp
        tape_path.write_text(json.dumps(tapes, ensure_ascii=False), encoding="utf-8")
        save("closed.json", closed)
        save("meta.json", {"updated": now.strftime("%Y-%m-%d %H:%M:%S"), "open_count": len(open_list),
                            "closed_count": len(closed), "account": (acc._asdict().get("login") if acc else None)})
        log(f"OK open={len(open_list)} closed={len(closed)}")
        return 0
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    sys.exit(main())
