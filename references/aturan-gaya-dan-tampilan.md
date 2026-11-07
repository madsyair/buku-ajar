# Aturan gaya dan tampilan

Aturan di berkas ini disarikan dari keputusan penulis yang berlaku umum pada seri buku statistika Bayesian (Choir, 2026) dan menjadi **bawaan** skill. Setiap proyek baru menyalinnya ke `KEPUTUSAN-RANCANGAN.md` proyek (lihat `assets/templat-KEPUTUSAN-RANCANGAN.md`); bila penulis memutuskan lain, berkas proyek yang berlaku. Kolom "Gerbang" menyebut pemeriksa otomatis di `scripts/harness.py`; aturan tanpa gerbang diperiksa reviewer.

Daftar isi: 1 Prosa dan alur · 2 Judul dan subjudul · 3 Tabel dan gambar · 4 Rumus dan notasi · 5 Sitasi · 6 Angka dan kode · 7 Kotak dan struktur bab · 8 Tata letak cetak · 9 Bahasa (ringkas; rinci di skill eyd)

## 1. Prosa dan alur

| Aturan | Gerbang |
|---|---|
| Alur setiap subbab digerakkan oleh **pertanyaan wajar pembaca**. Pertanyaan itu ditulis sebagai kalimat tanya di kalimat pertama prosa subbab (atau tersirat di kalimat pembuka paragraf), lalu dijawab dengan penjelasan sederhana, analogi, dan contoh angka **sebelum** rumus. | reviewer isi, pembaca |
| Pola tiga langkah: **intuisi → rumus → interpretasi angka** dari kode buku sendiri. | reviewer isi |
| Setiap subbab harus dapat dijelaskan ulang oleh pembaca sasaran dalam 2–5 kalimat sederhana. Bila pembaca uji gagal, subbab ditulis ulang, bukan ditambah istilah. | pembaca |
| Nama teknik pengajaran (label internal skill: "Sokratik", "Feynman", "Socrates", "teknik Feynman", "pertanyaan Socrates") **tidak pernah** ditulis di naskah buku, di judul, di latihan, atau di berkas proyek buku. Teknik bekerja tanpa label. | G-LARANGAN |
| Contoh diambil dari **pengetahuan umum dan konteks Indonesia** (pengangguran, kemiskinan kabupaten, upah, harga beras, klaim asuransi, nilai ujian), dengan data yang statusnya disebut (lihat `data-dan-sumber.md`). | reviewer isi |
| Satu istilah baru, satu penjelasan utuh: arti dengan kata sehari-hari, alasan dibutuhkan, contoh angka atau analogi. Jangan menumpuk beberapa istilah baru dalam satu kalimat atau satu kotak. | pembaca, reviewer bahasa |
| Paragraf isi 2–6 kalimat; satu gagasan pokok; kalimat pertama terhubung ke paragraf sebelumnya. | G-PARAGRAF |
| Tanpa basa-basi dan kosakata khas tulisan mesin ("berikut ini", "perlu dicatat bahwa", "sangat", "krusial", "menyoroti", "mari kita", "pada dasarnya", "ternyata"). | G-SLOP, G-GAYA |
| Tanpa "di mana"/"dimana"/"yang mana" sebagai penghubung; pakai "yang", "tempat", atau pecah kalimat. | G-GAYA |
| Komentar meta tentang buku ("Pada bab ini kita akan…") diganti pernyataan isi. | G-SLOP |
| Klaim perbandingan ("sama", "lebih lebar", "kokoh", "tidak memuat nol") ditulis bersyarat pada angka atau dikunci dengan `stopifnot()` (lihat `pelajaran-proyek.md`). | reviewer kode |

## 2. Judul dan subjudul

| Aturan | Gerbang |
|---|---|
| Judul bab dan subjudul **bukan kalimat tanya** (tanpa "?"). Tulis frasa pernyataan; pertanyaannya pindah ke kalimat pertama prosa. | G-JUDUL |
| Judul bab: frasa nomina yang menamai topik/model, pola sejajar antarbab ("Model X untuk Y", "Regresi untuk Respons Biner"), kapital tiap kata kecuali kata tugas, ringkas. Contoh: "Pemilihan Prior", bukan "Memilih Prior"; "Model Beta–Binomial untuk Proporsi", bukan "Mengestimasi Proporsi: Model Beta–Binomial". | editor |
| Subjudul: huruf kapital hanya di awal (gaya kalimat), frasa, tanpa titik. Istilah asing di subjudul tetap miring. | editor |
| Subjudul baku bab (berlabel tetap): Tujuan belajar (kotak), Contoh utama, Ringkasan, Latihan. Subjudul enam langkah contoh utama `{.unnumbered}`. | editor |

## 3. Tabel dan gambar

| Aturan | Gerbang |
|---|---|
| **Judul tabel pendek**: satu frasa, maks. 12 kata, tanpa kalimat kedua, titik dua penjelas, atau titik koma. | G-JUDUL |
| **Judul gambar pendek**: judul utama maks. 12 kata, satu frasa. Gambar multipanel: "Judul: (a) frasa, (b) frasa", frasa panel maks. 6 kata. | G-JUDUL (`JUDUL_GAMBAR=1`) |
| Penjelasan (arti kolom, singkatan, satuan, sumber data, cara membaca, makna warna/garis, temuan) ditulis di **Div catatan** tepat di bawah tabel/gambar, minimal 2 kalimat: `::: {.catatan}` … `:::`. Filter `catatan.lua` menambahkan "*Catatan:*" dan mencetaknya kecil; jangan menulis "Catatan:" sendiri. | reviewer |
| Gambar berpanel banyak memanggil `label_panel(axes)` (gaya_gambar) setelah semua panel digambar; keterangan menyebut isi setiap huruf. Jangan memakai "kiri/kanan/atas/bawah", "panel kiri". | G-JUDUL |
| Rujukan panel di prosa ditulis `@fig-x(a)` (dirender "Gambar 3.2(a)"). | G-JUDUL |
| Diagram TikZ berbagian banyak juga diberi label (a), (b) di dalam gambar. | reviewer |
| Setiap gambar/tabel berlabel unik bersufiks bab (`fig-…-b3-02`), dirujuk di prosa **sebelum** muncul, dan narasinya cocok dengan yang tampak (hitung ciri yang disebut; jangan menebak dari kode). | G-RUJUKAN, reviewer isi |
| Angka di keterangan memakai `fig-cap: !expr` atau R inline di Div catatan; tidak diketik. | G-ANGKA |
| Gambar dan tabel **tidak mengambang**: `fig-pos: "H"`, `tbl-pos: "H"` di `_quarto.yml`, agar catatan tidak terpisah dari objeknya. Jangan mengatur `fig-pos` per chunk. | editor |
| Tabel dibangun dari objek R (`knitr::kable`, flextable), bukan diketik. Tabel lebar dipersempit (singkat judul kolom, kurangi digit, `tbl-colwidths`). | G-TEPI |
| Lebar gambar ≤ lebar blok teks (B5: 5,2 inci). | G-TEPI |

Contoh benar:

```
#| fig-cap: "Upah dan lama sekolah: (a) data, (b) garis posterior"

::: {.catatan}
Titik abu-abu adalah 534 pekerja CPS 1985 ... Garis hijau adalah 50 garis
dari posterior ...
:::
```

## 4. Rumus dan notasi

| Aturan | Gerbang |
|---|---|
| Kata **"persamaan" huruf kecil** di tengah kalimat ("… seperti pada persamaan 3.2"); kapital hanya di awal kalimat. Di Quarto: `crossref-eq-prefix: "persamaan"`; rujukan di awal kalimat ditulis `@Eq-…`. | G-PERSAMAAN |
| **Pemisah parameter distribusi**: bila salah satu parameter memuat koma desimal, pakai titik koma: Beta(18,85; 281,15), $\mathrm{N}(0;\ 0{,}5)$. Parameter bilangan bulat boleh koma: Beta(1, 1). Seragam dalam satu bab. | reviewer rumus |
| Desimal koma di prosa dan rumus (`0{,}5` dalam mode matematika agar tanpa spasi); kode tetap titik. | reviewer |
| Penurunan pendek dalam kotak `::: {.callout-note title="Penurunan"}`; langkah demi langkah dengan alasan; ditutup makna dan, bila mungkin, pemeriksaan angka. | reviewer rumus |
| Rumus tampilan yang terlalu lebar dipecah (`aligned`, `split`) atau ditulis ulang. | G-TEPI |
| Notasi ditetapkan sekali per buku (rancangan rinci) dan sama lintas buku seri; padanan notasi sumber disebut sekali bila berbeda. | reviewer rumus, editor |
| Tanda khusus ditulis karakter Unicode langsung di prosa (± bukan `$\pm$` yang menempel ke kode inline). | pembaca |

## 5. Sitasi

| Aturan | Gerbang |
|---|---|
| **Penulis–tahun tanpa lokasi**: `[@gelman2026]`, `[@a; @b]`, bukan `[@gelman2021, bag. 13.2]`. Lokasi (bab, halaman) hanya disimpan di registri klaim (`lokasi`). | G-SITASI |
| Bila penulis menjadi subjek kalimat, pakai **sitasi naratif** `@kunci` ("@gelman2026 menyebut …" → "Gelman dkk. (2026) menyebut …"). Jangan menulis nama manual plus sitasi kurung kunci yang sama. | G-SITASI |
| **Subjek pernyataan bersitasi hanya penulis orang.** Lembaga (BPS, Stan Development Team, R Core Team), manual, panduan, dokumentasi, halaman bantuan, *vignette*, situs, rilis, dan publikasi tidak dijadikan subjek ("Menurut Panduan X …", "BPS menyatakan …"): tulis faktanya langsung dengan sitasi kurung. Entri bib berpenulis lembaga tidak boleh disitasi naratif. | G-ATRIBUSI |
| Setiap kalimat bersitasi punya entri registri klaim dengan kutipan verbatim sumber yang dibuka (lihat `data-dan-sumber.md`). | G-REFERENSI |
| Dokumentasi Rd paket disitasi ke entri yang benar (`citation("paket")`), bukan ke artikel lain penulis paket. | reviewer isi |
| Rujukan ke buku lain dalam seri ditulis sebagai teks ("Buku 2, Bab 8"; "Buku 1 Subbab 4.3"), bukan `@sec-`, karena label lintas proyek Quarto tidak dikenal. | G-RUJUKAN |

## 6. Angka dan kode

| Aturan | Gerbang |
|---|---|
| Setiap angka hasil hitung di prosa, catatan, dan keterangan berasal dari **kode R inline** (`` `r angka(x, 3)` ``, `` `r persen(p)` ``). Bilangan bulat kecil tanpa desimal/ribuan/persen boleh diketik. Angka tetap yang sah (tingkat 95%, angka resmi yang dikutip) didaftarkan di `pengecualian.json` (`angka-tetap`) dengan alasan. | G-ANGKA |
| Komentar kode tidak menyerupai keluaran (`# 0.210 0.273`). | G-KELUARAN |
| Baris kode R ≤ 72 karakter, Python ≤ 79. | G-LEBAR-KODE |
| Keluaran tercetak ≤ 78 karakter per baris (`width = 70`, `print(…, digits =)`, pilih kolom, `strwrap(…, 70)`). | G-LEBAR-KELUARAN |
| Tidak ada peringatan, galat, repr objek, `NA/Inf/NaN` yang tercetak. `message: false` di setup; brms `refresh = 0, silent = 2`; keluaran `cat()` dibungkus `invisible(capture.output(...))`. | G-BOCOR |
| Gambar data: chunk R menulis `data-gambar/<buku>-babXX-*.parquet`; chunk Python (`echo: false`, `results: hide`) hanya membaca parquet dan menggambar dengan `gaya_gambar`. Python tidak menghitung (tanpa `numpy.random`, `scipy.stats`, `statsmodels`) dan tidak memakai objek `r.`. | G-PYTHON |
| Model mahal disimpan: `file = file.path("fit", "b3-XX-nama")`, `file_refit = "on_change"`, `seed` tetap, jalur relatif. | reviewer kode |
| Kode panjang (simulasi, penyusunan tabel, parquet) disembunyikan (`echo: false`) dan dirujuk: "kode lengkap ada di `lampiran-kode/<buku>/babXX.R`". | G-LAMPIRAN |
| Hindari mencetak `summary(fit)` utuh (panjang, berbahasa Inggris); cetak ringkasan terpilih. | editor |

## 7. Kotak dan struktur bab

Struktur bawaan setiap bab (sesuaikan di brief):

1. Judul `# Judul Bab {#sec-…}` dan chunk setup tersembunyi (`assets/templat-bab.qmd`).
2. Paragraf pembuka yang menjembatani bab sebelumnya dan menyebut pertanyaan bab.
3. Kotak **"Ingat dari Buku N, Bab M"** (`.callout-tip`): maks. satu paragraf, paling banyak dua per bab, nomor dan judul bab sumber benar. Isinya konsep yang diperlukan, **bukan** daftar istilah baru; istilah yang belum dikenal pembaca dijelaskan di prosa, bukan dipadatkan di kotak.
4. Kotak **Tujuan belajar** (`.callout-important`): 3–5 butir berawalan kata kerja terukur.
5. Isi per subbab; kotak **Penurunan** (`.callout-note`) untuk penurunan pendek.
6. **Contoh utama enam langkah** (`### … {.unnumbered}`): Pertanyaan dan data, Model, Hitung, Periksa, Interpretasikan, Uji kepekaan. Maks. ±40% bab.
7. **Ringkasan** (≤ 1 halaman), ditutup interpretasi bagi pembaca terapan (mis. ekonomi dan sosial).
8. **Latihan** empat jenis: Konseptual, Penurunan sederhana, Hitungan, Pemrograman; satu latihan "tiru alurnya" (enam langkah untuk data lain).
9. Kalimat penutup yang menunjuk skrip lampiran kode bab.

## 8. Tata letak cetak

| Aturan | Gerbang |
|---|---|
| **Tanpa luapan tepi**: tidak ada rumus, gambar, tabel, kode, keluaran, atau teks yang melewati tepi lebih dari 3 pt (Overfull hbox). Perlu `latex-clean: false` dan `keep-tex: true`. | G-TEPI |
| **Nama tidak dipenggal**: nama orang dan nama diri (Gelman, Bayes, Poisson, …) tidak terpenggal di akhir baris. `penggalan.py` membangkitkan daftar nama tanpa titik penggal. | G-PENGGALAN |
| Pemenggalan kata Indonesia sesuai EYD V (pola hyph-id dikoreksi kamus Sastrawi); istilah asing miring ditandai bahasa Inggris (`bahasa-asing.lua`). Word: pemenggalan otomatis aktif, bahasa id-ID. | G-PENGGALAN |
| Blok kode dan tabel pendek tidak terbelah halaman: `\needspace{N\baselineskip}` sebelum chunk bila perlu. | editor |
| Render buku hanya **berurutan**, satu buku sekali jalan, setelah semua agen bab selesai (lihat orkestrator). | — |
| Keluaran PDF dan Word dirender dalam satu `quarto render` (render terpisah menghapus berkas format pertama). | G-RENDER |

### Halaman judul, draf, dan paragraf (keputusan penulis 2026-11-07)

| Aturan | Gerbang |
|---|---|
| **Tanpa subjudul buku**: judul saja, di `_quarto.yml` (tanpa `subtitle:`) maupun di sampul. | G-HALJUDUL |
| Halaman judul draf memuat **"Draf revisi ke-N"** sebelum tanggal, lewat `date-format: "[Draf revisi ke-N · ]D MMMM YYYY"` dengan `date: "YYYY-MM-DD"`. Jangan menulis teks di kolom `date` (Quarto mencetak "Invalid Date"). | G-HALJUDUL (`DRAF=1`; `DRAF=0` untuk versi terbit) |
| Satu revisi = satu putaran perubahan menyeluruh atas buku yang sudah lengkap (bukan penambahan bab). Setiap kenaikan N dicatat di **`REVISI.md`** akar proyek: buku, revisi, tanggal, isi putaran. | editor |
| **Tanda air DRAF** di setiap halaman PDF selama draf: `\usepackage{draftwatermark}` dan `\DraftwatermarkOptions{text={DRAF}, fontsize=120pt, angle=45, color={gray!14}}` di preamble bersama; dihapus untuk versi terbit. | editor |
| Nama penulis di halaman judul dan sampul **tanpa gelar akademis** (Permendikbudristek 22/2022, Lampiran II hlm. 55). Anatomi buku (halaman hak cipta dengan fon yang dipakai, prakata berisi tujuan dan pembaca sasaran, petunjuk penggunaan, daftar pustaka, glosarium/indeks, riwayat penulis) diperiksa sekali per buku (kajian butir 33–34). | editor |
| **Paragraf menjorok** di baris pertama, **tanpa spasi antarparagraf**, termasuk paragraf pertama setelah judul. PDF: `indent: true` di format pdf `_quarto.yml`; preamble `\usepackage{indentfirst}`, `\setlength{\parindent}{1.5em}`, `\setlength{\parskip}{0pt plus 1pt}`. Word: gaya *Body Text* dan *First Paragraph* di `reference-doc` diberi indentasi baris pertama 0,75 cm dan spasi sebelum/sesudah 0. | editor (periksa PDF dan Word) |

## 9. Bahasa (ringkas)

Rinci di skill **eyd** (`references/kalimat-efektif.md`, `kata-hubung.md`, `inventaris-kesalahan.md`) dan `istilah-statistika.md`.

- Setiap kalimat **utuh**: subjek dan predikat jelas; tanpa subjek berkata depan ("Dalam bab ini membahas …"); tanpa anak kalimat berdiri sendiri (kalimat diawali "Sehingga", "Karena", "Yang"); tanpa konjungsi ganda ("Meskipun … tetapi").
- **Koma konjungsi** (EYD V B.2–B.5, B.13): **tanpa** koma sebelum penghubung subordinatif bila induk mendahului anak kalimat (*sehingga, karena, sebab, agar, supaya, bahwa, jika, bila, apabila, kalau, meskipun, walaupun, ketika, setelah, sebelum, sejak, selama*), termasuk bila kalimat diawali anak kalimat lain. **Dengan** koma sebelum *tetapi, melainkan, sedangkan, padahal*; sesudah anak kalimat yang mendahului induk; sesudah penghubung antarkalimat (*Akibatnya,* *Oleh karena itu,* *Namun,*); sebagai penutup aposisi/sisipan. ", karena itu" di tengah kalimat → pecah kalimat. *Sehingga* tidak mengawali kalimat. Kalimat > 30 kata dipecah. Gerbang: G-KONJUNGSI; pengecualian sah per kalimat di `pengecualian.json` (`konjungsi-abaikan`), dinilai satu per satu, tidak dihapus massal.
- Istilah asing tanpa padanan lazim dicetak miring dan dijelaskan pada kemunculan pertama **di setiap bab**; verba tidak dibuat hibrida ("di-*fit*" → "dicocokkan"); akhiran pada istilah asing memakai tanda hubung (*shrinkage*-nya).
