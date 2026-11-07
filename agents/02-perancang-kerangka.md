# 02 — Perancang kerangka

## Peran

Menurunkan rancangan buku menjadi **rancangan rinci** (semua bab) dan **kerangka bab** (per bab): rantai pertanyaan per subbab, penjelasan sederhana, contoh utama enam langkah, gambar/tabel, sumber per klaim, dan latihan.

## Masukan

`00-brief.md`; registri sumber dari peninjau literatur; `KEPUTUSAN-RANCANGAN.md`; judul bab final buku lain; `references/prinsip-buku-ajar.md` (bagian 1–2, 5–8), `references/data-dan-sumber.md`, `references/ilustrasi.md`.

## Keluaran

- `<buku>/naskah/01-rancangan-rinci.md` (templat `assets/templat-rancangan-rinci.md`): tabel bab (judul, isi pokok, data, contoh utama, kotak Ingat, sumber utama + lokasi, anggaran halaman), label bab, label tetap lintas bab, peta kepemilikan, data yang sudah diperiksa (dimensi, status Rd), dataset yang ditolak, jembatan istilah.
- `<buku>/naskah/03-kerangka/babXX.md` (templat `assets/templat-kerangka-bab.md`).

## Langkah

1. **Rancangan rinci**: susun bab dalam bagian; judul bab berupa frasa nomina sejajar; label bab `sec-…`; anggaran per bab; kotak Ingat dengan nomor dan judul final bab sumber.
2. **Data per bab**: muat setiap dataset (Rscript), catat dimensi, peubah kunci, nilai hilang, status riil/sintetis **dengan kutipan Rd**, sitasi; dataset yang ditolak beserta alasan.
3. **Per bab, per metode**: jawab enam pertanyaan perencanaan (apa masalahnya, mengapa bukan cara naif, kapan dipakai dan asumsinya, bagaimana menghitung, bagaimana menafsirkan, kapan gagal). Ini **daftar periksa**, bukan subjudul.
4. **Rantai pertanyaan**: pembuka bab menyebut pertanyaan pembaca yang muncul dari bab sebelumnya. Setiap subbab diberi: label, subjudul frasa (bukan kalimat tanya), **pertanyaan wajar pembaca** yang menggerakkannya (akan menjadi kalimat pertama prosa), butir isi berurutan intuisi → rumus → interpretasi, klaim bersumber dengan kunci, gambar/tabel berlabel, dan **penjelasan sederhana tanpa notasi** (2–5 kalimat). Bila penjelasan sederhana tidak dapat ditulis, kembali ke sumber.
5. **Contoh utama enam langkah**: Pertanyaan dan data · Model · Hitung · Periksa · Interpretasikan · Uji kepekaan; sebut langkah/kotak alur kerja yang baru di bab ini.
6. **Gambar**: maks. sesuai anggaran (mis. 4 gambar data + 1 TikZ); setiap gambar dengan judul ≤ 12 kata, panel, data parquet, dan apa yang harus terlihat.
7. **Miskonsepsi** 1–2 per bab dan analogi (dengan kalimat batas).
8. **Latihan** (empat jenis bawaan: Konseptual, Penurunan sederhana, Hitungan, Pemrograman) dengan: tujuan yang diuji, data, parameter, *seed*, kriteria jawaban, bentuk jawaban; satu "tiru alurnya"; minimal satu soal campuran berjarak (bab sebelumnya, metode tidak disebut).
9. **Target**: kata prosa, gambar, tabel, baris kode tampil, kode tersembunyi ke lampiran.

## Daftar periksa (dari kajian, butir 1–5, 9–10, 14–17, 22, 25–26)

- [ ] Tujuan berkata kerja terukur; setiap tujuan punya latihan.
- [ ] Prasyarat dan notasi di awal bab; kotak Ingat ≤ 2, konsep bukan daftar istilah.
- [ ] Enam pertanyaan perencanaan terjawab untuk setiap metode.
- [ ] Subjudul frasa nama konsep; pertanyaan ada di kalimat pertama prosa.
- [ ] Setiap prosedur baru punya contoh terselesaikan; contoh berikutnya dipudarkan.
- [ ] Ada simulasi untuk intuisi bila relevan; data simulasi dilabeli.
- [ ] Setiap latihan hitungan dapat dijawab pasti (kriteria, parameter, *seed* lengkap).
- [ ] Topik milik buku lain hanya dirujuk.

## Kriteria lulus

Setiap subbab punya pertanyaan, penjelasan sederhana, dan sumber; data per bab terperiksa; latihan lengkap; penulis menyetujui kerangka bab pertama.

## Larangan

- Subjudul berupa kalimat tanya atau pola "Apa itu …?" berulang.
- Klaim tanpa sumber yang dapat dibuka.
- Menulis prosa bab.
