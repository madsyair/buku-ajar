# Data dan sumber

Dua janji buku ajar: setiap angka dapat dihitung ulang, dan setiap pernyataan bersumber dapat ditelusuri ke teks yang benar-benar dibuka. Berkas ini mengatur keduanya.

## A. Data contoh

### Urutan pilihan data (keputusan penulis 2026-11-07, bawaan skill)

1. **Data riil**: paket R di CRAN, lembaga statistik (BPS), repositori terbuka (UCI), berkas yang diunggah penulis.
2. Bila data riil tidak cocok (struktur tidak sesuai, tidak tersedia, atau contoh perlu nilai parameter sebenarnya untuk validasi): **data simulasi/sintetis yang sudah ada di paket** (sebut statusnya persis seperti dokumentasi Rd).
3. Bila tetap tidak cocok: **bangkitkan sendiri** dengan fungsi pembangkit yang ditampilkan atau dilampirkan dan `set.seed()` tetap; nilai parameter sebenarnya dilaporkan berdampingan dengan posterior.

Data simulasi dipakai terutama untuk **validasi** (parameter sebenarnya diketahui, berfungsi sebagai kunci jawaban); penerapan memakai data riil.

### Status data selalu disebut

Saat data diperkenalkan, naskah menyebut status, asal, dan cakupannya dalam satu kalimat: "data riil survei angkatan kerja AS Mei 1985 dari paket AER", "data sintetis bawaan paket sae", "data simulasi buku ini dengan parameter sebenarnya diketahui", "data simulasi berbasis peta". Jangan pernah menyajikan data simulasi sebagai angka resmi, dan **jangan mengarang angka lembaga** (BPS atau lainnya).

### Memeriksa data sebelum dipakai

Untuk setiap dataset, perancang/penulis memuatnya (mis. Rscript) dan mencatat di rancangan rinci: paket dan versi, dimensi, peubah kunci, nilai hilang, **status riil/sintetis dari kutipan Rd**, bab pemakai, kunci sitasi (`citation("paket")`). Dataset yang ditolak dicatat beserta alasannya (sintetis menurut Rd, asal tidak dinyatakan, gagal dipasang, status tidak dapat dipastikan karena paket lain menyebut data identik sintetis).

Label kategori, satuan, dan arti peubah ditulis **sesuai dokumentasi Rd** (dan sesuai bunyi soal latihan). Jangan menebak arti kode faktor.

### Data lembaga dan peta

- Data BPS dipakai bila berkasnya tersedia di proyek (diunggah penulis atau diunduh lewat jalur resmi); simpan di `<buku>/data/bps/` dengan `SUMBER.md` (judul publikasi, tanggal rilis, halaman, URL, tanggal akses). Situs yang menolak akses otomatis tidak dijadikan alasan mengarang angka.
- Data repositori terbuka (UCI, dll.) diunduh sekali ke `<buku>/data/<repo>/<nama>/` bersama `SUMBER.md` (URL, tanggal unduh, DOI, lisensi). Bab membaca salinan lokal, bukan URL.
- Peta: pakai batas wilayah berlisensi terbuka; **tahun data mengikuti tahun peta** (mis. peta 34 provinsi → data sebelum pemekaran). Data dan peta tidak digabung lintas pembagian wilayah berbeda kecuali penggabungan itu dijelaskan; agregasi hanya untuk besaran yang dapat dijumlahkan, rasio dibobot penyebutnya.
- Bila data lembaga tidak tersedia (tingkat wilayah halus, galat baku), boleh **simulasi berbasis peta** (poligon, ketetanggaan, luas, hierarki wilayah) dengan parameter eksplisit dan, bila mungkin, dikalibrasi ke angka agregat resmi; selalu disebut "data simulasi berbasis peta".
- Data contoh bawaan paket yang tampak seperti data wilayah nyata (mis. matriks ketetanggaan contoh) diperiksa dokumentasinya; sebut apa adanya ("matriks contoh 5 × 5 untuk data simulasi paket, bukan peta provinsi").

### Data yang diketik dari artikel

Data yang hanya tersedia sebagai tabel di artikel atau buku diketik ulang, lalu **dicocokkan sel demi sel** dengan gambar halaman PDF (bukan dengan teks konversi, yang sering menggeser kolom). Hasilnya disimpan sebagai berkas data (`<buku>/data/<sumber>/<nama>.csv`) bersama `SUMBER.md`: kunci sitasi, halaman dan nomor tabel, tanggal pengetikan, dan catatan pencocokan. Bab membaca berkas itu, bukan angka yang diketik di chunk. Contoh seri: data 23 rumah sakit Datta dkk.

### Batasan data di prakata

Setiap buku memuat subbagian prakata **"Data yang digunakan dan batasannya"**: jenis data (riil, sintetis paket, simulasi), alasan memakai simulasi, data lembaga yang belum dapat dipakai dan sebabnya, dan rujukan ke lampiran **Sumber Data** (daftar lengkap per bab: paket dan versi, sumber asli, status, lisensi, tanggal unduh). Lampiran ditulis setelah bab terakhir.

## B. Sumber dan registri klaim

### Sumber yang boleh disitasi

Hanya sumber yang **teksnya dapat dibuka dan dicocokkan**:

- teks lokal di `harness/sumber/<berkas>.md` (konversi PDF buku/artikel, dengan penanda `<!-- Page N -->` bila ada). Bila ada konversi lain dari buku yang sama (mis. unggahan baru yang lebih rapi untuk tahap gaya, tetapi tanpa penanda halaman atau dengan angka tabel hilang), simpan sebagai sumber kedua `harness/sumber/versi2/<berkas>.md` dengan baris kepala asal dan tanggal; jangan timpa sumber utama yang lebih lengkap;
- dokumentasi paket R terpasang (Rd, DESCRIPTION, `citation()`);
- halaman web yang dibuka saat menulis (dicatat URL, tanggal akses, kutipan verbatim);
- hitungan ulang (ekspresi R yang hasilnya dibandingkan dengan angka sumber).

Sumber yang tidak dapat dibuka **tidak disitasi** dan isinya tidak disebut seolah dikutip. Peninjau literatur menyusun daftar **sumber yang perlu diunggah penulis** (judul, alasan, bab yang membutuhkan) alih-alih mengarang.

Baris pertama setiap `harness/sumber/<kunci>.md` adalah komentar asal: berkas PDF asal, tanggal konversi, cara konversi, dan **pemetaan halaman PDF → halaman terbit** (mis. `<!-- asal: gelman2013.pdf; pymupdf4llm 2026-11-20; hlm. terbit = hlm. PDF − 14 -->`). Setiap halaman ditandai `<!-- Page n -->`. Pemetaan ini yang dipakai untuk lokasi klaim dan lokator sitasi, karena halaman PDF dan halaman terbit jarang sama. Versi lain buku yang sama (pracetak arXiv lawan versi terbit, bab lepas lawan buku lengkap) mengikuti aturan `versi2/` di atas.

### Daftar unggah

Daftar sumber yang perlu diunggah penulis (`naskah/sumber-perlu-diunggah.md`; di seri asal `harness/daftar-unggah.md`) terdiri atas empat tabel dan diperbarui setiap kali sumber masuk:

| Tabel | Isi |
|---|---|
| A | prioritas: dibutuhkan bab yang sedang atau akan ditulis |
| B | opsional: memperkaya, tetapi bab dapat ditulis tanpanya |
| C | bukti sementara hanya dari web atau sumber sekunder; perlu teks primer sebelum disitasi |
| D | tidak perlu lagi (sudah ada, diganti sumber lain), dengan alasannya |

Setiap baris: judul, alasan, bab yang membutuhkan, cara memperoleh. Setiap laporan bab dan laporan orkestrator kepada penulis **menyebut sumber [PERLU UNGGAH]**, juga bila daftarnya kosong (permintaan penulis seri, 2026-11-20).

### Wiki referensi dan konversi PDF

Bila banyak sumber diunggah sekaligus (seri asal: 18 buku dan 11 artikel), sumber masuk lewat **wiki referensi** (pola Karpathy LLM Wiki; skill karpathy-llm-wiki bila terpasang) sebelum disalin ke `harness/sumber/`:

- `raw/`: teks lengkap setiap sumber dengan penanda `[hlm. PDF n]`;
- `wiki/`: satu ringkasan per sumber dengan bagian "Bahan yang bisa memperkaya seri" (bab sasaran dan halaman), artikel konsep lintas sumber, `index.md`, dan `log.md`.

Wiki menjadi masukan kajian celah (`loop-kerja.md`, "Tambahan dari referensi baru dan bab yang dikunci") dan audit istilah (hitungan pemakaian istilah di referensi). Wiki bukan bukti klaim; bukti tetap kutipan verbatim dari `harness/sumber/`.

**Urutan konversi PDF** (berhenti pada cara pertama yang menghasilkan teks bersih):

1. **pymupdf4llm** tanpa OCR (`use_ocr=False`) untuk PDF yang berlapis teks;
2. **`pdftotext` tanpa `-layout`** untuk PDF dengan lapisan OCR lama penerbit, agar dua kolom terbaca berurutan;
3. **Tesseract** (lewat PyMuPDF, pixmap RGB; pixmap abu-abu menghasilkan teks kosong) untuk pindaian; halaman yang memuat dua halaman buku per lembar dipotong menjadi setengah kiri dan kanan sebelum OCR.

**Rumus tidak diambil dari teks konversi**: rumus sering rusak di ketiga cara. Untuk rumus yang **dipakai** di naskah atau di registri saja, render gambar halamannya (mis. `alat/render_halaman.py`), transkripsikan ke LaTeX, cocokkan balik dengan teks `raw/`, dan beri catatan "(transkripsi dari gambar hlm. PDF n)" di salinan sumber. Contoh seri: Jaccard berupa pindaian dua halaman per lembar.

Urutan prioritas jenis sumber (dari buku-praktikum, tetap berlaku): buku teks dan monograf penerbit akademik; artikel bertelaah; dokumentasi resmi perangkat lunak (untuk perilaku fungsi, bukan teori); publikasi lembaga resmi (data, definisi); pracetak bila tidak ada padanan, dengan catatan. Draf buku boleh disitasi bila penulis memutuskan, dengan entri pustaka yang menandainya sebagai draf.

### Registri klaim (`harness/klaim.json`)

Satu daftar JSON untuk seluruh proyek; setiap entri satu klaim pada satu kalimat:

```json
{
  "bab": "buku3/bab02",
  "kunci": "gelman2026",
  "penanda": "lemah atau kuatnya prior bukan sifat prior itu saja",
  "bukti": [
    {"jenis": "berkas", "berkas": "bayesian-workflow-buku.md",
     "lokasi": "bag. 5.9",
     "kutipan": "whether a prior is weakly informative depends on the question being asked"}
  ]
}
```

- `bab`: id bab (`<folder-buku>/<bab>`; lihat `id_bab` di harness).
- `penanda`: potongan teks **unik** dari baris bersitasi, persis seperti di `.qmd`, tanpa kode inline. Bila kalimat diubah, penanda diperbarui; kutipan bukti tidak diubah. Ini termasuk perubahan tanda miring istilah asing (mis. odds → `*odds*`) dan pemindahan kunci bab saat pemaduan buku multidisiplin (`<buku>/babXX-<kode>` → `<buku>/babXX`).
- `bukti[].jenis` dan medan wajib:

| Jenis | Medan | Diperiksa ulang harness |
|---|---|---|
| `berkas` | `berkas`, `lokasi`, `kutipan` | kutipan dicari di `harness/sumber/<berkas>` setelah normalisasi (ligatur, petik lengkung, pemenggalan akhir baris); bila tidak ditemukan, di versi kedua `harness/sumber/versi2/<berkas>`; laporan menyebut versi yang cocok (`[utama]` atau `[versi kedua]`) |
| `rd` | `paket`, `topik`, `kutipan` | dicari di `tools::Rd2txt` |
| `deskripsi` | `paket`, `kutipan` | DESCRIPTION paket |
| `citation` | `kutipan` | keluaran `citation()` |
| `hitung` | `kode`, `nilai_sumber`, `toleransi` | ekspresi R dijalankan, dibandingkan dengan angka sumber |
| `web` | `url`, `diakses`, `kutipan` | tidak dapat diulang luring; dicatat sebagai bukti manual |

- **Kutipan verbatim**: salin dari sumber yang dibuka; cek dengan `grep -F` sebelum dicatat. Parafrase di naskah harus setia pada kutipan; jangan menambah isi yang tidak ada.
- Klaim yang tidak dapat dibuktikan: hapus, atau ubah menjadi pernyataan tentang hasil hitung kode buku sendiri.

### Registri identitas (`harness/referensi.json`)

Per kunci bib: `identitas` (DOI/ISBN/URL) dan daftar `verifikasi` (`cara`, `sumber`, `tanggal`, `hasil`). Setiap entri `pustaka.bib` yang disitasi wajib punya DOI, ISBN, atau URL, dan entri `referensi.json` yang terverifikasi (halaman penerbit, katalog perpustakaan, `citation()`). Entri bib tidak disusun dari ingatan.

### Menulis registri secara aman

`klaim.json` dan `pengecualian.json` dipakai bersama semua agen. Penulisan **hanya** lewat kunci berkas:

```bash
flock <scratchpad>/klaim.lock python3 tambah_klaim.py   # baca, ganti entri bab sendiri, tulis ulang
```

Skrip membaca berkas, menambah/mengganti **entri bab sendiri saja**, lalu menulis ulang dengan `json.dump(..., ensure_ascii=False, indent=1)`. Jangan menyunting entri bab atau buku lain. Templat skrip ada di `harness-dan-gerbang.md`.

### Sitasi data dan paket

Paket yang datanya dipakai disitasi dari `citation("paket")` (entri bib + `referensi.json`). Dataset repositori disitasi dengan DOI dari halaman dataset. Rilis lembaga disitasi dengan entri berpenulis lembaga (hanya sitasi kurung).

**Konflik kepentingan.** Untuk setiap paket yang dipakai, cocokkan `Author`/`Maintainer` di DESCRIPTION dengan penulis buku. Bila penulis adalah pembuat atau pemelihara paket, tulis satu kalimat pengungkapan (mis. "Penulis buku ini adalah pembuat dan pemelihara paket X.") di tempat paket pertama dipakai atau di prakata, catat bukti DESCRIPTION (jenis `description`) di registri klaim, dan pastikan jalur alternatif tanpa paket itu tetap lengkap.
