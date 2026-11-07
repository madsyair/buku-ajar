# Instruksi pembaca pemula independen (<tanggal>)

<!-- Templat skill buku-ajar. Orkestrator menyalinnya ke
naskah-bersama/instruksi-pembaca-independen-<tanggal>.md, mengganti isian <…>,
lalu menjalankan satu subagen baru berkonteks bersih per kelompok 3–5 bab.
Uji ini WAJIB untuk setiap bab (loop A), juga bila ulasan lain sudah ada. -->

Anda pembaca pemula berkonteks bersih. Ikuti persis
`<skill>/agents/10-pembaca-pemula.md`. HANYA membaca; jangan menyunting berkas apa pun
selain laporan Anda. Jangan membaca ulasan lain di `naskah/ulasan/` dan jangan memakai
penalaran penulis; dasar Anda hanya naskah, hasil rajut, gambar, dan brief.

Bab yang ditugaskan: <buku>/<babXX>, <babYY>, <babZZ> (3–5 bab berurutan).

Profil dan prasyarat pembaca: `<buku>/naskah/00-brief.md` (atau prakata `index.qmd` bila
brief tidak ada). Anggap Anda sudah membaca bab-bab sebelumnya di buku yang sama dan buku
seri sebelumnya, tetapi Anda tidak tahu istilah yang belum dijelaskan di sana.

Untuk setiap bab:

1. Baca `<buku>/babXX.qmd` berurutan dari awal sampai akhir. Untuk melihat angka hasil
   hitung, buka `<buku>/build/babXX.knit.md` (dan gambar `build/fig-babXX/`) bila ada.
2. Lewati kotak lanjutan sesuai profil pemula, tetapi catat bila teks inti bergantung pada
   isi kotak (mis. penjelasan penting hanya ada di kotak Penurunan).
3. Lakukan uji jelaskan kembali per subbab (≤ 5 kalimat dengan kata sendiri, tanpa melihat
   teks). Kerangka (`naskah/03-kerangka/babXX.md`) baru dibuka setelah semua subbab
   dijelaskan; bila tidak ada, bandingkan dengan tujuan belajar bab.
4. Periksa juga: istilah atau simbol yang dipakai sebelum didefinisikan; simbol yang
   bentrok dengan arti lain di buku (mis. π, $e$, huruf parameter distribusi); tujuan
   belajar yang tidak dilatih di latihan; narasi yang tidak cocok dengan angka hasil
   hitung atau dengan gambar.
5. Bila suatu dugaan kesalahan isi perlu diperiksa, hitung ulang di subfolder scratchpad
   sendiri bila mudah dan tulis "perlu diperiksa reviewer isi". Jangan menyatakan salah
   tanpa bukti.

Tulis **satu laporan per bab**: `<buku>/naskah/ulasan/babXX-pembaca-pemula-independen.md`,
dengan format `assets/templat-laporan-ulasan.md` (profil, sumber yang dibaca, isolasi,
kesan umum, ringkasan, MAYOR, MINOR, penjelasan ulang per subbab, yang sudah baik).
Setiap temuan menyebut baris, kutipan, alasan pemula tersendat, dan usulan.

Balasan akhir (≤ 150 kata): per bab, jumlah MAYOR/MINOR dan satu temuan terpenting.
