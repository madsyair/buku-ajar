# Gaya Buku Ajar: Komunikatif, Semi-Formal, Istilah Terjelaskan, Rujukan Seperlunya

Berkas ini mengatur **tahap gaya akhir** setiap bab, yaitu tahap sesudah bab ditulis, ditinjau, dan diperbaiki (loop A). Selama loop A, naskah sengaja padat sitasi supaya setiap pernyataan punya dasar rujukan yang dapat diperiksa (G-REFERENSI). Pada tahap ini naskah ditulis ulang agar bergaya **buku ajar**, bukan artikel ilmiah. Dasarnya tetap utuh di registri klaim.

Peran yang menjalankan tahap ini: **22 Penyunting gaya buku ajar** menelaah dan menulis ulang, **23 Penerap revisi gaya** memeriksa dan menerapkan hasilnya, dan **24 Editor penerbitan** menelaah buku utuh di tahap akhir. Gerbang terukur: `harness.py --tahap akhir` (G-GAYA-AJAR) dan G-STRUKTUR.

## 1. Komunikatif dan interaktif

- **Menyapa pembaca dengan *kita*** (keputusan penulis 2026-11-10). Kalimat ditulis seolah-olah penulis sedang berdialog dengan pembaca dan mengerjakan langkahnya bersama: *kita hitung*, *kita lihat hasilnya*, *kita perlu bertanya*. Kata *Anda* tidak dipakai di prosa bab; perintah di latihan ditulis sebagai kalimat perintah tanpa kata ganti (*Hitunglah …*, *Bandingkan …*). Buku lain boleh memilih sapaan lain dengan mengubah `sapaan` di `konfig.json` dan mencatatnya di `KEPUTUSAN-RANCANGAN.md`.
  - ✗ *Rata-rata sampel dihitung dengan menjumlahkan semua pengamatan.* → ✓ *Untuk mendapatkan rata-rata, kita jumlahkan semua pengamatan, lalu bagi dengan banyaknya.*
  - ✗ *Pembaca diharapkan memeriksa asumsi kenormalan.* → ✓ *Sebelum memakai uji ini, kita periksa dulu apakah datanya kira-kira normal.*
- **Pertanyaan yang mengajak berpikir** di tempat pembaca biasanya ragu: *Apa yang terjadi bila sampelnya dua kali lebih besar?* Pertanyaan itu langsung dijawab atau dijadikan aktivitas singkat. Subjudul tetap berupa frasa, bukan kalimat tanya (G-JUDUL).
- **Kalimat aktif** lebih dulu. Kalimat pasif dipakai bila pelakunya tidak penting (*Data dikumpulkan BPS setiap Maret.*). Hindari menulis tumpukan pasif berpelaku tersembunyi seperti di artikel.
- **Kata *pembaca* sebagai pelaku diganti sapaan.** *Pembaca dapat melihat …* → *Kita dapat melihat …*. Kata *pembaca* tetap boleh di prakata dan petunjuk penggunaan.
- **Batas dialog.** Sapaan bukan komentar meta. Hindari pengumuman kosong (*Mari kita lihat …*, *Pada bab ini kita akan …*, *Seperti yang akan kita lihat …*), karena G-SLOP tetap menolaknya. Langsung kerjakan: *Kita hitung rata-ratanya.* Hindari juga basa-basi pujian (*Selamat, Anda telah …*) dan kalimat perintah beruntun tanpa penjelasan.

## 2. Semi-formal

- **Kosakata baku EYD V** (skill eyd): tanpa ragam cakapan (*nggak, banget, kayak*), tanpa singkatan obrolan, istilah sesuai `keputusan-istilah.md`.
- **Struktur kalimat mengalir, pendek, tidak berbelit.** Satu gagasan per kalimat. Panjang kalimat rata-rata ±12–20 kata, dan tidak ada kalimat lebih dari 35 kata. Anak kalimat bertumpuk (*yang …, yang …, yang …*) dipecah. Kalimat pendek dipakai untuk penekanan.
- **Paragraf pendek** (2–6 kalimat, G-PARAGRAF), dibuka kalimat topik, dan disambung kata hubung yang tepat (skill eyd, `kata-hubung.md`).
- **Contoh dekat dengan pembaca**: konteks Indonesia, angka yang masuk akal, dan data yang statusnya disebut.

## 3. Penjelasan istilah

- **Setiap istilah teknis atau asing dijelaskan langsung pada kemunculan pertama di setiap bab**: arti dalam kata sehari-hari, lalu contoh singkat. Istilah asing dicetak miring (`istilah-statistika.md`).
  - ✓ *Galat baku (*standard error*) mengukur seberapa jauh rata-rata sampel biasanya meleset dari rata-rata populasi. Bayangkan kita mengambil banyak sampel …*
- **Satu istilah baru per kalimat.** Istilah yang belum dijelaskan tidak dipakai untuk menjelaskan istilah lain.
- **Glosarium**: setiap istilah yang dijelaskan masuk `keputusan-istilah.md` dan glosarium buku dengan arti singkat yang sama dengan penjelasan di bab. Istilah yang dijelaskan di bab lain cukup diingatkan singkat dengan jembatan istilah.
- Rumus dan simbol mengikuti `rumus-dan-simbol.md`: setiap simbol diterangkan pada kemunculan pertama.

## 4. Rujukan seperlunya (gaya buku ajar, bukan artikel)

Tujuannya adalah **menghapus sitasi dari prosa, bukan menghapus dasar**. Setiap klaim tetap tercatat di registri klaim (`harness/klaim.json`) beserta kutipan verbatimnya. Yang berubah hanya tampilannya di buku.

| Jenis kalimat | Keputusan | Alasan |
|---|---|---|
| Kutipan langsung, definisi yang dikutip, angka atau data dari sumber lain, tabel/gambar yang diadaptasi | **pertahankan** sitasi di kalimat | hak cipta dan keterlacakan angka |
| Hasil yang khas satu sumber, masih diperdebatkan, atau baru (setelah buku teks baku) | **pertahankan** | pembaca perlu tahu asalnya |
| Nama metode, teorema, atau rumus yang dinamai orang, pada kemunculan pertama | **pertahankan sekali** (penulis–tahun) | atribusi |
| Pengetahuan baku yang ada di banyak buku teks (definisi rata-rata, sifat ragam, teorema limit pusat) | **hapus** dari prosa; sumbernya masuk *Bacaan lanjut* | buku ajar tidak mendokumentasikan pengetahuan umum kalimat demi kalimat |
| Beberapa sitasi untuk satu klaim (`[@a; @b; @c]`) | **sisakan satu** sumber terbaik; sisanya ke *Bacaan lanjut* | keterbacaan |
| Sitasi yang hanya menambah wibawa (*sebagaimana dikemukakan para ahli …*) | **hapus** beserta frasanya | basa-basi |
| Sumber yang sama disitasi lagi di kalimat berikutnya dalam paragraf yang sama | **sitasi sekali**, pada kemunculan pertama; kalimat berikutnya tanpa sitasi ("Sumber yang sama juga menunjukkan …", atau cukup tanpa sitasi bila jelas); lokator berbeda digabung di sitasi pertama (`[@k, hlm. 5, 9]`) | keputusan penulis 2026-11-12; G-SITASI-ULANG |

- Sumber yang dihapus dari prosa dikumpulkan di subbab **Bacaan lanjut** di akhir bab (sebelum Latihan), dikelompokkan per topik, dengan satu kalimat alasan untuk setiap sumber. Daftar pustaka buku tetap memuat semuanya.
- Entri registri klaim untuk kalimat yang sitasinya dihapus diberi `"tampil": "bacaan-lanjut"` sehingga G-REFERENSI tetap dapat menelusuri dasarnya.
- **Satu sumber sekali per paragraf** (keputusan penulis 2026-11-12). Entri klaim untuk kalimat yang sitasinya dihapus karena sumbernya sudah disitasi lebih awal di paragraf itu **tidak dihapus**: entri tetap ada (kunci, penanda, bukti) dan diberi `"sitasi_di": "kalimat pertama paragraf (sitasi digabung, 2026-11-12)"`. G-REFERENSI tetap memeriksa buktinya terhadap sumber dan menolak entri `sitasi_di` yang paragrafnya tidak lagi menyitasi `@kunci` sebelum penandanya. Dalam satu paragraf yang sama, sitasi di kalimat pertama juga diterima untuk klaim yang penandanya berada di baris lain paragraf itu. Bila sumbernya manual atau lembaga, tulis faktanya langsung tanpa sitasi, bukan "Panduan yang sama menyatakan" (G-ATRIBUSI). Rujukan silang `@sec-`, `@fig-`, `@tbl-`, `@eq-`, `@lst-` bukan sitasi; butir daftar dihitung terpisah.
- **Kepadatan sasaran** (konfig `sitasi_per_1000_kata_maks`, bawaan 4) dihitung pada prosa isi, di luar *Bacaan lanjut*, kotak, dan keterangan gambar/tabel. Angka ini adalah pegangan kerja, bukan kaidah; bab bersejarah atau bab tinjauan boleh dikecualikan di `pengecualian.json` dengan alasan.

## 5. Struktur bab

1. **Pengantar bab yang menarik**: studi kasus nyata (data atau peristiwa Indonesia yang statusnya disebut) atau cerita pendek (tokoh, situasi, masalah). Panjangnya 120–300 kata, ditaruh sebelum kotak *Tujuan belajar*, berakhir pada pertanyaan yang akan dijawab bab ini, dan dirujuk lagi di contoh utama atau rangkuman. Jangan membuka dengan *Bab ini membahas …* atau definisi. G-STRUKTUR memeriksa keberadaan dan panjangnya; kemenarikannya dinilai peran 22 dan pembaca 10.
2. **Uraian materi dalam subbab ringkas**: satu subbab mengerjakan satu konsep atau langkah. Setiap bagian (di antara dua judul) paling banyak `subbab_maks_kata` kata prosa (bawaan 800). Subbab yang lebih panjang dipecah menurut konsep, bukan dipotong di tengah penjelasan.
3. **Rangkuman di setiap akhir bab**: subbab *Rangkuman* (bab lama yang memakai *Ringkasan* tetap diterima), sebelum *Bacaan lanjut* dan *Latihan*. Isinya 3–7 butir atau 1–2 paragraf (40–450 kata) dengan pesan utama bab dalam bahasa sederhana, satu kalimat yang menjawab pertanyaan pengantar, dan tanpa sitasi.

## 6. Ukuran (G-GAYA-AJAR, `--tahap akhir`)

| Ukuran | Bawaan (`konfig.json`) | Gagal bila |
|---|---|---|
| Sapaan *kita* per 1.000 kata prosa (`sapaan`: "kita") | `sapaan_per_1000_kata_min`: 3 | di bawah ambang |
| Kata *Anda* di prosa bab bila `sapaan` = "kita" | `anda_maks`: 0 | di atas ambang (dilaporkan per kalimat) |
| Kata *pembaca* sebagai pelaku di prosa bab | `pembaca_pelaku_maks`: 3 | di atas ambang |
| Rata-rata panjang kalimat | `rerata_kata_kalimat_maks`: 20 | di atas ambang |
| Kalimat terpanjang | `kalimat_maks_kata`: 35 | ada kalimat lebih panjang (dilaporkan) |
| Sitasi per 1.000 kata prosa isi | `sitasi_per_1000_kata_maks`: 4 | di atas ambang |
| Sumber yang disitasi lebih dari sekali dalam satu paragraf (G-SITASI-ULANG; WARNING pada tahap draf) | 1 kali per paragraf | ada kunci ≥ 2 kali (dilaporkan per baris, kunci, jumlah, dan saran gabung lokator) |
| Istilah miring tanpa penjelasan dekat kemunculan pertama dan tanpa entri `keputusan-istilah.md` | — | dilaporkan (WARNING untuk peran 22/23) |

## 7. Daftar periksa peran 22 dan 23
- [ ] Pengantar bab berupa studi kasus nyata atau cerita pendek, 120–300 kata, berakhir pada pertanyaan bab, dan dirujuk lagi kemudian.
- [ ] Prosa menyapa pembaca dengan *kita* (tanpa *Anda*) dan tanpa komentar meta; kalimat aktif lebih dulu.
- [ ] Kosakata baku; kalimat pendek dan mengalir; paragraf 2–6 kalimat.
- [ ] Setiap istilah teknis/asing dijelaskan pada kemunculan pertama di bab dan ada di glosarium.
- [ ] Sitasi tersisa hanya untuk kutipan, angka/data sumber lain, hasil khas/diperdebatkan, dan atribusi nama metode; sisanya di *Bacaan lanjut*; registri klaim mencatat `"tampil": "bacaan-lanjut"`.
- [ ] Subbab ringkas (≤ 800 kata per bagian), satu konsep per subbab.
- [ ] Satu sumber disitasi sekali per paragraf (G-SITASI-ULANG LULUS pada `--tahap akhir`); kalimat lanjutan dari sumber yang sama tanpa sitasi, entri klaimnya tetap di registri dengan `"sitasi_di"`.
- [ ] Rangkuman di akhir bab, tanpa sitasi, menjawab pertanyaan pengantar.
- [ ] Angka tetap dihitung kode (G-ANGKA), rumus dan simbol tetap benar (G-RUMUS), dan tidak ada klaim baru tanpa registri.
