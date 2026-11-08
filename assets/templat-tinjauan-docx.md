# Tinjauan keluaran Word — <buku>, <tanggal>, putaran <1–3>

Berkas: `<buku>/_book/<nama>.docx` (render <tanggal>). Peninjau membuka DOCX di Word (atau LibreOffice bila Word tidak ada; catat yang dipakai) dan, untuk butir otomatis, membaca hasil harness `--render`.
Setiap temuan ditulis dengan lokasi (bab, judul, halaman Word), masalah, dan sumber perbaikan: reference-doc (`_bersama/huruf.py`), filter Lua, `.qmd`, atau `_quarto.yml`. **DOCX tidak disunting langsung.** Sesudah perbaikan, render ulang dan buka putaran berikut. Batasnya 3 putaran; sisa temuan dieskalasi ke penulis.

Kolom "Otomatis" menyebut gerbang yang sudah memeriksa butir itu. Butir bertanda "—" diperiksa mata.

| No. | Butir | Otomatis | Hasil (ya/tidak/catatan) |
|---|---|---|---|
| **Rumus** | | | |
| 1 | Rumus sebaris, rumus tampilan (termasuk `aligned`, `cases`), dan rumus di tabel adalah persamaan Word asli (OMML): klik rumus membuka editor persamaan, bukan gambar atau teks TeX | G-DOCX-RUMUS (a)(b)(c) | |
| 2 | Tidak ada TeX mentah (`\frac`, `^{`, `$`) di teks biasa; `$` di blok kode R wajar | G-DOCX-RUMUS (b) | |
| 3 | Fon rumus sesuai gaya Word (`m:mathFont`: Cambria Math untuk gaya Windows); bentuk rumus di Word boleh berbeda dari PDF | G-DOCX-RUMUS (d) | |
| 4 | Nomor persamaan dan rujukan `@eq-` tampil dan sesuai | — | |
| 5 | Persamaan dapat dikonversi MathType (perlu dicek di versi MathType pengguna) | — | |
| **Huruf dan gaya paragraf** | | | |
| 6 | Teks, judul, kode, keluaran memakai huruf gaya Word yang dipilih (`reference-<ukuran>[-windows].docx`); tidak ada huruf pengganti | — (cek dengan python-docx: font run efektif) | |
| 7 | Paragraf isi menjorok baris pertama, spasi sebelum/sesudah 0; paragraf pertama sesudah judul juga menjorok | — | |
| 8 | Bahasa dokumen id-ID dan pemenggalan otomatis aktif | G-PENGGALAN (Word) | |
| **Halaman** | | | |
| 9 | Ukuran halaman dan margin sama dengan ukuran buku (`ukuran` di `konfig.json`) | G-DOCX (ukuran halaman) | |
| **Struktur** | | | |
| 10 | Halaman judul, lalu halaman hak cipta (versi teks di `index.qmd`) **sebelum** daftar isi | — | |
| 11 | Daftar isi ada dan dapat diperbarui (field TOC) | — | |
| 12 | Judul bab dan subbab bergaya Heading 1–3 dan bernomor sesuai PDF | G-DOCX (Heading1, nomor) | |
| 13 | Glosarium, Daftar Pustaka, dan riwayat penulis ada; indeks hanya di PDF | — | |
| **Gambar** | | | |
| 14 | Semua gambar muncul (termasuk diagram TikZ sebagai PNG) dan tidak melebihi bidang teks | G-DOCX (lebar gambar) | |
| 15 | Setiap gambar punya teks alternatif (`fig-alt`) dan keterangan bernomor | — | |
| 16 | Tidak ada ikon kotak (*callout*) berupa gambar kecil | G-DOCX (gambar ≤ 0,2 inci) | |
| **Tabel, kotak, kode** | | | |
| 17 | Tabel utuh, kepala tabel tebal, lebar kolom wajar, keterangan dan catatan di tempatnya | — | |
| 18 | Kotak (Tujuan belajar, Ingat, Penurunan) tampil dengan judulnya | — | |
| 19 | Kode dan keluaran bergaya Source Code/Verbatim Char, tidak terpotong, tanpa baris yang melewati tepi | — | |
| **Rujukan** | | | |
| 20 | Tidak ada "??", `@fig-`, `@tbl-`, `@sec-`, `@eq-` mentah; sitasi penulis-tahun terselesaikan | G-DOCX | |
| **Draf** | | | |
| 21 | Status draf terlihat (judul atau tanggal "Draf revisi ke-N"; tanda air DRAF hanya di PDF kecuali reference-doc diberi tanda air) | — | |

## Ringkasan putaran

- Temuan MAYOR: …
- Temuan MINOR: …
- Diperbaiki di sumber: … (berkas, perubahan)
- Sisa untuk penulis: …
