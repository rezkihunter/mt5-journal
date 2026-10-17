# TUTORIAL — MT5 Journal

Panduan memasang dan memakai skrip jurnal + evaluasi AI.

## 1. Prasyarat

- Python 3.8+.
- MetaTrader 5 desktop terinstal dan sudah **login** ke akun yang dipantau.
- Paket Python MetaTrader5:
  ```powershell
  pip install MetaTrader5
  ```
- API key OpenRouter (gratis) untuk evaluasi AI: https://openrouter.ai/keys

## 2. Setup

1. Clone repo, lalu edit **`config.json`**:
   ```json
   {
     "account_login": 425426658,
     "days_back": 120,
     "max_eval_per_run": 10,
     "model_primary": "nvidia/nemotron-3-ultra-550b-a55b:free",
     "model_fallback": "google/gemma-4-31b-it:free",
     "poll_seconds": 10,
     "scheduler_minutes": 1,
     "terminal_path": "C:\\Program Files\\MetaTrader 5 EXNESS\\terminal64.exe"
   }
   ```
   - `account_login`: nomor akun MT5.
   - `terminal_path`: lokasi `terminal64.exe` di komputermu.
   - `model_primary`/`model_fallback`: model OpenRouter (boleh model gratis).
   - `max_eval_per_run`: batas evaluasi AI tiap jalan (hemat kuota gratis).

2. Simpan API key OpenRouter ke **`private/openrouter_key.txt`** (satu baris, tanpa spasi).
   Folder `private/` sudah di-`.gitignore` sehingga key tidak ter-commit.

## 3. Cara jalan

### Manual

```powershell
run.bat
```

Isi `run.bat` = `fetch_closed.py` lalu `evaluate.py`.

Atau satu-satu:

```powershell
python fetch_closed.py   # tarik posisi close baru dari MT5 -> data/
python evaluate.py       # evaluasi AI posisi baru -> data/ai.json
```

### Otomatis (Scheduled Task)

1. Task Scheduler → **Create Task**.
2. Trigger: **Daily**, repeat tiap **1 menit** (atau sesuai `scheduler_minutes`).
3. Action: jalankan **`run.vbs`** (jalan tanpa jendela) — atau `run.bat` bila ingin lihat log.
4. Pastikan MT5 sudah login saat task berjalan.

## 4. Output

Hasil ditulis ke `data/`:

| File | Isi |
|---|---|
| `closed.json` | posisi yang sudah ditutup |
| `open.json` | posisi masih terbuka |
| `account.json` | info akun (balance/equity) |
| `meta.json` | metadata terakhir diperbarui |
| `sl_snapshot.json` | snapshot SL/TP |
| `tapes.json` | pita harga M5 per posisi |
| `ai.json` | evaluasi AI per posisi (`position_id` → teks) |

Lihat hasil di web pakai project **mt5-dashboard**.

## 5. Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| `INIT_FAIL` | MT5 tidak jalan / `terminal_path` salah / belum login | Buka MT5, cek `config.json` |
| `FAIL ... 429` | Rate limit model gratis OpenRouter | Skrip otomatis `sleep` lalu lanjut; kurangi `max_eval_per_run` |
| Evaluasi AI tidak muncul | `private/openrouter_key.txt` kosong/salah | Isi API key yang valid |
| Data tidak update | Scheduled Task tidak jalan | Cek Task Scheduler + `run.log` |
