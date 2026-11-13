# Tinjauan keluaran Word — <buku>, <tanggal>, putaran <1–3>

Berkas: `<buku>/_book/<nama>.docx` (render <tanggal>). Peninjau membuka DOCX di Word (atau LibreOffice bila Word tidak ada; catat yang dipakai) dan, untuk butir otomatis, membaca hasil harness `--render`.
Setiap temuan ditulis dengan lokasi (bab, judul, halaman Word), masalah, dan sumber perbaikan: reference-doc (`_bersama/huruf.py`), filter Lua, `.qmd`, atau `_quarto.yml`. **DOCX tidak disunting langsung.** Sesudah perbaikan, render ulang dan buka putaran berikut. Batasnya 3 putaran; sisa temuan dieskalasi ke penulis.

Kolom "Otomatis" menyebut gerbang yang sudah memeriksa butir itu. Butir bertanda "—" diperiksa mata. Nomor, rujukan silang, dan daftar dibuat `_bersama/word-otomatis.lua` sebagai bidang Word; perbarui semua bidang (Word: Ctrl+A lalu F9, atau terima tawaran saat dokumen dibuka) sebelum memeriksa nomor halaman daftar. Rincian: `references/aturan-gaya-dan-tampilan.md`, "Rumus dan fitur otomatis di Word".

| No. | Butir | Otomatis | Hasil (ya/tidak/catatan) |
|---|---|---|---|
| **Rumus** | | | |
| 1 | Rumus sebaris, rumus tampilan (termasuk `aligned`, `cases`), dan rumus di tabel adalah persamaan Word asli (OMML): klik rumus membuka editor persamaan, bukan gambar atau teks TeX | G-DOCX-RUMUS (a)(b)(c) | |
| 2 | Tidak ada TeX mentah (`\frac`, `^{`, `$`) di teks biasa; `$` di blok kode R wajar | G-DOCX-RUMUS (b) | |
| 3 | Fon rumus sesuai gaya Word (`m:mathFont`: Cambria Math untuk gaya Windows); bentuk rumus di Word boleh berbeda dari PDF | G-DOCX-RUMUS (d) | |
| 4 | Nomor persamaan rata kanan di luar rumus (bidang SEQ Persamaan), rujukan "persamaan (n.n)" (bidang REF), sesuai PDF; rumus `aligned` diperiksa di Word, bukan LibreOffice | G-DOCX (SEQ, REF) | |
| 5 | Persamaan dapat dikonversi MathType (perlu dicek di versi MathType pengguna) | — | |
| **Huruf dan gaya paragraf** | | | |
| 6 | Teks, judul, kode, keluaran memakai huruf gaya Word yang dipilih (`reference-<ukuran>[-windows].docx`); tidak ada huruf pengganti | — (cek dengan python-docx: font run efektif) | |
| 7 | Paragraf isi menjorok baris pertama, spasi sebelum/sesudah 0; paragraf pertama sesudah judul juga menjorok | — | |
| 8 | Bahasa dokumen id-ID dan pemenggalan otomatis aktif | G-PENGGALAN (Word) | |
| **Halaman** | | | |
| 9 | Ukuran halaman dan margin sama dengan PDF (`ukuran` di `konfig.json`; B5 28/28/22/24 mm, bidang teks 12 cm) | G-DOCX (ukuran, margin) | |
| 9a | Tanda air DRAF di belakang teks dan nomor halaman di footer (hapus tanda air dari reference-doc untuk naskah akhir) | — | |
| **Struktur** | | | |
| 10 | Halaman judul, lalu halaman hak cipta (blok `custom-style="Hak Cipta"` di `index.qmd`) **sebelum** daftar isi | G-DOCX (hak cipta sebelum TOC) | |
| 11 | Daftar Isi, Daftar Gambar, dan Daftar Tabel ada sebagai bidang TOC; nomor halaman muncul sesudah bidang diperbarui | G-DOCX (bidang TOC) | |
| 12 | Judul bab dan subbab bergaya Heading 1–3 dan bernomor sesuai PDF | G-DOCX (Heading1, nomor) | |
| 12a | Judul lampiran "Lampiran A — …", bukan "Appendix" | — | |
| 13 | Glosarium, Daftar Pustaka, dan riwayat penulis ada; indeks hanya di PDF | — | |
| **Gambar** | | | |
| 14 | Semua gambar muncul (termasuk diagram TikZ sebagai PNG), tidak melebihi bidang teks, dan tidak terpotong di sel tabel (gaya `Compact` tanpa menjorok) | G-DOCX (lebar gambar) | |
| 15 | Setiap gambar punya teks alternatif (`fig-alt` atau judul) dan keterangan bernomor (bidang SEQ Gambar) | G-DOCX (alt-text, SEQ) | |
| 16 | Tidak ada ikon kotak (*callout*) berupa gambar kecil | G-DOCX (gambar ≤ 0,2 inci) | |
| **Tabel, kotak, kode** | | | |
| 17 | Tabel utuh, kepala tabel tebal, tidak ada kolom yang lebih sempit dari satu kata (kata terpenggal per huruf), perataan kolom sesuai sumber, keterangan bernomor (SEQ Tabel) dan catatan (gaya `Catatan`) di tempatnya | G-DOCX (SEQ Tabel) | |
| 18 | Kotak (Tujuan belajar, Ingat, Penurunan) tampil dengan judulnya | — | |
| 19 | Kode dan keluaran bergaya Source Code/Verbatim Char (7 pt pada B5), tidak terpotong, tanpa baris yang melewati tepi | — | |
| **Rujukan** | | | |
| 20 | Tidak ada "??", `@fig-`, `@tbl-`, `@sec-`, `@eq-` mentah; setiap rujukan silang adalah bidang REF ke bookmark yang ada; sitasi penulis-tahun terselesaikan dan bertaut ke Daftar Pustaka (`link-citations`) | G-DOCX (REF) | |
| **Draf** | | | |
| 21 | Status draf terlihat (tanggal "Draf revisi ke-N" dan tanda air DRAF dari reference-doc) | — | |

## Batasan yang diketahui (bukan temuan)

- Huruf tidak tersemat di DOCX: pembaca harus memasang huruf opsi (mis. Libertinus) atau memakai gaya Word Windows.
- Nomor halaman Daftar Isi, Daftar Gambar, dan Daftar Tabel muncul sesudah bidang diperbarui; LibreOffice dan Google Docs menampilkan entri tanpa nomor halaman.
- LibreOffice menampilkan penanda perataan `aligned` sebagai simbol ("∧", "¿"); periksa rumus bertingkat di Word.
- Indeks hanya ada di PDF.

## Keputusan penulis

- Sitasi sebagai bidang Zotero (`zotero-word.lua`, bawaan sejak 2026-11-11; `zotero-word: false` mematikannya): tetap/matikan, alasan. Periksa jumlah ZOTERO_ITEM = jumlah sitasi, satu ZOTERO_BIBL, `ZOTERO_PREF_n`, dan teks sitasi terbaca di LibreOffice (G-DOCX). Langkah penulis dan batasan: `references/zotero-word.md`.

## Ringkasan putaran

- Temuan MAYOR: …
- Temuan MINOR: …
- Diperbaiki di sumber: … (berkas, perubahan)
- Sisa untuk penulis: …
