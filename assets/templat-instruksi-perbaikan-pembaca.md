# Instruksi perbaikan dari pembaca pemula independen (<tanggal>)

<!-- Templat skill buku-ajar. Penyunting adalah agen BERBEDA dari pembaca yang menulis
laporan dan dari agen yang mengaudit; satu agen per kelompok bab tanpa irisan. Pola ini
juga dipakai untuk tindak lanjut telaah pakar (peran 21): ganti nama laporan. -->

Anda penulis-penyunting (`<skill>/agents/04-penulis.md`), bukan pembaca yang menulis
laporan. Proyek: <proyek>. Lingkungan: <perintah lingkungan>.
Aturan mengikat: `KEPUTUSAN-RANCANGAN.md`, brief dan `keputusan-istilah.md` buku,
`<skill>/references/aturan-gaya-dan-tampilan.md`, `istilah-statistika.md`,
`kunci-jawaban.md`.

Bab yang ditugaskan: <buku>/<babXX>, <babYY>.

Untuk setiap bab:

1. Baca `<buku>/naskah/ulasan/babXX-pembaca-pemula-independen.md` dan babnya.
2. **Periksa setiap temuan seperti reviewer isi sebelum mengubah apa pun**: cocokkan dengan
   naskah dan hasil kode, hitung ulang dengan R bila temuan menyangkut angka, cek kutipan di
   registri klaim bila menyangkut sumber. Temuan yang ternyata keliru: tulis
   "tidak diterapkan" beserta buktinya (angka hitung ulang, baris, kutipan).
3. Tutup semua MAYOR yang sah. Bila ada kesalahan angka atau ketidakcocokan kode, perbaiki
   kodenya dan biarkan angka dihitung inline. Perbaiki MINOR yang kecil dan jelas. MINOR
   yang butuh contoh baru atau keputusan penulis: **tunda** dengan alasan dan nilai bawaan
   sementara, lalu masukkan ke "Usulan untuk diputuskan penulis" (loop-kerja.md).
4. Latihan yang berubah: sesuaikan kunci di buku kunci (bentuk lengkap, rubrik 10 poin) dan
   catat di `kunci-<buku>/naskah/temuan-soal.md`. Nomor latihan lama tidak digeser; latihan
   baru di akhir kelompoknya.
5. Harness tanpa `--render` sampai LULUS untuk setiap berkas yang diubah (bab dan kunci).
   JANGAN `--render`. Klaim hanya lewat `flock <scratchpad>/klaim.lock`; bila kalimat
   berklaim berubah, sesuaikan penandanya saja, jangan kutipannya.
6. Tulis `## Tindak lanjut (<tanggal>)` di setiap laporan: per temuan "diperbaiki (lokasi)",
   "tidak diterapkan (bukti)", atau "ditunda (alasan; usulan untuk penulis no. N)".
7. Jangan ubah `_quarto.yml`, `_bersama/`, `harness/*.py`, atau bab di luar tugas Anda.

Balasan akhir (≤ 150 kata): per bab, MAYOR ditutup/tidak diterapkan, MINOR
diperbaiki/ditunda, latihan dan kunci yang berubah, status harness.
