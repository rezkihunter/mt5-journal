# MT5 Journal

Skrip Python untuk menarik riwayat trade dari MetaTrader 5, menyimpan snapshot posisi, dan mengevaluasi tiap posisi yang baru ditutup dengan LLM (OpenRouter). Data JSON-nya dipakai oleh dashboard di folder [`htdocs/`](../htdocs) (satu repo).

> Panduan lengkap (setup + cara pakai): **[TUTORIAL.md](TUTORIAL.md)**

## Alur

1. `fetch_closed.py` — konek ke MT5 (paket `MetaTrader5`), ambil posisi closed baru, gabung data SL/TP, simpan pita harga M5 ("tape"), lalu tulis `data/` (`closed.json`, `open.json`, `account.json`, `meta.json`, `sl_snapshot.json`, `tapes.json`).
2. `evaluate.py` — untuk tiap posisi baru, susun prompt dari tape M5 lalu panggil model gratis OpenRouter (primary + fallback) → simpan evaluasi ke `data/ai.json`.

Keduanya dijalankan berkala oleh Scheduled Task lewat `run.bat` (fetch lalu evaluate). `run.vbs` menjalankan tanpa jendela.

## Menjalankan

```
run.bat
```

Konfigurasi di `config.json`: login akun, rentang hari, jumlah eval per run, model primary/fallback, path terminal MT5.

## Rahasia

- API key OpenRouter: `private/openrouter_key.txt` (folder `private/` di-`.gitignore`).
- `private/`, `*.log`, `.lastbusy` tidak di-commit.

## Catatan

- Butuh `pip install MetaTrader5` + MT5 desktop terinstal dan login.
- Snapshot contoh di `data/` ikut ter-commit agar UI dashboard bisa dilihat tanpa MT5.
