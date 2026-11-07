# Skill `buku-ajar` (draf, 7 November 2026)

Skill Claude untuk menulis buku ajar berbahasa Indonesia (EYD V) di bidang statistika, sains data, matematika terapan, dan komputasi dengan alur multi-agen, gerbang mutu yang dapat dieksekusi, dan loop ulasan independen. Disarikan dari proses nyata penulisan seri buku statistika Bayesian Achmad Syahrul Choir (Politeknik Statistika STIS): tiga buku induk, tiga buku kunci jawaban untuk pengajar, rancangan buku keempat, ±1.200 klaim berkutipan verbatim, dan puluhan keputusan gaya penulis yang ditegakkan harness.

## Isi

```
SKILL.md                     alur, peran, harness, loop, paralelisasi, kriteria selesai
agents/00–15                 orkestrator, perencana, perancang kerangka, peninjau literatur,
                             penulis, reviewer isi/rumus/bahasa/kode, editor,
                             pembaca pemula/menengah/mahir, pembuat kunci, penyunting soal,
                             pengaudit ilustrasi
references/                  aturan gaya dan tampilan, istilah, data dan sumber, harness dan
                             gerbang, loop kerja, kunci jawaban, ilustrasi, pelajaran proyek,
                             prinsip buku ajar (ringkasan) + kajian lengkap
assets/                      templat brief, rancangan rinci, kerangka bab, bab .qmd, bab kunci,
                             laporan ulasan, temuan soal, KEPUTUSAN-RANCANGAN, REVISI, STATUS;
                             _quarto.yml, preamble.tex, tikz-preamble.tex, konfig.json,
                             apa.csl, reference-b5.docx
scripts/                     harness.py (25 gerbang), referensi.py, penggalan.py,
                             uji_harness.sh + uji-buku/, gaya_gambar.py, catatan.lua,
                             bahasa-asing.lua, kemas_sumber.py, siapkan_proyek.py, README.md
```

## Perbedaan dengan `buku-praktikum`

`buku-praktikum` adalah skill umum yang baik untuk modul dan buku tunggal. `buku-ajar` mempertahankan gagasan terbaiknya (agen berkontrak, peninjau berkonteks bersih, gerbang, loop beranggaran, kode yang benar-benar dijalankan, penurunan langkah demi langkah) dan memperbaiki kekurangan yang tampak saat dipakai untuk seri buku sungguhan.

| Aspek | buku-praktikum | buku-ajar |
|---|---|---|
| Nama teknik pengajaran | Sokratik–Feynman diajarkan sebagai fitur naskah (latihan "jelaskan kembali", "pertanyaan Sokratik") | Hanya label internal; **dilarang di naskah** dan ditegakkan gerbang G-LARANGAN; gaya ditulis di brief sebagai deskripsi |
| Subjudul | tidak diatur | bukan kalimat tanya (G-JUDUL); pertanyaan di kalimat pertama prosa; 5W1H hanya daftar periksa perencanaan |
| Sitasi | dengan lokasi (`[@k, hlm. 212]`); buku besar klaim berupa tabel parafrase berstatus | **penulis–tahun tanpa lokasi**; subjek hanya penulis orang; registri JSON dengan **kutipan verbatim** yang dicocokkan ulang otomatis ke teks sumber, Rd, DESCRIPTION, `citation()`, atau hitung ulang (G-REFERENSI) |
| Angka di prosa | diisi dari keluaran setelah loop kode (penanda `[[...]]`) | **selalu R inline**; gerbang G-ANGKA menolak angka diketik; klaim "sama/tidak satu pun" dikunci `stopifnot` |
| Gambar | tidak diatur rinci | R → parquet → Python `gaya_gambar` (Python tidak menghitung, G-PYTHON); TikZ untuk DAG; judul ≤ 12 kata, panel (a)(b), Div catatan; gambar tidak mengambang |
| Gerbang | G0–G9 memeriksa keberadaan artefak tahap | 25 gerbang memeriksa isi bab, hasil rajut, dan hasil render (tepi halaman, pemenggalan EYD V, nama tidak dipenggal, Word) |
| Uji harness | tidak ada | fikstur gagal/lulus `uji-buku/` + `uji_harness.sh`; setiap gerbang baru wajib berfikstur |
| Keputusan penulis | dicatat di STATE | `KEPUTUSAN-RANCANGAN.md` bertanggal → gerbang/konfig baru → **audit semua buku** → putaran sunting → "Draf revisi ke-N" + `REVISI.md` (loop D) |
| Pembaca uji | satu pembaca simulasi | **tiga tingkat** (pemula, menengah yang menjalankan kode, mahir) + reviewer isi, rumus, bahasa, kode, dan **editor** yang memutuskan temuan |
| Seri buku | tidak ada | peta "satu topik, satu pemilik", kotak "Ingat dari Buku N, Bab M", jembatan istilah antarbuku |
| Kunci jawaban | tidak ada | buku terpisah untuk pengajar: pembahasan langkah demi langkah, rubrik 10 poin, temuan soal → perbaikan soal induk oleh agen terpisah (loop C) |
| Data | sumber data umum | urutan riil → sintetis paket → simulasi; status dari Rd; peta berlisensi; tahun data mengikuti peta; batasan data di prakata |
| Multi-agen | paralel bila tidak bergantung | satu agen per berkas, `flock` untuk registri, render berurutan, pemulihan setelah kontainer dimulai ulang, titik simpan git |
| Tampilan cetak | `_quarto.yml` dasar | B5, paragraf menjorok tanpa spasi, tanda air DRAF, tanpa subjudul buku, "Draf revisi ke-N", tanpa luapan tepi (G-TEPI) |
| Dasar pedagogi | kajian Sokratik–Feynman | kajian prinsip buku ajar lebih luas (beban kognitif, contoh terselesaikan, pemudaran, pembaca berlapis, Permendikbudristek 22/2022 terverifikasi) dengan daftar periksa 35 butir yang dipetakan ke agen |
| Pelajaran | — | `pelajaran-proyek.md`: kesalahan berulang dari ulasan nyata (narasi gambar tak cocok, ambang tipis, kotak Ingat menumpuk istilah, label kategori tak sesuai Rd, …) |

Yang **tidak** diambil dari buku-praktikum: `cek_gerbang.py` (gerbang artefak), `init_naskah.py` (diganti `siapkan_proyek.py`), glosarium CSV (diganti `keputusan-istilah.md` per buku). `cek_turunan.py` tetap dirujuk untuk reviewer rumus bila buku-praktikum terpasang.

## Memasang

1. Salin folder ini ke direktori skill Claude, mis. `~/.claude/skills/buku-ajar/` (atau unggah sebagai skill di claude.ai). Jangan menimpa skill `buku-praktikum`; keduanya dapat berdampingan.
2. Pastikan skill **eyd** terpasang (wajib untuk G-EYD) dan, dianjurkan, **humanizer-id** dan **dataviz**.
3. Siapkan proyek:

   ```bash
   python3 ~/.claude/skills/buku-ajar/scripts/siapkan_proyek.py \
       --proyek ~/sumber/seri-baru --buku buku1 --judul "Judul Buku" --penulis "Nama Penulis"
   cd ~/sumber/seri-baru && bash harness/uji_harness.sh
   ```

4. Perangkat: R (knitr, arrow, paket bab), Quarto ≥ 1.6, TeX Live/XeLaTeX (TeX Gyre, DejaVu Sans Mono, `indentfirst`, `draftwatermark`), Python 3 (pandas, pyarrow, matplotlib, seaborn, Sastrawi), poppler (`pdftotext`). Rincian dan variabel yang perlu disesuaikan: `scripts/README.md`.

## Status draf

- Diuji 2026-11-07: `uji_harness.sh` (9 fikstur gagal, 1 lulus) dan templat bab/kunci LULUS harness pada proyek baru hasil `siapkan_proyek.py` (tanpa render). Render penuh dengan templat belum diuji di proyek baru.
- `references/kajian-prinsip-buku-ajar.md` sebagian bersumber sekunder ([S]); Permendikbudristek 22/2022 sudah diverifikasi ke teks peraturan.
- Uji perilaku skill-creator iterasi 1 (2026-11-07, `evals/`): dua kasus, masing-masing dengan dan tanpa skill.

  | Kasus | Dengan skill | Tanpa skill |
  |---|---|---|
  | `tulis-bab-binomial` (proyek baru, satu bab) | 6/6 | 5/6 |
  | `audit-bab-bermasalah` (audit dan perbaikan bab bercacat) | 9/9 | 6/9 |
  | Rata-rata waktu / token | 343 s / 171,8 ribu | 127 s / 77,4 ribu |

  Butir yang hanya lulus dengan skill: subjudul bukan kalimat tanya, tidak ada angka hasil yang diketik (termasuk di `fig-alt` dan kunci), dan penilaian dari tiga tingkat pembaca. Ulasan dalam uji dijalankan berurutan oleh satu agen ("tanpa isolasi konteks") karena subagen uji tidak punya alat subagen.
- Deskripsi skill dipendekkan menjadi 912 karakter agar lolos validasi (batas 1.024); pemicuannya belum dioptimalkan dengan evaluasi pemicuan skill-creator.
