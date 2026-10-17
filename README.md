# MT5 Dashboard

Dashboard web (PHP) untuk memantau jurnal trade MetaTrader 5 secara live: posisi close/open, hasil TP/SL, kalender harian, dan evaluasi AI per posisi. Tanpa database — data dibaca langsung dari file JSON.

## Fitur

- Ringkasan akun & metrik trade (net, winrate, jumlah posisi)
- Filter posisi: semua / Hit TP / Hit SL
- Kalender harian profit-loss
- Menampilkan evaluasi AI per posisi (dari `ai.json`)
- Auto-refresh tiap 30 detik, `Cache-Control: no-store`

## Arsitektur

- `index.php` — UI. Tema [Argon Dashboard 3](https://www.creative-tim.com/) (MIT, Creative Tim).
- `api.php` — endpoint JSON; membaca `../JurnalMT5/data/*.json`.
- `assets/` — CSS/JS/font tema Argon.

## Menjalankan (lokal)

1. Jadikan folder ini sebagai DocumentRoot Apache (contoh `http://127.0.0.1:2026`).
2. Pastikan folder `../JurnalMT5/data/` berisi data hasil logger — lihat project **mt5-journal**.
3. Buka `index.php` di browser.

## Data

`api.php` membaca `closed.json`, `ai.json`, `open.json`, `account.json`, `meta.json` yang dihasilkan oleh project `mt5-journal`.
