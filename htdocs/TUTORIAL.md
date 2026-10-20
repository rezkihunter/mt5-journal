# TUTORIAL — MT5 Dashboard

Panduan memasang dan memakai dashboard.

## 1. Prasyarat

- Web server Apache + PHP 7.4/8.x.
- Data dari project **mt5-journal** (folder `JurnalMT5/data/`).

## 2. Struktur folder yang benar

`api.php` membaca data dari path relatif `../JurnalMT5/data`. Jadi susunannya:

```
workspace/
├── htdocs/            <- repo ini = DocumentRoot
│   ├── index.php
│   └── api.php
└── JurnalMT5/
    └──   data/          <- berisi closed.json, ai_report.json, ai_memory.json, open.json, account.json, meta.json
```

## 3. Setup

1. Clone repo dan letakkan seperti struktur di atas (sebelah folder `JurnalMT5`).
2. Arahkan **DocumentRoot** Apache ke folder repo ini.
   Contoh `httpd.conf`:
   ```apache
   DocumentRoot "C:/path/ke/workspace/htdocs"
   <Directory "C:/path/ke/workspace/htdocs">
       Require all granted
   </Directory>
   ```
3. Restart Apache, lalu buka `http://localhost/` (atau port yang dipakai).

### Cara cepat tanpa Apache (untuk tes)

Jalankan PHP built-in server dari folder repo:

```powershell
php -S 127.0.0.1:8080
```

Buka `http://127.0.0.1:8080`. Pastikan folder `../JurnalMT5/data` sudah berisi data.

## 4. Cara pakai

- Halaman auto-refresh tiap **10 detik** (tanpa reload manual).
- **Sidebar kiri** = filter posisi: *Semua posisi*, *Hit TP*, *Hit SL*.
- **Kalender** = ringkasan profit/loss per hari (hijau = profit, merah = loss).
- Kartu **Evaluasi AI** (dari `ai_report.json`) berisi laporan per jam dalam bahasa awam: ringkasan, yang sudah bagus, yang bikin rugi, dan saran perbaikan. Klik kartu untuk buka/tutup; di dalamnya ada **Memori & pola jangka panjang** (dari `ai_memory.json`) yang bisa dibuka terpisah.

## 5. Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| Tabel kosong, `api.php` balas `{}` | Belum ada data / path `JurnalMT5/data` salah | Jalankan collector **mt5-journal** dulu; pastikan folder sibling benar |
| 404 Not Found | DocumentRoot belum ke folder ini | Perbaiki `DocumentRoot` di Apache |
| Perubahan data tidak muncul | Data belum di-refresh logger | Tunggu logger berikutnya (mt5-journal) |
