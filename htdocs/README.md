# MT5 Dashboard

Dashboard web (PHP) untuk memantau jurnal trade MetaTrader 5 secara live: posisi close/open, hasil TP/SL, kalender harian, laporan evaluasi AI **per jam** (bahasa awam), dan **memori pola jangka panjang**. Tanpa database — data dibaca langsung dari file JSON.

> Panduan lengkap (setup + cara pakai): **[TUTORIAL.md](TUTORIAL.md)**

## Fitur

- Ringkasan akun & metrik trade (net, winrate, jumlah posisi)
- Kartu **Deposit / WD** + **Growth (ex-cash)** — cash flow dipisah dari P&L trade, jadi pertumbuhan akun tidak salah dibaca saat ada deposit/withdrawal
- Filter posisi: semua / Hit TP / Hit SL
- Kalender harian profit-loss
- Kartu **Evaluasi AI per jam** (dari `ai_report.json`) — ringkasan, **pola profit & pola loss beserta penyebabnya**, saran perbaikan; plus `<details>` **Memori & pola jangka panjang** (dari `ai_memory.json`)
- Auto-refresh tiap 10 detik, `Cache-Control: no-store`

## Arsitektur

- `index.php` — UI. Tema [Argon Dashboard 3](https://www.creative-tim.com/) (MIT, Creative Tim).
- `api.php` — endpoint JSON; membaca `../JurnalMT5/data/*.json`.
- `assets/` — CSS/JS/font tema Argon.

## Menjalankan (lokal)

1. Jadikan folder ini sebagai DocumentRoot Apache (contoh `http://127.0.0.1:2026`).
2. Pastikan folder `../JurnalMT5/data/` berisi data hasil logger — lihat project **mt5-journal**.
3. Buka `index.php` di browser.

## Data

`api.php` membaca `closed.json`, `cash_flow.json`, `ai_report.json`, `ai_memory.json`, `open.json`, `account.json`, `meta.json` yang dihasilkan oleh project `JurnalMT5`.
