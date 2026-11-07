# Skrip skill buku-ajar

Salinan yang digeneralisasi dari harness dan alat seri statistika Bayesian (A. S. Choir, 2026). Skrip tidak dijalankan dari folder skill: **disalin ke proyek** (`siapkan_proyek.py` melakukannya), karena harness menghitung akar proyek dari letaknya sendiri (`harness/..`).

| Berkas | Tujuan di proyek | Fungsi |
|---|---|---|
| `siapkan_proyek.py` | (dijalankan dari skill) | Membuat tata letak proyek dan menyalin semua berkas di bawah; tidak menimpa tanpa `--timpa` |
| `harness.py` | `harness/` | Gerbang mutu per bab (daftar di `references/harness-dan-gerbang.md`) |
| `referensi.py` | `harness/` | G-REFERENSI: registri klaim dan identitas pustaka |
| `penggalan.py` | `harness/` | Pemenggalan EYD V, daftar nama yang tidak dipenggal, istilah asing (perlu `pip install Sastrawi`) |
| `uji_harness.sh`, `uji-buku/` | `harness/` | Uji regresi harness: fikstur gagal harus GAGAL, `babbaik` harus LULUS |
| `kemas_sumber.py` | `harness/` atau `alat/` | Mengemas kode sumber per buku (+ kunci) ke zip dengan `BANGUN.md` |
| `gaya_gambar.py` | `_bersama/` | Gaya matplotlib seri: palet, fon, koma desimal, `label_panel()`, `tampil()` |
| `catatan.lua` | `_bersama/` | Filter Div `::: {.catatan}`: "*Catatan:*" kecil di bawah tabel/gambar (PDF dan Word) |
| `bahasa-asing.lua` | `_bersama/` | Frasa miring di `istilah-asing.txt` diberi `lang=en` (pemenggalan Inggris) |

## Memasang di proyek baru

```bash
python3 <skill>/scripts/siapkan_proyek.py --proyek ~/sumber/seri-x --buku buku1 \
    --judul "Judul Buku" --penulis "Nama Penulis"
cd ~/sumber/seri-x
pip install Sastrawi pandas pyarrow matplotlib seaborn   # bila belum
bash harness/uji_harness.sh                              # semua baris harus "benar"
```

Prasyarat perangkat: R (knitr, arrow; paket bab), Quarto ≥ 1.6, TeX Live dengan XeLaTeX (fon TeX Gyre Pagella/Heros, DejaVu Sans Mono; paket `indentfirst`, `draftwatermark`, `needspace`, `fvextra`, `pdfpages` bila memakai sampul), Python 3, `pdftotext` (poppler) untuk audit PDF, skill **eyd** terpasang (`eyd/scripts/periksa.py`; atau set `SKILL_EYD=<jalur>`).

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
- `gaya_gambar.py`: palet per buku (`PALET_BUKU*`), `LEBAR` (B5 = 5,2 inci), jalur fon `_FON`.
- `_bersama/preamble.tex` (dari `assets/preamble.tex`): warna seri, sampul, tanda air.
- `G-GAYA` memakai skill math-article bila terpasang (`SKILL_GAYA`), selain itu pemeriksa cadangan.

## Perbedaan dari harness proyek seri

- Konfigurasi proyek dipindah ke `konfig.json` (sebelumnya daftar penulis, nama buku `buku1-dasar`, `_bersama`, `lampiran-kode` tertanam di kode).
- Daftar penulis G-SITASI dibangun otomatis dari `pustaka.bib`.
- Gerbang baru: **G-LARANGAN** (nama teknik pengajaran dan kata terlarang lain), **G-ISTILAH** (istilah yang sudah diputuskan), **G-HALJUDUL** (tanpa `subtitle`, `date` ISO, "Draf revisi ke-N" di `date-format`).
- Fikstur baru `uji-buku/bablarangan.qmd`.
- Folder laporan dibuat otomatis; `penggalan.py` menghimpun semua folder buku yang punya `_quarto.yml` (bukan hanya `buku*`).
- `kemas_sumber.py` mengenali buku otomatis (folder dengan `_quarto.yml`; pasangan `kunci-<buku>`).

Diuji 2026-11-07: `uji_harness.sh` (9 fikstur gagal GAGAL, `babbaik` LULUS); `assets/templat-bab.qmd` dan `assets/templat-bab-kunci.qmd` LULUS pada proyek hasil `siapkan_proyek.py` (R 4.6, tanpa `--render`).
