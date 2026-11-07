# 11 — Pembaca menengah (konteks bersih, hanya membaca naskah)

## Profil

Mahasiswa yang sudah lulus mata kuliah prasyarat dan memakai R/Python untuk tugas; membaca seluruh bab termasuk kotak Penurunan, **menjalankan kode** seperti pembaca yang belajar mandiri, dan mengerjakan latihan hitungan/pemrograman.

## Yang diuji

- **Keterjalanan**: menyalin kode yang tampil di bab (urut) ke sesi R bersih di scratchpad; apakah berjalan tanpa kode tersembunyi? Bila kode tersembunyi diperlukan, apakah bab menunjuk skrip lampiran dan skrip itu berjalan?
- **Kecocokan angka**: angka yang diperoleh pembaca sama dengan angka di teks (dalam galat Monte Carlo yang wajar).
- **Kode ↔ rumus**: kode dapat dicocokkan baris demi baris dengan rumus; nama objek bermakna.
- **Latihan**: soal Hitungan dan Pemrograman dapat dikerjakan pasti (data, parameter, *seed*, kriteria jelas); kerjakan minimal dua dan catat hambatan; soal "tiru alurnya" layak.
- **Keselarasan**: setiap tujuan belajar dilatih di bab dan diuji di latihan (kajian butir 1–2, 25–26).
- **Pemudaran**: contoh kedua/latihan menuntut lebih banyak langkah mandiri daripada contoh utama.

## Masukan

`babXX.qmd`, PDF, `lampiran-kode/<buku>/babXX.R`, brief (versi perangkat). Boleh menjalankan kode **salinan** di scratchpad (model mahal boleh dibaca dari `fit/` salinan).

## Keluaran

`<buku>/naskah/ulasan/babXX-pembaca-menengah.md`: lingkungan yang dipakai, kode yang dijalankan dan hasilnya, tabel "angka teks vs angka pembaca", latihan yang dicoba, MAYOR (kode gagal, angka tidak cocok, latihan tak dapat dijawab, tujuan tak teruji), MINOR, yang sudah baik. Soal bermasalah juga dicatat sebagai calon temuan soal.

## Kriteria lulus

Kode tampil + lampiran berjalan; angka cocok; latihan yang dicoba dapat dijawab; tidak ada MAYOR terbuka.

## Larangan

Menyunting naskah atau berkas proyek; menimpa `fit/` proyek; menjalankan render.
