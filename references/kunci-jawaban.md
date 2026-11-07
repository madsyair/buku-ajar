# Kunci jawaban dan pembahasan untuk pengajar

Disarikan dari rancangan dan instruksi kunci jawaban seri statistika Bayesian (keputusan penulis 2026-11-07). Dipakai agen `agents/13-pembuat-kunci-jawaban.md` dan `agents/14-penyunting-soal.md`.

## Bentuk terbitan

- Satu buku pendamping per buku induk: **"Kunci Jawaban dan Pembahasan untuk Pengajar"**, terbit terpisah; buku induk tidak memuat jawaban.
- Folder `kunci-<buku>/`, Quarto *book* dengan `_quarto.yml`, preamble, filter, gaya gambar, dan harness yang **sama** dengan buku induk. `pustaka.bib` salinan bib buku induk.
- Satu bab kunci per bab induk (`kunci-babXX.qmd`), judul bab sama, label `#sec-kunci-kN-XX`; label lain bersufiks `-kN-XX`.
- Sampul memakai halaman sampul buku induk. Prakata singkat menjelaskan cara pakai rubrik.

## Isi setiap latihan

Setiap latihan `### Latihan N {#sec-kN-XX-lN}` (nomor sama dengan buku induk; pengelompokan induk seperti "Konseptual", "Hitungan" ditiru sebagai `## … {.unnumbered}`) memuat berurutan:

1. **Ringkasan soal** satu kalimat (bukan salinan utuh), agar kunci dibaca berdampingan dengan buku induk; sebut jenis soal.
2. `#### Pembahasan langkah demi langkah {.unnumbered}`: langkah bernomor, setiap langkah dengan alasan, rumus, atau kode yang dijalankan; angka inline.
   - *Konseptual*: langkah = urutan penalaran dengan angka pendukung dari bab induk.
   - *Hitungan/komputasi*: kode R (atau Stan/brms) yang **benar-benar dijalankan**, keluaran ringkas, angka di prosa dihitung inline.
   - *Penurunan*: langkah aljabar (boleh dalam kotak Penurunan), lalu pemeriksaan numerik bila mungkin.
   - *Terbuka* ("diskusikan", "rancang"): cara menyusun jawaban yang baik dan satu contoh jawaban.
3. **Jawaban akhir** sebagai kutipan blok tersendiri setelah langkah terakhir: `> **Jawaban akhir:** isi jawaban.` (hanya label yang tebal).
4. `#### Pedoman penilaian {.unnumbered}`: kalimat pengantar yang merujuk tabel, lalu **tabel rubrik** (judul ≤ 12 kata, mis. "Rubrik Latihan 1 Bab 1"), kolom unsur/langkah dan skor, **total 10 poin**; lalu Div `::: {.catatan}` berisi kesalahan umum dan pengurangan poinnya, contoh jawaban sebagian dan skornya, serta variasi jawaban lain yang tetap benar.

Rubrik dibangun dengan fungsi pembantu yang dijaga `stopifnot(sum(skor) == 10)` (lihat `assets/templat-bab-kunci.qmd`). Skor contoh jawaban sebagian harus sama dengan penjumlahan rubrik (temuan berulang: "diberi 6 poin" padahal rubrik memberi 7).

## Aturan mutu

- Semua aturan buku induk berlaku dan ditegakkan harness yang sama (EYD V, istilah, koma konjungsi, subjek sitasi, judul, subjudul bukan kalimat tanya, tanpa luapan tepi, nama tidak dipenggal, tanpa nama teknik pengajaran, tanpa basa-basi).
- **Bab kunci mandiri**: chunk `setup` tersembunyi membangun ulang data dan objek yang dipakai soal (data, prior, *seed*, notasi sama dengan bab induk); jangan `source()` berkas buku induk. Baca juga keluaran rajutan induk (`build/babXX.knit.md`) untuk angka yang dipakai bab.
- Model mahal disimpan di `kunci-<buku>/fit/` dengan `file =` dan *seed* tetap.
- Rujukan ke buku induk ditulis sebagai teks ("Buku 2 Bab 7, Subbab 7.3"); rujukan di dalam buku kunci memakai `@sec/@eq/@tbl` berlabel bersufiks.
- Sitasi hanya bila perlu; lebih baik merujuk bab induk dengan teks daripada menambah sitasi. Klaim bersumber tetap masuk registri lewat `flock`.
- Label kategori, nama kelompok, dan simbol dalam jawaban **sama persis** dengan soal dan tabel bab induk.
- Kalimat tafsiran yang bergantung pada angka ditulis bersyarat atau dikunci `stopifnot` (temuan berulang: tafsiran otomatis tidak lagi cocok dengan angka hasil rajutan).

## Temuan soal

Bila menyusun kunci menunjukkan soal induk ambigu, salah, kurang data, atau tidak dapat dijawab dengan isi bab:

1. Penulis kunci **tidak mengubah buku induk**. Ia mencatat satu baris di `kunci-<buku>/naskah/temuan-soal.md` (templat `assets/templat-temuan-soal.md`): bab, latihan, masalah (dengan angka bila perlu), dan **rumusan soal baru yang lengkap** (bukan hanya masalahnya).
2. Penulis kunci menulis kunci untuk **rumusan soal baru** itu, dengan catatan pengajar bila perlu.
3. Agen **penyunting soal** (terpisah, agar tidak ada dua agen menyunting berkas yang sama) menerapkan rumusan baru ke buku induk, menandai baris temuan "**Diterapkan YYYY-MM-DD:** …", menjalankan harness bab induk sampai LULUS.
4. Penulis kunci (atau penyunting soal, bila disepakati orkestrator) menyesuaikan kunci dengan soal yang benar-benar diterapkan dan menjalankan harness bab kunci.
5. Keputusan yang mengubah makna soal secara berarti diajukan kepada penulis.

Pola masalah soal yang sering ditemukan: kriteria tidak disebut ("mulai memadai", "tidak lagi bergantung"), parameter simulasi tidak lengkap (proporsi, ukuran, *seed*), jawaban bergantung pada *seed* atau komputer (waktu jalan), istilah ambigu (lebar total vs setengah lebar), skenario tidak wajar, label indeks yang menyesatkan (komponen ke-3 dari `ordered` bukan "komponen tambahan").

## Pemeriksaan independen kunci

Satu agen pemeriksa per buku kunci (konteks bersih), hanya membaca:

- mencocokkan setiap latihan dengan soal induk (nomor, ringkasan, semua bagian dijawab);
- **menghitung ulang mandiri** dengan kode sendiri di scratchpad (metode lain bila mungkin: vektor eigen vs matriks fundamental, integrasi numerik, grid); model mahal dibaca dari `fit/*.rds`, tidak dijalankan ulang;
- memeriksa program Stan dengan `stanc` bila ada;
- menjumlahkan semua rubrik (harus 10), memeriksa setiap latihan memuat `> **Jawaban akhir:**`;
- memeriksa istilah terlarang dan istilah keputusan;
- melaporkan MAYOR/MINOR per bab dengan tabel ringkas jumlah temuan; temuan yang menyangkut soal diteruskan ke `temuan-soal.md`.

## Alur kerja

1. Kerangka proyek buku kunci (sebelum menulis): `_quarto.yml`, preamble, prakata, bab rintisan.
2. Penulisan per kelompok bab (paralel, satu agen per kelompok, satu agen per berkas).
3. Pemeriksaan independen per buku; perbaikan.
4. Render buku kunci berurutan; G-RENDER, G-TEPI, G-PENGGALAN.
5. Bila buku induk masih ditulis, bab kunci ditambahkan setiap kali satu bab induk selesai.
