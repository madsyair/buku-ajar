# Pelajaran dari proyek seri statistika Bayesian

Kesalahan yang **berulang** ditemukan peninjau independen pada Buku 1–3 dan kunci jawabannya (November 2026), beserta cara mencegahnya. Penulis membaca berkas ini sebelum menulis bab; peninjau memakainya sebagai daftar buru.

## 1. Narasi tidak cocok dengan gambar

*Gejala*: prosa berkata "interval melebar untuk pekerjaan yang pekerjanya sedikit, seperti penjualan", padahal di panel (a) berskala dolar yang paling lebar justru manajemen; narasi PPC "panel (a)" berlawanan dengan gambar; narasi hanya menceritakan sebagian kuantil.

*Pencegahan*: setiap ciri gambar yang disebut di prosa (urutan, terlebar, banyak garis keluar pita, arah) **dihitung di R** dari data yang sama dengan parquet gambar, ditulis inline atau sebagai kalimat bersyarat, dan bila menjadi dasar kalimat tetap, dikunci `stopifnot()`. Perhatikan skala (log vs asli) dan panel yang dimaksud. Peninjau membuka PDF dan parquet, bukan hanya qmd.

## 2. Ambang tipis

*Gejala*: kalimat bersyarat `if (x < y - 0.01) "turun cukup jauh"` lolos dengan selisih 0,0002; "interval tidak memuat nol" dengan batas bawah 0,00067; "kokoh" dengan ambang 0,03 sementara nilainya 0,0255 dan arahnya justru melebar; daftar kategori ekstrem bergantung pada potongan 0,025/0,975 dengan kategori lain nyaris ikut.

*Pencegahan*: pilih ambang yang jauh dari nilai (beberapa galat Monte Carlo/galat baku), atau tulis tiga cabang (jelas di atas, jelas di bawah, "di sekitar ambang"); sebut nilai yang nyaris ("perempuan nyaris, 0,046"); hindari kata sifat penilai (kokoh, cukup jauh) tanpa ukuran. Reviewer kode mencetak margin setiap kalimat bersyarat dan menandai margin < 2 MCSE atau < 10% ambang.

## 3. Klaim "sama", "tidak satu pun", "cocok" tanpa penguncian

*Gejala*: "tidak satu pun *draw* positif" dengan kode `< 0.001` yang masih meloloskan tiga *draw*; "kira-kira sama" untuk dua kuantil yang berbeda dua kali lipat; tafsiran otomatis di kunci yang tidak lagi cocok setelah dirajut ulang.

*Pencegahan*: klaim kesamaan/ketiadaan memakai uji persis (`== 0`, `all.equal(…, tolerance =)`) dan `stopifnot()` di chunk tersembunyi; bila render ulang mengubah fakta, rajut gagal dan penulis tahu. Kata "sama" hanya untuk kesamaan dalam toleransi yang disebut.

## 4. Kotak "Ingat" menumpuk istilah

*Gejala*: satu kotak memadatkan R-hat, ESS *bulk*/*tail*, *divergent transition*, NUTS, PSIS, Pareto $\hat k$ tanpa arti; kotak mengulang definisi yang diulang lagi di prosa; NUTS disebut tanpa penjelasan.

*Pencegahan*: kotak Ingat maks. satu paragraf berisi **konsep** yang diperlukan dari bab sumber, bukan daftar istilah; istilah yang belum dikenal pembaca (yang boleh melompat buku) dijelaskan di prosa pada tempat pemakaiannya; satu istilah baru per kalimat. Pembaca pemula menghitung istilah baru per kotak.

## 5. Label kategori dan arti peubah tidak sesuai dokumentasi

*Gejala*: jawaban akhir menulis "manufaktur" padahal soal dan tabel memakai "manufaktur dan pertambangan"; label indeks komponen `ordered` ditafsirkan sebagai "komponen tambahan"; dokumentasi Rd disitasi ke artikel JSS penulis paket.

*Pencegahan*: label kategori, satuan, dan arti peubah diambil dari Rd paket (kutip di rancangan rinci) dan dipakai persis sama di soal, tabel, gambar, dan kunci; nama level faktor dicetak dari data, bukan diketik; sitasi dokumentasi ke entri `citation("paket")` atau halaman bantuan.

## 6. Label "lemah/sempit" dan istilah yang berganti makna

*Gejala*: N(0; 1) disebut "lemah" di satu subbab dan "sempit" di contoh utama karena skala respons berbeda; "prior N(0;10) per dolar tidak lemah" padahal superlebar; "lemah informatif" bertentangan dengan keputusan istilah.

*Pencegahan*: label set model/prior ditetapkan sekali per bab dan selalu dikaitkan dengan skalanya; reviewer rumus memeriksa setiap kata sifat terhadap skala yang dimaksud.

## 7. Penjelasan mekanisme yang keliru walau angkanya benar

*Gejala*: "R² lebih rendah karena koefisien jarang menyebar merata", padahal sebab utamanya ketaksamaan Jensen; "posterior LOO berrata-rata tak berhingga" padahal yang dimaksud distribusi rasio bobot *importance*; ridge tanpa syarat y terpusat.

*Pencegahan*: setiap "karena" yang menjelaskan hasil numerik diuji reviewer rumus dengan simulasi pembanding kecil; parafrase sumber setia pada kutipan; syarat (prior *proper*, data terpusat) disebut.

## 8. Notasi dan pembulatan tidak konsisten

*Gejala*: N(0; 10) dan N(0, s) dalam satu bab; "22,5%" dan "22%" untuk nilai yang sama; "0.5" bertitik di prosa dari `paste()`; ± tercetak sebagai `$±$` karena menempel ke kode inline.

*Pencegahan*: pemisah parameter titik koma bila ada desimal; satu fungsi `angka()`/`persen()` dengan digit yang sama untuk besaran yang sama; tidak memakai `paste()` angka mentah; karakter Unicode langsung di prosa.

## 9. Soal latihan yang tidak dapat dijawab pasti

*Gejala*: kriteria tidak disebut ("mulai memadai"), parameter simulasi tidak lengkap, jawaban bergantung pada *seed* atau kecepatan komputer, istilah ambigu (lebar total vs setengah lebar), skenario tak wajar (peluang transisi 0).

*Pencegahan*: perancang kerangka menulis untuk setiap latihan hitungan: data, parameter, *seed*, kriteria, bentuk jawaban; pembuat kunci menjawab semua soal sebelum buku dianggap selesai dan mencatat temuan soal (loop C).

## 10. Pengulangan dan panjang

*Gejala*: bab melampaui anggaran karena definisi diulang di kotak, prosa, dan ringkasan; contoh pendek lebih dari dua; kode pembantu ditampilkan.

*Pencegahan*: anggaran per bab (kata/400 + gambar/2 + kode) dilaporkan penulis tiap putaran; kode pembantu `echo: false` dan dirujuk ke lampiran; pemangkasan hanya untuk kalimat mubazir dan pengulangan, **bukan** penjelasan, contoh, atau langkah penurunan (keputusan penulis: kejelasan didahulukan, anggaran bukan batas keras).

## 11. Tampilan cetak

*Gejala*: luapan tepi dari keluaran lebar, rumus panjang, tabel lebar; blok kode terbelah satu baris di halaman berikut; label TikZ tertimpa panah; legenda menutupi data; puncak prior menjulang sehingga posterior tampak kecil; tabel terbelah longtable.

*Pencegahan*: gerbang G-LEBAR-KELUARAN dan G-TEPI; `\needspace` sebelum chunk pendek; pembaca/editor memeriksa PDF hasil render per halaman bab; batasi sumbu atau sebut di catatan bila puncak dipotong.

## 12. Proses multi-agen

*Gejala*: dua agen menulis `klaim.json` bersamaan; render paralel saling menimpa `_book/`; render terpisah PDF lalu Word menghapus berkas format pertama; registri klaim usang setelah kalimat diubah; pekerjaan hilang saat kontainer dimulai ulang.

*Pencegahan*: satu agen per berkas; `flock` untuk berkas bersama; render berurutan oleh orkestrator dalam satu `quarto render`; penanda klaim diperbarui bersama kalimatnya (G-REFERENSI menangkap yang usang); titik simpan git setelah setiap bab/putaran lulus dan `STATUS.md` diperbarui (lihat orkestrator).

## 13. Nama teknik pengajaran bocor ke naskah

*Gejala*: brief menamai teknik (wajar sebagai instruksi), lalu agen penulis menyalin "pertanyaan Sokratik" atau "uji Feynman" ke latihan atau kotak.

*Pencegahan*: G-LARANGAN pada semua bab buku induk dan kunci; brief buku menyebut gaya dengan deskripsi ("pertanyaan wajar pembaca", "penjelasan sederhana yang dapat diulang"), bukan nama; nama label internal hanya di berkas skill.
