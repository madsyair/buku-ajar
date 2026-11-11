# Skrip skill buku-ajar

Salinan yang digeneralisasi dari harness dan alat seri statistika Bayesian (A. S. Choir, 2026). Skrip tidak dijalankan dari folder skill: **disalin ke proyek** (`siapkan_proyek.py` melakukannya), karena harness menghitung akar proyek dari letaknya sendiri (`harness/..`).

| Berkas | Tujuan di proyek | Fungsi |
|---|---|---|
| `siapkan_proyek.py` | (dijalankan dari skill) | Membuat tata letak proyek dan menyalin semua berkas di bawah; tidak menimpa tanpa `--timpa` |
| `harness.py` | `harness/` | Gerbang mutu per bab (daftar di `references/harness-dan-gerbang.md`) |
| `referensi.py` | `harness/` | G-REFERENSI: registri klaim dan identitas pustaka |
| `penggalan.py` | `harness/` | Pemenggalan EYD V, daftar nama yang tidak dipenggal, istilah asing (perlu `pip install Sastrawi`) |
| `uji_harness.sh`, `uji-buku/` | `harness/` | Uji regresi harness: fikstur gagal harus GAGAL, `babbaik` harus LULUS; G-TAG diuji pada `tag-tanpa.pdf` (GAGAL) dan `tag-baik.pdf` (LULUS); G-LN pada `babln.qmd` (GAGAL) dan `babbaik.qmd` (LULUS); G-LOG pada `log/rerun.txt`, `log/ganda.txt` (GAGAL) dan `log/bersih.txt` (LULUS); G-DOCX pada `docx/docx-baik.docx` (LULUS, termasuk bidang Zotero) dan tujuh fikstur fitur otomatis Word (`docx-zotero`: JSON ZOTERO_ITEM rusak; `docx-tanpa-otomatis` juga GAGAL karena sitasi statis); setiap fikstur GAGAL dengan pesannya sendiri (`docx/buat_fikstur.py` membangunnya ulang dengan Pandoc) |
| `kemas_sumber.py` | `harness/` atau `alat/` | Mengemas kode sumber per buku (+ kunci) ke zip dengan `BANGUN.md` |
| `gaya_gambar.py` | `_bersama/` | Gaya matplotlib seri: palet, huruf teks dan matematika opsi `huruf` (Type 3), `LEBAR` = lebar kolom, koma desimal, `label_panel()`, `tampil()` |
| `huruf.py` | `_bersama/` | Opsi huruf (`libertinus`, `springer`, `crc`, `stix`), profil penerbit (`seri`, `springer`, `crc`, `wiley`), dan ukuran buku (`b5`, `unesco`, `a5`, `a4`, `6x9`, `7x10`) dari `konfig.json`: menulis blok `>>> huruf`/`>>> profil` di `_quarto.yml` dan `_bersama/*.tex`, menghitung ukuran mono kode/keluaran, `options(width)` di `<buku>/.Rprofile`, gaya Word Windows; dipakai `gaya_gambar.py` dan G-HURUF. `python3 _bersama/huruf.py --daftar` |
| `catatan.lua` | `_bersama/` | Filter Div `::: {.catatan}`: "*Catatan:*" kecil di bawah tabel/gambar (PDF dan Word) |
| `bahasa-asing.lua` | `_bersama/` | Frasa miring di `istilah-asing.txt` diberi `lang=en` (pemenggalan Inggris) |
| `word-otomatis.lua` | `_bersama/` | Hanya DOCX (`at: post-render`): nomor bab/gambar/tabel/persamaan sebagai bidang SEQ, rujukan silang REF, Daftar Isi/Gambar/Tabel sesudah halaman hak cipta, teks alternatif, lebar gambar, lebar kolom, dan "Lampiran"; bidang teks dibaca dari reference-doc (`references/aturan-gaya-dan-tampilan.md`, "Rumus dan fitur otomatis di Word") |
| `zotero-word.lua` | `_bersama/` | Hanya DOCX (`at: post-render`, sesudah `word-otomatis.lua`): sitasi sebagai bidang `ADDIN ZOTERO_ITEM CSL_CITATION` dengan butir tersemat dari `pustaka.bib`, Daftar Pustaka `ADDIN ZOTERO_BIBL`, preferensi `ZOTERO_PREF_n`; tanpa Zotero saat render (`references/zotero-word.md`) |

## Memasang di proyek baru

```bash
python3 <skill>/scripts/siapkan_proyek.py --proyek ~/sumber/seri-x --buku buku1 \
    --judul "Judul Buku" --penulis "Nama Penulis"
cd ~/sumber/seri-x
pip install Sastrawi pandas pyarrow matplotlib seaborn   # bila belum
bash harness/uji_harness.sh                              # semua baris harus "benar"
```

Prasyarat perangkat: R (knitr, arrow; paket bab), Quarto ≥ 1.6, TeX Live (diuji 2023) dengan **LuaLaTeX** (Debian: `texlive-luatex` untuk `lualatex-math`, `texlive-latex-extra`, `texlive-fonts-extra` untuk huruf Libertinus Serif/Mono/Math dan `libertinus-type1`/`libertinust1math` bagi TikZ; paket `indentfirst`, `draftwatermark`, `needspace`, `fvextra`, `tcolorbox`, `pdfpages` bila memakai sampul), Python 3 (matplotlib menemukan OTF Libertinus di folder TeX Live atau lewat `kpsewhich`), poppler-utils (`pdftotext` untuk audit PDF, `pdfinfo` untuk G-TAG), `pikepdf` opsional (cek `/Lang` G-TAG), skill **eyd** terpasang (`eyd/scripts/periksa.py`; atau set `SKILL_EYD=<jalur>`).

## Yang perlu disesuaikan per proyek

Semua yang khusus proyek ada di `harness/konfig.json` (contoh: `assets/konfig.json`):

| Kunci | Arti | Bawaan |
|---|---|---|
| `bersama` | folder preamble, filter, gaya gambar | `_bersama` |
| `lampiran` | folder skrip lampiran yang dibangkitkan G-LAMPIRAN | `lampiran-kode` |
| `id_bab_polos` | buku yang kunci klaimnya nama bab saja (registri lama) | `[]` (kunci = `<buku>/<bab>`) |
| `penulis` | nama keluarga penulis tambahan untuk G-SITASI (nama dari `pustaka.bib` diambil otomatis) | `[]` |
| `larangan` | pola kata terlarang di naskah (G-LARANGAN); menggantikan bawaan bila diisi | Sokratik/Socrates/Feynman |
| `istilah_terlarang` | pola istilah yang sudah diganti keputusan penulis (G-ISTILAH) | `[]` |
| `kemasan` | keterangan perangkat per buku untuk `BANGUN.md` | `{}` |

Hal lain yang masih tertanam di kode dan mungkin perlu diubah:

- `harness.py`: batas lebar (`BATAS_LEBAR`, `BATAS_LEBAR_KELUARAN`), judul (`MAKS_KATA_JUDUL_*`), daftar `SLOP_ID`, pola atribusi lembaga (`POLA_ATRIBUSI_MANUAL`: BPS, Stan Development Team, R Core Team — tambahkan lembaga bidang lain), daftar penghubung `POLA_KONJ`, singkatan (`SINGKATAN`).
- `penggalan.py`: daftar eponim yang tidak dipenggal di `nama_diri()` (Bayes, Poisson, Gauss, …).
- `gaya_gambar.py`: palet per buku (`PALET_BUKU*`); `LEBAR` dihitung dari kolom (B5 seri 4,72 inci); jalur fon dicari dengan `kpsewhich`, lalu `_FON_CALON`.
- `konfig.json`: `huruf`, `profil`, `ukuran`, `docx_huruf`, `batas_kode`, `batas_keluaran`; sesudah mengubahnya jalankan `python3 _bersama/huruf.py --proyek . --buku <buku>`.
- `_bersama/preamble.tex` (dari `assets/preamble.tex`): warna seri, sampul, tanda air; blok lebar (`\tambahlebar`) dihitung dari kertas dan margin.
- `_bersama/doc-class.tex` (dari `assets/doc-class.tex`): modul `testphase` `\DocumentMetadata`; di TeX Live 2024+ pertimbangkan `tagging=on`.
- `G-GAYA` memakai skill math-article bila terpasang (`SKILL_GAYA`), selain itu pemeriksa cadangan.

## Perbedaan dari harness proyek seri

- Konfigurasi proyek dipindah ke `konfig.json` (sebelumnya daftar penulis, nama buku `buku1-dasar`, `_bersama`, `lampiran-kode` tertanam di kode).
- Daftar penulis G-SITASI dibangun otomatis dari `pustaka.bib`.
- Gerbang baru: **G-LARANGAN** (nama teknik pengajaran dan kata terlarang lain), **G-ISTILAH** (istilah yang sudah diputuskan), **G-HALJUDUL** (tanpa `subtitle`, `date` ISO, "Draf revisi ke-N" di `date-format`).
- Fikstur baru `uji-buku/bablarangan.qmd`.
- G-LOG sama dengan seri (log LaTeX akhir stabil, tanpa label ganda); G-LN baru di skill (`\log` tanpa basis di rumus prosa; sakelar `LN`, pengecualian `ln-abaikan`); fikstur `uji-buku/babln.qmd` dan `uji-buku/log/*.txt`.
- `siapkan_proyek.py` juga menyalin `assets/hak-cipta.tex` (halaman hak cipta dengan fon dan lisensinya) dan mengisi judul serta penulis di `include-before-body`.
- G-TAG sama dengan seri, ditambah opsi `--tag-pdf`, sakelar `TAG`, dan cek `/Lang` cadangan tanpa pikepdf; fikstur PDF `uji-buku/tag-*.pdf`.
- Folder laporan dibuat otomatis; `penggalan.py` menghimpun semua folder buku yang punya `_quarto.yml` (bukan hanya `buku*`).
- `kemas_sumber.py` mengenali buku otomatis (folder dengan `_quarto.yml`; pasangan `kunci-<buku>`).

Diuji 2026-11-07: `uji_harness.sh` (9 fikstur gagal GAGAL, `babbaik` LULUS); `assets/templat-bab.qmd` dan `assets/templat-bab-kunci.qmd` LULUS pada proyek hasil `siapkan_proyek.py` (R 4.6, tanpa `--render`).

Diuji ulang 2026-11-07 (tipografi): `uji_harness.sh` hijau (9 fikstur GAGAL, `babbaik` LULUS, G-TAG pada dua PDF fikstur); `templat-bab.qmd` LULUS tanpa dan dengan `--render` (G-RENDER, G-TAG, G-TEPI, G-PENGGALAN; `pdffonts` hanya Libertinus) pada proyek baru hasil `siapkan_proyek.py` (TeX Live 2023, Quarto 1.10).
