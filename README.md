# MT5 Journal + Dashboard

Satu project untuk memantau & mengevaluasi jurnal trade MetaTrader 5:

- **`JurnalMT5/`** — skrip Python: tarik riwayat trade dari MT5, simpan snapshot posisi, lalu evaluasi tiap posisi yang baru ditutup dengan LLM (OpenRouter). Data JSON ditulis ke `JurnalMT5/data/`.
- **`htdocs/`** — dashboard web PHP (tanpa database) yang membaca `JurnalMT5/data/*.json` dan menampilkannya: posisi close/open, hasil TP/SL, kalender harian, dan evaluasi AI.

```
.
├── JurnalMT5/     # backend (Python) + data/
└── htdocs/        # dashboard (PHP) — DocumentRoot web server
```

## Alur

1. `JurnalMT5/fetch_closed.py` — konek ke MT5, ambil posisi closed baru, simpan pita harga M5, tulis `data/`.
2. `JurnalMT5/evaluate.py` — evaluasi tiap posisi baru via model OpenRouter (primary + fallback) → `data/ai.json`.
3. `htdocs/api.php` + `htdocs/index.php` — baca data dan render dashboard (auto-refresh 30 detik).

Keduanya dijalankan berkala lewat `JurnalMT5/run.bat` (fetch lalu evaluate); `run.vbs` menjalankannya tanpa jendela.

## Menjalankan singkat

Backend:

```
JurnalMT5\run.bat
```

Dashboard:

1. Arahkan **DocumentRoot** Apache ke folder `htdocs/`.
2. Buka `http://localhost/` (atau `php -S 127.0.0.1:8080` dari dalam `htdocs/` untuk tes).

Panduan lengkap tiap bagian: [`JurnalMT5/TUTORIAL.md`](JurnalMT5/TUTORIAL.md) dan [`htdocs/TUTORIAL.md`](htdocs/TUTORIAL.md).

## Rahasia

- API key OpenRouter: `JurnalMT5/private/openrouter_key.txt` (folder `private/` di-`.gitignore`, tidak ikut ter-commit).
- Snapshot contoh di `JurnalMT5/data/` ikut ter-commit agar UI bisa dilihat tanpa MT5.
