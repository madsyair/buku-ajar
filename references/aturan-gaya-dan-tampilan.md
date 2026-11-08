# Aturan gaya dan tampilan

Aturan di berkas ini disarikan dari keputusan penulis yang berlaku umum pada seri buku statistika Bayesian (Choir, 2026) dan menjadi **bawaan** skill. Setiap proyek baru menyalinnya ke `KEPUTUSAN-RANCANGAN.md` proyek (lihat `assets/templat-KEPUTUSAN-RANCANGAN.md`); bila penulis memutuskan lain, berkas proyek yang berlaku. Kolom "Gerbang" menyebut pemeriksa otomatis di `scripts/harness.py`; aturan tanpa gerbang diperiksa reviewer.

Daftar isi: 1 Prosa dan alur · 2 Judul dan subjudul · 3 Tabel dan gambar · 4 Rumus dan notasi · 5 Sitasi · 6 Angka dan kode · 7 Kotak dan struktur bab · 8 Tata letak cetak (termasuk halaman judul, anatomi buku, huruf dan templat penerbit, ukuran buku, gaya Word, rumus di Word) · 9 Bahasa (ringkas; rinci di skill eyd)

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
| Lebar gambar ≤ lebar blok lebar (B5: 5,2 inci = 132 mm; blok lebar 140 mm, lihat bagian 8, "Tipografi"). | G-TEPI |

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
| **Logaritma natural ditulis ln** di prosa, rumus (`\ln`), tabel (judul kolom tampilan lewat `col.names`, nama variabel kode tetap), gambar, dan glosarium; **kode R/Stan dan keluarannya tetap `log`**. Basis lain `\log_{10}`, `\log_2`. Kemunculan pertama per buku induk diberi paragraf penjelas: ln di naskah; `log()` di R/Stan sudah logaritma natural; basis lain `log10()`, `log2()`, `log(x, base = b)`. Kata yang bukan logaritma (logit, logistik, katalog, log LaTeX) tidak diubah. Rincian: `istilah-statistika.md`. | G-LN (rumus prosa, keterangan); reviewer rumus (prosa, tabel, gambar) |
| **Periksa bentrok simbol lintas bab dan buku sebelum memilih notasi**: π konstanta (distribusi stasioner memakai ω), $e$ bilangan Euler, huruf parameter distribusi (estimasi $\hat\theta$, bukan $a$ yang bentrok dengan Beta($a$, $b$) dan bukan $d$ yang bentrok dengan $d\theta$); satu simbol satu arti dalam satu bab. | reviewer rumus, pembaca pemula, editor |
| Inti penurunan yang dipakai teks inti, Ringkasan, tujuan belajar, atau latihan ditulis satu atau dua kalimat di teks inti; kotak Penurunan hanya rinciannya (pola temuan pembaca pemula yang paling sering). | pembaca pemula |

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
| Baris kode R ≤ 72 karakter, Python ≤ 79 (`batas_kode`, `batas_kode_python` di `konfig.json`; ukuran buku kecil: subbab "Ukuran buku"). | G-LEBAR-KODE |
| Keluaran tercetak ≤ 78 karakter per baris (`batas_keluaran`; `huruf.py` menulis `options(width = batas_keluaran − 3)` ke `<buku>/.Rprofile`; `print(…, digits =)`, pilih kolom, `strwrap(…, 70)`). | G-LEBAR-KELUARAN |
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
| **Daftar isi dan rujukan stabil**: `latex-min-runs: 4` di format pdf `_quarto.yml` (Quarto tidak mengulang LuaLaTeX untuk "Rerun to correct this" dari `lastpage` sehingga daftar isi tertinggal satu putaran: Indeks hilang, nomor halaman salah). Log akhir tanpa "Rerun to correct", "Label(s) may have changed", "Rerun to get … right", dan label ganda. | G-LOG |
| **Tanpa label ganda dari tabel panjang**: keterangan `longtable` Pandoc ada di `\endhead` dan disalin ke setiap halaman lanjutan beserta `\label`-nya; `preamble.tex` mendefinisikan ulang `\endhead` sehingga salinan untuk halaman lanjutan dibersihkan dari `\write` dan anchor (LuaTeX). Keterangan tetap diulang. | G-LOG |
| **Tanpa baris yatim dan janda**: `\widowpenalty`, `\clubpenalty`, `\displaywidowpenalty` 10000 di `preamble.tex` (Permendikbudristek 22/2022, Lampiran III). | editor |

### Halaman judul, draf, dan paragraf (keputusan penulis 2026-11-07)

| Aturan | Gerbang |
|---|---|
| **Tanpa subjudul buku**: judul saja, di `_quarto.yml` (tanpa `subtitle:`) maupun di sampul. | G-HALJUDUL |
| Halaman judul draf memuat **"Draf revisi ke-N"** sebelum tanggal, lewat `date-format: "[Draf revisi ke-N · ]D MMMM YYYY"` dengan `date: "YYYY-MM-DD"`. Jangan menulis teks di kolom `date` (Quarto mencetak "Invalid Date"). | G-HALJUDUL (`DRAF=1`; `DRAF=0` untuk versi terbit) |
| Satu revisi = satu putaran perubahan menyeluruh atas buku yang sudah lengkap (bukan penambahan bab). Setiap kenaikan N dicatat di **`REVISI.md`** akar proyek: buku, revisi, tanggal, isi putaran. | editor |
| **Tanda air DRAF** di setiap halaman PDF selama draf: `\usepackage{draftwatermark}` dan `\DraftwatermarkOptions{text={DRAF}, fontsize=120pt, angle=45, color={gray!14}}` di preamble bersama; dihapus untuk versi terbit. | editor |
| Nama penulis di halaman judul dan sampul **tanpa gelar akademis** (Permendikbudristek 22/2022, Lampiran II hlm. 55). Anatomi buku (halaman hak cipta dengan fon yang dipakai, prakata berisi tujuan dan pembaca sasaran, petunjuk penggunaan, daftar pustaka, glosarium/indeks, riwayat penulis) diperiksa sekali per buku (kajian butir 33–34). | editor |
| **Paragraf menjorok** di baris pertama, **tanpa spasi antarparagraf**, termasuk paragraf pertama setelah judul. PDF: `indent: true` di format pdf `_quarto.yml`; preamble `\usepackage{indentfirst}`, `\setlength{\parindent}{1.5em}`, `\setlength{\parskip}{0pt plus 1pt}`. Word: gaya *Body Text* dan *First Paragraph* di `reference-doc` diberi indentasi baris pertama 0,75 cm dan spasi sebelum/sesudah 0. | editor (periksa PDF dan Word) |

### Anatomi buku (keputusan penulis seri, dicatat 2026-11-07)

| Aturan | Gerbang |
|---|---|
| Setiap buku (induk dan kunci) punya **halaman hak cipta**: judul, penulis, penerbit, tahun, ISBN, edisi/revisi, fon yang dipakai **beserta lisensinya** (Libertinus: SIL Open Font License 1.1), lisensi kode. Data yang belum ada ditulis **"belum ditetapkan"**, tidak dikarang (mis. "ISBN: belum ditetapkan"). Templat PDF: `assets/hak-cipta.tex` (`\halamanhakcipta`, dipanggil lewat `include-before-body`); Word: versi teks di awal `index.qmd`. | editor |
| **Pengungkapan konflik kepentingan**: bila penulis buku adalah pembuat atau pemelihara paket yang dipakai (cocokkan `Author`/`Maintainer` di DESCRIPTION dengan penulis di `_quarto.yml`), tulis **satu kalimat pengungkapan** di tempat paket pertama dipakai atau di prakata, dengan bukti DESCRIPTION di registri klaim. Jalur alternatif tanpa paket itu tetap lengkap (paket penulis cukup satu subbab "perangkat siap pakai"). | editor, penelaah pakar |
| Setiap buku punya **glosarium** (istilah dari `keputusan-istilah.md`, istilah asing miring dengan padanan atau penjelasan singkat) dan **indeks** di keluaran PDF (entri dari istilah glosarium dan nama metode; Word tidak wajib berindeks). | editor |
| **Riwayat hidup penulis** hanya berisi fakta dari sumber resmi (laman profil lembaga, SK, publikasi resmi) yang **salinannya disimpan** di proyek (mis. `naskah/sumber-riwayat/`, dengan tanggal unduh); fakta tanpa salinan sumber tidak ditulis. | editor |

### Tipografi (keputusan penulis seri, diterapkan dan diuji 2026-11-07)

Diterapkan di templat `assets/_quarto.yml`, `assets/preamble.tex`, `assets/doc-class.tex`, `assets/tikz-preamble.tex`, `assets/reference-b5.docx`, dan `scripts/gaya_gambar.py`. Kajian butir 34 (paling banyak dua *typeface*, 40–70 karakter per baris) dan butir 35 (aksesibilitas versi elektronik).

| Aturan | Gerbang |
|---|---|
| **Satu keluarga huruf: Libertinus** (SIL OFL, dibawa TeX Live). Teks dan judul Libertinus Serif 12 pt; `sansfont` juga Libertinus Serif sehingga tidak ada keluarga kedua; judul KOMA-Script memakai huruf teks tebal (`\setkomafont{disposition}{\normalfont\bfseries…}`), bukan sans. Rumus memakai Libertinus Math. Kode Libertinus Mono: `Scale=0.8` untuk kode sebaris; blok kode 7,2 pt (`\kodekecil`) dan keluaran 6,8 pt (`\keluarankecil`) pada B5, dihitung `huruf.py` dari lebar kolom. Glif yang tidak ada di Libertinus Mono (mis. huruf Yunani di kode) diambil dari Libertinus Serif/Math lewat `luaotfload.add_fallback` di `doc-class.tex`. Ini opsi `huruf: libertinus` (bawaan); opsi lain di subbab "Huruf dan templat penerbit". | G-HURUF (`pdffonts`: hanya Libertinus*) |
| Keluarga yang sama di luar teks: **gambar** matplotlib (`gaya_gambar.py` mendaftarkan OTF Libertinus Serif, juga untuk *mathtext*; ukuran huruf gambar sumbu 11, angka 9,5; disematkan sebagai **Type 3** karena Libertinus berupa OTF-CFF yang salah disematkan mode Type 42), **TikZ** knitr (pdfLaTeX: `libertinus` dan `libertinust1math` di `tikz-preamble.tex`), **sampul** (`\setmainfont{Libertinus Serif}`, `\setmathfont{Libertinus Math}`, dikompilasi LuaLaTeX), dan **Word** (`reference-b5.docx`: gaya teks, judul, dan tema Libertinus Serif, kode Libertinus Mono, rumus Libertinus Math; pembaca perlu memasang huruf Libertinus, bila tidak, Word memakai pengganti). Halaman hak cipta menyebut ketiga anggota keluarga. | editor |
| **Ikon kotak (*callout*) dimatikan** di PDF (`callout-icon: false`): ikon FontAwesome adalah huruf kedua. | editor |
| **Panjang baris teks inti 40–70 karakter** (Permendikbudristek 22/2022, Lampiran III). Pada B5 176 × 250 mm: Libertinus Serif 12 pt, margin dalam/luar 28 mm (**kolom prosa 120 mm**), atas 22 mm, bawah 24 mm, `linestretch` 1,1. Hasil seri: median 64, persentil-95 72 karakter (sebelumnya Pagella 10,5 pt, kolom 136 mm: 75/83); templat bab skill 2026-11-08: 60/69. Ukuran buku lain: subbab "Ukuran buku". | editor (ukur dari PDF) |
| **Semua blok di dalam kolom** (keputusan seri 2026-11-07): kode, keluaran R, gambar, tabel, dan rumus tampilan tidak melebihi kolom prosa (`\tambahlebar` 0 di `preamble.tex`; nilai positif menghidupkan lagi blok lebar). Ukuran mono dihitung `huruf.py` agar `batas_kode` (72) karakter kode di kotak kode (garis 2 pt, bantalan 1,4 + 0,6 mm) dan `batas_keluaran` (78) karakter keluaran muat utuh; `gaya_gambar.LEBAR` = lebar kolom. Di dalam kotak atau daftar blok tidak dilebarkan dan baris panjang dipenggal (fvextra `breaklines`). Rumus tampilan memakai `\everydisplay` (nomor persamaan di tepi blok lebar). Kode sebaris boleh patah sesudah `_ / . < > = [ ( ,` tanpa tanda hubung (penalti disisipkan di Lua). | G-TEPI, G-LEBAR-KODE, G-LEBAR-KELUARAN |
| **Cara ukur panjang baris**: `pdftotext -layout buku.pdf -` pada halaman isi bab, hanya baris prosa (buang baris kode, keluaran, rumus, tabel, judul, dan baris pendek akhir paragraf), lalu hitung **median** dan **persentil-95** jumlah karakter per baris. Median harus di 40–70; persentil-95 boleh sedikit di atas 70 karena baris renggang. Hasil dicatat di `KEPUTUSAN-RANCANGAN.md` proyek. | editor (sekali per buku) |
| **Mesin LuaLaTeX dan PDF bertag**: `pdf-engine: lualatex` (XeLaTeX tidak mendukung *tagging*); `\DocumentMetadata{testphase={phase-II,sec,toc,minipage,graphic,text}, pdfversion=1.7, lang=id-ID}` dipasang sebelum `\documentclass` lewat partial Quarto `_bersama/doc-class.tex` (`template-partials`). Judul KOMA-Script ditambal di `preamble.tex` agar subbab menjadi H2/H3 tertutup dan paragraf sesudahnya P; judul bab berkoma dibungkus kurung kurawal. Paket Debian **`texlive-luatex`** wajib (`lualatex-math`). | G-TAG |
| **Batasan TeX Live 2023** (LaTeX 2023-11): modul `float` bentrok dengan `[H]` (gambar tetap ditag Figure, tetapi keterangannya tidak dikaitkan); modul `block`/`bib` (daftar, kutipan, daftar pustaka) bentrok dengan fancyvrb dan tidak dipakai; isi `longtable` tidak ditag (`\tagstop`); isi blok kode tidak ditag; **teks alternatif gambar belum ada**. Hasilnya PDF bertag yang sah (Document–Sect–H1/H2/H3–P–Figure–TOC), **belum PDF/UA**. Kunci Quarto `pdf-standard`/`tagging=on` baru ada di LaTeX 2024; tagging penuh menunggu TeX Live 2024+. | editor (catat di halaman hak cipta atau prakata versi elektronik) |

### Huruf dan templat penerbit (2026-11-08)

Aturan "satu keluarga huruf" (Libertinus) adalah **gaya bawaan seri**. Bila naskah diserahkan ke penerbit, ikuti kelas dan huruf penerbit itu dan **jangan memakai huruf kustom**: halaman dukungan LaTeX Springer Nature meminta "Please do not use any custom fonts". Opsi skill di bawah hanya **meniru huruf** templat penerbit untuk draf dan uji tata letak. Konversi Quarto ke kelas penerbit (mis. `documentclass: krantz` atau `SNmono`) memerlukan berkas kelas dari penerbit/Overleaf. Kelas itu tidak ada di TeX Live, jadi mintalah ke editor.

Opsi dipilih dengan satu kunci di `harness/konfig.json`: `"huruf": "libertinus" | "springer" | "crc" | "stix"`. Sesudah mengubahnya, jalankan `python3 _bersama/huruf.py --proyek . --buku <buku>` (atau `siapkan_proyek.py --huruf …`). Skrip menulis ulang blok bertanda `>>> huruf` di `_quarto.yml`, `_bersama/doc-class.tex` (huruf cadangan), `preamble.tex` (mono dan cadangan teks lewat `\babelfont`), `tikz-preamble.tex`, dan `hak-cipta.tex` (`\serifon`: nama huruf beserta lisensinya). `gaya_gambar.py` membaca kunci yang sama.

| Penerbit | Kelas templat | Huruf templat | Paket TeX Live | Opsi skill | Sumber (diakses 2026-11-08) |
|---|---|---|---|---|---|
| Springer Nature (monografi) | `\documentclass[graybox,envcountchap,sectrefs]{SNmono}` (penerus svmono) | Times: `newtxtext` + `newtxmath[varvw]` ("selects Times Roman as basic font"); baris lama `mathptmx`/`helvet`/`courier` dikomentari | newtx (Type 1); OpenType setara: TeX Gyre Termes, Termes Math, Heros, Cursor | `springer` | overleaf.com/latex/templates/template-for-springer-monographs/jkmjvjrkqrpb, ditautkan dari springernature.com/gp/authors/campaigns/latex-author-support |
| Chapman & Hall/CRC | `\documentclass[krantz1,ChapterTOCs]{krantz}` | kelas tidak memuat paket huruf (opsi `times` dideklarasikan, tetapi tidak dipakai), jadi Computer Modern; contoh bookdown-crc memakai `sourcecodepro` (`scale=.8`) untuk kode | Latin Modern Roman/Math (OpenType CM), Source Code Pro | `crc` | overleaf.com/latex/templates/krantz-book-template/vfrsjggghjcd; `krantz.cls` (salinan diperiksa); github.com/yihui/bookdown-crc |
| Wiley | `\documentclass[11pt]{book}` + `Wiley-AuthoringTemplate.sty` | **tidak dapat dipastikan**: isi `.sty` tidak terbaca; Overleaf menyarankan berdiskusi dengan editor Wiley lebih dulu | — | sementara `springer` (Times); konfirmasikan ke editor | overleaf.com/latex/templates/book-template-for-wiley-authors/zbfhmmzbhhfr |
| (umum) | — | STIX Two Text/Math | `stix2-otf`, `stix2-type1` | `stix` | — |

Isi setiap opsi (`scripts/huruf.py`, `OPSI`). Skala mono dipilih agar lebar karakter efektif ≤ Libertinus Mono 0,8 (0,51 em) sehingga 72 karakter kode muat di kolom.

| Opsi | mainfont | sansfont | mathfont | monofont (Scale) | TikZ (pdfLaTeX) | Gambar matplotlib | Word bawaan |
|---|---|---|---|---|---|---|---|
| `libertinus` | Libertinus Serif | Libertinus Serif | Libertinus Math | Libertinus Mono (0,8) | `libertinus` + `libertinust1math` | Libertinus Serif; mathtext *rm* Libertinus Math | `reference-<ukuran>.docx` (Libertinus) |
| `springer` | TeX Gyre Termes | TeX Gyre Heros | TeX Gyre Termes Math | **TeX Gyre Cursor (0,85)**: klon Courier, pasangan Times di baris `courier` templat lama; newtx sendiri memakai `ntxtt` yang tidak punya versi OpenType | `newtxtext` + `newtxmath[varvw]` (sama dengan templat) | TeX Gyre Termes; *rm* Termes Math | `reference-<ukuran>-windows.docx` |
| `crc` | Latin Modern Roman (+ cadangan Latin Modern Math untuk Yunani dan ≤ ≈) | Latin Modern Sans | Latin Modern Math | Source Code Pro (0,8) | `lmodern` | Latin Modern Roman; *rm* Latin Modern Math; huruf Yunani mathtext dari cadangan "cm" (Computer Modern BaKoMa) | `reference-<ukuran>.docx` |
| `stix` | STIX Two Text (+ cadangan STIX Two Math untuk ≤ ≥ ≈) | STIX Two Text | STIX Two Math | Source Code Pro (0,8) | `stix2` | STIX Two Text; *rm* STIX Two Math | `reference-<ukuran>.docx` |

**Hasil uji 2026-11-08** (proyek uji `siapkan_proyek.py`; templat bab + bab uji berisi paragraf, rumus sebaris dan tampilan, simbol Unicode θ ≤ σ² ≈ × − di prosa dan komentar kode, gambar matplotlib berlabel *mathtext*, diagram TikZ, tabel, kode 72 karakter, dan keluaran 78 karakter). Semua opsi: G-RENDER, G-LOG, G-TAG, G-TEPI, G-PENGGALAN, dan G-HURUF LULUS; log tanpa "Missing character".

| Opsi | Teks, judul, tabel | Rumus | Kode | Gambar matplotlib | Diagram TikZ |
|---|---|---|---|---|---|
| `libertinus` | LibertinusSerif-Regular/Italic/Bold | LibertinusMath-Regular | LibertinusMono-Regular | LibertinusSerif, LibertinusMath | LibertinusSerif, LibertinusT1Math |
| `springer` | TeXGyreTermes-Regular/Italic/Bold | TeXGyreTermesMath-Regular | TeXGyreCursor-Regular | TeXGyreTermes, TeXGyreTermesMath | TeXGyreTermesX, NewTXMI, txsys (newtx) |
| `crc` | LMRoman10/12/17, LMRoman9 (catatan) | LatinModernMath-Regular | SourceCodePro-Regular | LMRoman10, LatinModernMath, Cmmi10, Cmex10 | LMRoman9, LMMathItalic9, LMMathSymbols9 |
| `stix` | STIXTwoText-Regular/Italic/Bold | STIXTwoMath-Regular | SourceCodePro-Regular | STIXTwoText, STIXTwoMath | STIXTwoText, STIXTwoMath (Type 1) |

Pelajaran dari uji yang kini dicegah gerbang atau skrip:

- Babel (`lang: id-ID`) memasang huruf teks lewat `\babelfont{rm}` sehingga cadangan glif lewat `\setmainfont` saja hilang. Akibatnya θ, μ, σ, ≤, ≈ hilang di Latin Modern Roman dan ≤, ≈ hilang di STIX Two Text. `huruf.py` memasangnya lewat `\babelfont`; `mainfontoptions` dengan `RawFeature={…}` tidak dipakai karena Pandoc meloloskan kurung kurawalnya.
- *mathtext* mengambil varian ukuran akar (`\sqrt`) dan kurung besar dari huruf cadangan STIX (STIXGeneral tersemat). `gaya_gambar.py` mengambil glif itu dari huruf matematika opsi (satu ukuran, cukup untuk label).
- Pada opsi `crc`, Unicode Yunani atau ≤ yang **dicampur dengan `$…$` dalam satu label** jatuh ke kotak kosong STIX karena Latin Modern Roman tidak punya glifnya. Tulis simbol di dalam `$…$` (`$\theta \leq 1$`). Label tanpa `$` aman karena memakai rantai huruf teks → matematika.
- Latin Modern punya varian optis bernama keluarga sama (LMRoman5–17); `gaya_gambar.py` hanya mendaftarkan berkas opsi.
- Pemeriksaan seri 2026-11-08: keenam PDF di `seri-bayesian/kirim/` dan 968 PDF gambar proyek seri hanya memuat Libertinus (LibertinusSerif, LibertinusMath, LibertinusMono, LibertinusT1Math). Huruf lain hanya ada di dua PDF fikstur harness (`harness/uji-buku/gambar/fig-baik.pdf`, `fig-cap.pdf`: TeXGyrePagella), bukan di buku.

### Profil penerbit dan ukuran buku (2026-11-08)

Dua kunci lain di `konfig.json` dapat digabung dengan opsi huruf: **`profil`** (ukuran huruf dasar dan blok teks penerbit) dan **`ukuran`** (kertas dan margin). Ukuran mono kode dan keluaran dihitung `huruf.py` dari lebar kolom. Nilai yang tidak terbaca dari berkas sumber ditulis "belum terverifikasi" dan tidak dikarang.

| Profil | Huruf dasar | Kode / keluaran (pada ukuran uji) | Catatan kaki | Judul bab | Trim | Blok teks | Sumber dan status |
|---|---|---|---|---|---|---|---|
| `seri` (bawaan) | 12 pt, spasi 1,1 | 7,2 / 6,8 pt (B5, Libertinus Mono) | 10 pt (scrbook 12 pt) | `\Huge` tebal, warna seri | dari `ukuran` (B5) | kolom 120 mm (B5) | keputusan seri; terverifikasi |
| `crc` | 10 pt (`\ExecuteOptions{letterpaper,10pt,…}`) | 7,55 / 7,15 pt (6x9, Source Code Pro) | 8 pt (`bk10.clo`) | nomor 24 pt tebal, judul 18 pt miring (`\ChapNumFont`, `\ChapTitleFont`) | 6 × 9 in (`\trimwidth`, `\trimheight`) | `krantz1`: 28pc + 0,5 pt × 45pc + 3 pt (118,3 × 190,8 mm); `krantz2`: 33pc × 51pc | `krantz.cls`; terverifikasi. Profil skill memakai `krantz1`. |
| `springer` | 10 pt | 7,7 / 7,25 pt (B5, TeX Gyre Cursor) | belum terverifikasi | belum terverifikasi | belum terverifikasi | belum terverifikasi (memakai `ukuran`) | templat SNmono tanpa opsi ukuran; 10 pt = bawaan kelas yang lazim, **belum terverifikasi** (svmono/SNmono tidak ada di TeX Live) |
| `wiley` | 11 pt (`\documentclass[11pt]{book}`) | 7,7 / 7,25 pt (B5, opsi springer) | 9 pt (`bk11.clo`) bila `.sty` tidak mengubahnya | belum terverifikasi | belum diketahui | belum diketahui (memakai `ukuran`) | templat Overleaf Wiley; huruf dan tata letak `.sty` tidak terbaca |

| Ukuran | Kertas (mm) | Margin dalam/luar/atas/bawah (mm) | Kolom (mm) | Karakter per baris (median/p95, templat bab) | Mono kode/keluaran untuk 72/78 karakter (Libertinus, 12 pt) | Batas kode/keluaran yang dianjurkan | Sumber dan status |
|---|---|---|---|---|---|---|---|
| `b5` | 176 × 250 | 28 / 28 / 22 / 24 | 120 | 60 / 69 | 7,2 / 6,8 pt | 72 / 78 | keputusan seri |
| `unesco` | 155 × 230 | 30 / 20 / 30 / 20 | 105 | 53 / 61 (batas 64/68) | 6,3 / 5,95 pt (di bawah 6,8) | **64 / 68** (mono 7,05 / 6,85 pt), atau terima mono kecil | pedoman LPPM Unsoed (lppm.unsoed.ac.id/wp-content/uploads/2024/06/Persyaratan-umum-buku-edit.docx-1.pdf: kiri 3 cm, kanan 2 cm, atas 3 cm, bawah 2 cm) dan penerbit Deepublish; dasar PO BKD yang disebut Deepublish **belum terverifikasi; cek teks pedoman PAK/BKD yang berlaku** |
| `a5` | 148 × 210 | 18 / 15 / 18 / 20 | 115 | 56 / 67 | 6,9 / 6,5 pt | 72 / **75**, atau terima keluaran 6,5 pt | ukuran ISO; margin bawaan skill (bukan standar) |
| `a4` | 210 × 297 | 30 / 30 / 25 / 25 | 150 | belum diukur (perkiraan > 70 pada 12 pt) | 9,05 / 8,5 pt | 72 / 78 | ukuran ISO; margin bawaan skill |
| `6x9` | 152,4 × 228,6 | 17 / 17 / 19 / 19 | 118,4 | 62 / 77 (profil `crc`, Latin Modern 10 pt) | 7,1 / 6,7 pt | 72 / 77, atau profil `crc` (mono 7,55 / 7,15 pt) | trim `krantz.cls` (6 × 9 in) |
| `7x10` | 177,8 × 254 | 19 / 19 / 19 / 19 | 139,8 | belum diukur | 8,45 / 7,95 pt | 72 / 78 | **belum terverifikasi**: `krantz.cls` hanya menyatakan trim 6 × 9 in; lebar `krantz2` 33pc + 2 × 0,75 in = 7 in |

- Permendikbudristek 22/2022 **tidak menetapkan angka ukuran buku**. Ia hanya mewajibkan ukuran buku dan margin ditetapkan pada tahap perancangan templat halaman isi (Lampiran hlm. 42).
- Bila mono hitungan di bawah **6,8 pt**, `huruf.py` menawarkan dua jalan: (a) batas baris lebih kecil (`batas_kode`, `batas_keluaran` di `konfig.json`; G-LEBAR-KODE dan G-LEBAR-KELUARAN membaca batas itu; `options(width = batas_keluaran − 3)` ditulis ke `<buku>/.Rprofile`), atau (b) menerima mono kecil.
- **Lebih dari 70 karakter per baris**: profil `springer` pada B5 (10 pt, kolom 120 mm) menghasilkan median 73 / p95 86; `crc` (6 × 9) p95 77; `wiley` p95 77. Angka ini melanggar aturan 40–70 karakter seri (Permendikbudristek 22/2022, Lampiran III). Saat menyerahkan naskah ke penerbit, **standar penerbit didahulukan**; untuk buku seri sendiri tetap pakai profil `seri`.
- `siapkan_proyek.py --ukuran <u> --profil <p> --huruf <h>`; sampul tidak dibawa skill (`assets/` tanpa templat sampul), jadi ukuran sampul diatur sendiri di proyek.

### Gaya Word: huruf bawaan Windows

`assets/reference-b5-windows.docx` (dibangkitkan `huruf.py --buat-docx` dari `reference-b5.docx`) memakai huruf yang ada di setiap Windows. Ukuran, menjorok baris pertama, spasi 0, kertas, dan bahasa id-ID tetap. Untuk ukuran buku dan profil lain `huruf.py` membangkitkan `reference-<ukuran>[-windows][-<pt>pt].docx`: kertas dan margin mengikuti `ukuran`, dan semua `w:sz` diskalakan ke huruf dasar profil (springer 10 pt, wiley 11 pt).

| Unsur | Gaya Windows | Padanan di PDF |
|---|---|---|
| Teks dan judul | Times New Roman | TeX Gyre Termes (`springer`), STIX Two Text (`stix`) |
| Sans (tidak ada gaya sans di reference-doc) | Arial | TeX Gyre Heros |
| Kode dan keluaran (Source Code, Verbatim Char) | Courier New | TeX Gyre Cursor, Source Code Pro |
| Rumus (OMML) | Cambria Math (`m:mathFont`) | TeX Gyre Termes Math, STIX Two Math |

- **Pemilihan**: opsi `springer` memakainya otomatis. Opsi lain memilihnya dengan `"docx_huruf": "windows"` di `konfig.json` atau `reference-doc` di `_quarto.yml`. PDF tetap memakai huruf opsinya.
- **Alasan**: naskah DOCX akan disunting orang lain atau diserahkan ke penerbit, yang belum tentu memasang Libertinus. Tanpa huruf itu Word mengganti hurufnya diam-diam dan tata letak bergeser.
- Rumus di Word memakai **Cambria Math**, jadi bentuknya berbeda dari PDF. Pandoc tidak menyalin `m:mathPr` dari reference-doc. Karena itu, `_quarto.yml` menjalankan `post-render: ../_bersama/huruf.py --pasca-render`, yang menulis `m:mathFont` (Cambria Math untuk gaya Windows, huruf matematika opsi untuk gaya lain) ke setiap DOCX di `_book/`. Hasilnya diperiksa G-DOCX-RUMUS (d).
- Uji 2026-11-08 (python-docx): DOCX `springer` dan `wiley` memakai Times New Roman di 75 *run* dan Courier New di 77 *run*, tanpa nama Libertinus di `styles.xml`, `document.xml`, `fontTable.xml`, `settings.xml`, dan `theme1.xml`; ukuran dasar 10 pt (springer) dan 11 pt (wiley).

### Rumus di Word (2026-11-08)

| Aturan | Gerbang |
|---|---|
| Semua rumus ditulis sebagai matematika Pandoc (`$…$`, `$$…$$`, `aligned`, `cases`), bukan blok `{=latex}` mentah atau gambar. Pandoc mengubahnya menjadi persamaan Word asli (OMML) yang dapat disunting di Word. | G-DOCX-RUMUS (a)(b) |
| Makro rumus tidak boleh hanya didefinisikan di preamble LaTeX karena DOCX tidak membacanya. Definisikan dengan `\newcommand` di blok `$$` di awal dokumen (dipahami Pandoc) atau ganti dengan perintah standar. | G-DOCX-RUMUS (b) |
| Pakai perintah yang didukung OMML: `\operatorname`, `\mathrm`, `\boldsymbol`, `\text`. | reviewer rumus, tinjauan DOCX |
| Nomor persamaan dan rujukan `@eq-` tampil di Word. | tinjauan DOCX |
| Gambar yang memuat rumus (plot, diagram) tetap gambar; rumus di prosa dan tabel tidak boleh berupa gambar. | G-DOCX-RUMUS (c) |
| Persamaan Word asli dapat dikonversi MathType; **perlu dicek di versi MathType pengguna** (skill tidak menguji MathType). | — |

Aturan G-DOCX-RUMUS: (a) jumlah `m:oMath` di `word/document.xml` ≥ jumlah rumus sumber − maks(2, 2%). Rumus sumber dihitung dari blok `$$…$$` dan `$…$` sebaris di prosa bab yang terdaftar di `_quarto.yml`, di luar chunk, kode sebaris, R inline, komentar HTML, dan `\$`. (b) Tidak ada `\frac`, `\sum`, huruf Yunani TeX, `^{`, atau `_{` di *run* teks yang bukan bergaya kode. (c) Tidak ada gambar dengan nama atau teks alternatif bermakna rumus (`eq`, `rumus`, `persamaan`, `equation`, atau TeX). (d) `m:mathFont` sesuai gaya Word. Uji templat bab 2026-11-08: rumus sebaris, `aligned`, dan rumus di tabel menjadi OMML.

## 9. Bahasa (ringkas)

Rinci di skill **eyd** (`references/kalimat-efektif.md`, `kata-hubung.md`, `inventaris-kesalahan.md`) dan `istilah-statistika.md`.

- Setiap kalimat **utuh**: subjek dan predikat jelas; tanpa subjek berkata depan ("Dalam bab ini membahas …"); tanpa anak kalimat berdiri sendiri (kalimat diawali "Sehingga", "Karena", "Yang"); tanpa konjungsi ganda ("Meskipun … tetapi").
- **Koma konjungsi** (EYD V B.2–B.5, B.13): **tanpa** koma sebelum penghubung subordinatif bila induk mendahului anak kalimat (*sehingga, karena, sebab, agar, supaya, bahwa, jika, bila, apabila, kalau, meskipun, walaupun, ketika, setelah, sebelum, sejak, selama*), termasuk bila kalimat diawali anak kalimat lain. **Dengan** koma sebelum *tetapi, melainkan, sedangkan, padahal*; sesudah anak kalimat yang mendahului induk; sesudah penghubung antarkalimat (*Akibatnya,* *Oleh karena itu,* *Namun,*); sebagai penutup aposisi/sisipan. ", karena itu" di tengah kalimat → pecah kalimat. *Sehingga* tidak mengawali kalimat. Kalimat > 30 kata dipecah. Gerbang: G-KONJUNGSI; pengecualian sah per kalimat di `pengecualian.json` (`konjungsi-abaikan`), dinilai satu per satu, tidak dihapus massal.
- Istilah asing yang **diputuskan tetap dalam bahasa Inggris** (contoh: *odds*) selalu dicetak miring di prosa, judul, keterangan, dan latihan. Bila kalimat yang memuat istilah itu menjadi `penanda` klaim di `harness/klaim.json`, penanda ikut diperbarui agar tetap sama persis dengan teks `.qmd` (mis. `*odds*`); kutipan bukti tidak diubah (keputusan penulis seri, dicatat 2026-11-07).
- Istilah asing tanpa padanan lazim dicetak miring dan dijelaskan pada kemunculan pertama **di setiap bab**; verba tidak dibuat hibrida ("di-*fit*" → "dicocokkan"); akhiran pada istilah asing memakai tanda hubung (*shrinkage*-nya).
- *fit*: **mencocokkan/pencocokan** (model dengan data), "objek hasil pencocokan", *fitted values* = nilai prediksi, *goodness of fit* = kecocokan model, *overfitting* miring; "mencocokkan" dalam arti membandingkan → "membandingkan"; istilah Inggrisnya disebut pada kemunculan pertama per buku (`istilah-statistika.md`).
