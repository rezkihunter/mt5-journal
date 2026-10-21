# MT5 Journal

Skrip Python untuk menarik riwayat trade dari MetaTrader 5, menyimpan snapshot posisi, dan menulis **laporan evaluasi AI agregat per 1 jam** (bahasa awam) dengan LLM **Groq**. Data JSON-nya dipakai oleh dashboard **htdocs**.

> Panduan lengkap (setup + cara pakai): **[TUTORIAL.md](TUTORIAL.md)**

## Alur

1. `fetch_closed.py` — konek ke MT5 (paket `MetaTrader5`), ambil posisi closed baru, gabung data SL/TP, simpan pita harga M5 ("tape"), lalu tulis `data/` (`closed.json`, `open.json`, `account.json`, `meta.json`, `sl_snapshot.json`, `tapes.json`, `cash_flow.json`).
2. `evaluate.py` — sekali per interval (`eval_interval_minutes`, default 60 mnt): gabung arsip kumulatif (`history.json`) + hitung statistik lokal dari **seluruh riwayat** (per jam/hari/pair/sesi/durasi/hasil, R-multiple, MAE/MFE, konsentrasi, revenge, **misfire/exit-quality, RR rencana vs realisasi, biaya**), lalu **1 panggilan** Groq (primary + fallback) menulis **2 blok**: laporan bahasa awam (termasuk **POLA PROFIT** dan **POLA LOSS** beserta penyebabnya) → `data/ai_report.json` dan memori pola jangka panjang (setiap pola menyimpan `sebab` + bukti) → `data/ai_memory.json`.

Keduanya dijalankan berkala oleh Scheduled Task lewat `run.bat` (fetch lalu evaluate). `run.vbs` menjalankan tanpa jendela.

## Menjalankan

```
run.bat
```

Konfigurasi di `config.json`: login akun, rentang hari, interval evaluasi AI, model primary/fallback (Qwen/Groq), batas token & memori, path terminal MT5.

## Rahasia

- API key Groq: `private/groq_key.txt` (folder `private/` di-`.gitignore`).
- `private/`, `*.log`, `.lastbusy` tidak di-commit.

## Catatan

- Butuh `pip install MetaTrader5` + MT5 desktop terinstal dan login.
- Snapshot contoh di `data/` ikut ter-commit agar UI dashboard bisa dilihat tanpa MT5.
- Deposit/withdrawal (`DEAL_TYPE_BALANCE`, credit, bonus) dicatat di `cash_flow.json` dan **tidak** dihitung sebagai trade — jadi winrate/net tidak tercemar. Cakupannya mengikuti `days_back`.
