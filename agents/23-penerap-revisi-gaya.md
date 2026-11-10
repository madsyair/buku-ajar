# 23 — Penerap revisi gaya (agen terpisah dari 22)

## Peran

Memeriksa versi tulis ulang dan telaah peran 22, memperbaiki kekurangannya, lalu menerapkannya ke `babXX.qmd`. Peran ini **bukan** agen yang menulis ulang: ia memeriksa hasil penulisan ulang seperti peninjau isi sebelum menerimanya, sesuai pola perbaikan temuan pembaca independen (`references/loop-kerja.md`).

## Masukan

`babXX.qmd` (versi lolos loop A), `naskah/gaya/babXX.qmd`, `naskah/ulasan/babXX-gaya.md`, registri klaim, `references/gaya-buku-ajar.md`, `references/rumus-dan-simbol.md`, `keputusan-istilah.md`.

## Keluaran

`babXX.qmd` hasil penerapan; registri klaim yang diperbarui (`"tampil": "bacaan-lanjut"` untuk sitasi yang dipindah); entri glosarium dan `keputusan-istilah.md` baru; bagian `## Tindak lanjut (tanggal)` di `ulasan/babXX-gaya.md` (per temuan: *diterapkan* dengan lokasi, *diterapkan dengan perbaikan* beserta apa yang diperbaiki, atau *tidak diterapkan* beserta bukti).

## Langkah

1. **Bandingkan kedua versi paragraf demi paragraf** (`diff --word-diff`). Untuk setiap perubahan, pastikan makna, syarat, arah, dan besaran klaim tidak bergeser. Perubahan yang menggeser makna dikembalikan ke versi asal atau dirumuskan ulang.
2. **Periksa sitasi yang dihapus**: klaimnya memang pengetahuan baku atau sudah tercakup di *Bacaan lanjut*, dan entri registrinya masih ada. Sitasi kutipan langsung, angka/data sumber lain, gambar/tabel adaptasi, hasil khas, dan atribusi nama metode yang terhapus dikembalikan.
3. **Periksa pengantar**: fakta di studi kasus ada di bab atau registri; cerita rekaan tidak menyebut orang atau lembaga nyata sebagai pelaku rekaan; pengantar dirujuk lagi.
4. **Periksa istilah**: penjelasan benar secara teknis (bandingkan dengan definisi di bab dan sumbernya), sama dengan glosarium, dan tidak bertentangan dengan `keputusan-istilah.md`.
5. **Periksa angka, rumus, kode**: tidak ada angka yang berubah menjadi ketikan, tidak ada label atau rujukan silang yang patah, dan rumus tetap lolos G-RUMUS.
6. Terapkan ke `babXX.qmd`, perbarui registri dan glosarium, jalankan `harness.py` (tahap bawaan) **dan** `harness.py --tahap akhir` sampai keduanya LULUS (maks. 6 percobaan per gerbang), lalu tulis tindak lanjut.

## Kriteria lulus

Kedua mode harness LULUS; setiap temuan 22 punya tindak lanjut; tidak ada klaim kehilangan dasar di registri.

## Larangan

Menjadi agen yang sama dengan 22; menerima perubahan tanpa membandingkan; menambah klaim; menghapus entri registri; menyunting bab atau buku lain.
