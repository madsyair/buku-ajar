# Kerangka Bab N — <Judul Bab> (<tanggal>)

Anggaran: <…> hlm. Label bab `sec-…`; label lain bersufiks `-<kode>-NN`. Chunk setup `setup-<kode>babNN`. Berkas fit `fit/<kode>-NN-*`. Kode tersembunyi: `lampiran-kode/<buku>/babNN.R`.
Disiplin: <satu disiplin | multidisiplin: `model`, `ml`, …>. Penulis: <04 | 04a per disiplin + 04b pemadu>. Reviewer ahli: <05–08, 16–20 sesuai disiplin>; lintas bagian: 07, 09 (+ 20 untuk multidisiplin).
Target: ±<…> kata prosa, <…> gambar data (Python) + <…> TikZ, <…> tabel, ±<…> baris kode tampil.

## Pembuka

- Pertanyaan pembaca yang muncul dari bab sebelumnya: "<…>"
- Ingat dari Buku <N>, Bab <M> (<judul final>): <konsep yang diperlukan, bukan daftar istilah>.
- Tujuan belajar (3–5 butir berkata kerja terukur): …
- Prasyarat dan notasi kunci: …

## Enam pertanyaan perencanaan (tidak tampil sebagai subjudul)

| Metode | Apa masalahnya | Mengapa bukan cara naif | Kapan dipakai / asumsi | Bagaimana menghitung | Bagaimana menafsirkan | Kapan gagal |
| --- | --- | --- | --- | --- | --- | --- |

## Subbab

1. `sec-…-<kode>-NN` <Subjudul frasa, bukan kalimat tanya>
   - **Pertanyaan pembaca** (kalimat pertama prosa): "<…?>"
   - **Penjelasan sederhana** (2–5 kalimat, tanpa notasi): …
   - Isi berurutan: intuisi (contoh/data/analogi + batasnya) → rumus (simbol dijelaskan) → kode → interpretasi angka.
   - Klaim bersumber: <isi> [@kunci] (lokasi untuk registri: bag. …).
   - Gambar/tabel: `fig-…-<kode>-NN` "<judul ≤ 12 kata>: (a) …, (b) …"; data parquet `<buku>-babNN-…`; yang harus terlihat: …
   - Miskonsepsi yang disanggah (bila ada): …
   - **Disiplin dan penugasan** (multidisiplin): disiplin `<kode>`; penulis ahli 04a `<kode>`; berkas `babNN-<kode>.qmd`; reviewer ahli <nomor>; prasyarat dari disiplin lain: …

## Jembatan antardisiplin (multidisiplin; ditulis pemadu 04b)

| Dari subbab (disiplin) | Ke subbab (disiplin) | Yang sudah diketahui pembaca | Mengapa sudut pandang baru diperlukan | Istilah/notasi yang berganti |
| --- | --- | --- | --- | --- |

## Contoh utama `sec-contoh-utama-<kode>-NN`: <judul>

Kaitan dengan peta alur kerja/kerangka seri: <…>; yang baru di bab ini: <…>.

Disiplin per langkah (multidisiplin): <mis. Model dan Periksa: `model`; Hitung: `komputasi`; Interpretasikan: `<domain>`>.

1. Pertanyaan dan data (status data; sumber):
2. Model (formula, prior beserta alasan, DAG):
3. Hitung (`file =`, `seed`):
4. Periksa (diagnostik satu kalimat; pemeriksaan model sesuai jenis respons):
5. Interpretasikan (skala respons, kalimat yang dapat dikutip):
6. Uji kepekaan (asumsi yang diubah; katakan bila kesimpulan bergeser):

## Ringkasan

Tiga pesan utama; kalimat penutup bagi pembaca terapan.

## Latihan (<n> butir)

| No. | Jenis | Tujuan yang diuji | Data/parameter/*seed* | Kriteria dan bentuk jawaban |
| --- | --- | --- | --- | --- |
| 1 | Konseptual | | | |
| … | Penurunan sederhana | | | |
| … | Hitungan | | | |
| … | Pemrograman ("tiru alurnya") | | | |
| … | Campuran berjarak (bab sebelumnya, metode tidak disebut) | | | |
| … | Lintas disiplin (multidisiplin: memadukan minimal dua bagian) | | | |
