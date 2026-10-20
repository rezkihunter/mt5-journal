# TUTORIAL — MT5 Journal

Panduan memasang dan memakai skrip jurnal + evaluasi AI.

## 1. Prasyarat

- Python 3.8+.
- MetaTrader 5 desktop terinstal dan sudah **login** ke akun yang dipantau.
- Paket Python MetaTrader5:
  ```powershell
  pip install MetaTrader5
  ```
- API key **Groq** (gratis, tanpa kartu) untuk evaluasi AI: https://console.groq.com/keys

## 2. Setup

1. Clone repo, lalu edit **`config.json`**:
   ```json
   {
     "account_login": 425426658,
     "days_back": 120,
     "eval_interval_minutes": 60,
     "eval_skip_if_unchanged": true,
     "provider": "groq",
     "api_base": "https://api.groq.com/openai/v1/chat/completions",
     "key_file": "groq_key.txt",
     "model_primary": "qwen/qwen3.8-27b",
     "model_fallback": "openai/gpt-oss-120b",
     "reasoning_effort": "low",
     "max_tokens": 6000,
     "memory_max_words": 200,
     "poll_seconds": 10,
     "scheduler_minutes": 1,
     "terminal_path": "C:\\Program Files\\MetaTrader 5 EXNESS\\terminal64.exe"
   }
   ```
   - `account_login`: nomor akun MT5.
   - `terminal_path`: lokasi `terminal64.exe` di komputermu.
   - `api_base`/`key_file`/`model_primary`/`model_fallback`: endpoint + kunci + model LLM (Groq, OpenAI-compatible). Primer `qwen/qwen3.8-27b`, fallback `openai/gpt-oss-120b`.
   - `reasoning_effort`: `low` agar model reasoning (gpt-oss/qwen) tidak menghabiskan token untuk "berpikir".
   - `max_tokens`: batas token keluaran (6000 = cukup laporan + memori).
   - `memory_max_words`: panjang maksimal memori pola jangka panjang (default 200 kata).
   - `eval_interval_minutes`: jeda minimal antar laporan AI (default 60 = 1 jam, hemat kuota gratis).
   - `eval_skip_if_unchanged`: lewati laporan bila tak ada posisi close baru.





2. Simpan API key Groq ke **`private/groq_key.txt`** (satu baris, tanpa spasi).
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
python evaluate.py       # laporan AI per jam + memori jangka panjang (bila interval terlampaui) -> data/ai_report.json + data/ai_memory.json
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
| `ai_report.json` | laporan evaluasi AI per jam (`eval` = narasi bahasa awam, `data` = stat-pack) |
| `ai_memory.json` | memori pola jangka panjang (`text` = pola + keyakinan + tren, diperbarui tiap jam) |
| `history.json` | arsip kumulatif semua posisi close (dedup, tak hilang walau fetch cuma 120 hari) |
| `ai.json` | arsip evaluasi AI per-posisi lama (tidak dipakai lagi) |

Lihat hasil di web pakai project **mt5-dashboard**.

## 5. Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| `INIT_FAIL` | MT5 tidak jalan / `terminal_path` salah / belum login | Buka MT5, cek `config.json` |
| `FAIL report ... 429` | Rate limit model gratis Groq | Skrip otomatis `sleep` + fallback; laporan dibuat lagi jam berikutnya |
| `FAIL report ... 403` | Header `User-Agent` hilang / key salah | Pastikan `private/groq_key.txt` benar (skrip sudah kirim UA) |
| Evaluasi AI tidak muncul | `private/groq_key.txt` kosong/salah / blok `===MEMORI===` terpotong | Isi API key yang valid; naikkan `max_tokens` |
| Data tidak update | Scheduled Task tidak jalan | Cek Task Scheduler + `run.log` |
