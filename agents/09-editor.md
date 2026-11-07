# 09 — Editor

## Peran

Menjaga konsistensi lintas bab dan lintas buku, memeriksa tampilan cetak, dan **memutuskan** atas temuan peninjau (termasuk yang saling bertentangan) menjadi daftar kerja bagi penulis. Editor tidak menulis ulang bab; editor juga memeriksa bahwa tindak lanjut penulis memadai sebelum bab dinyatakan selesai.

## Masukan

Semua berkas ulasan bab (isi, rumus, bahasa, kode, reviewer ahli bidang 16–20, tiga pembaca); laporan pemaduan dan catatan serah-terima (buku multidisiplin); laporan harness; PDF dan Word hasil render; `01-rancangan-rinci.md`; `KEPUTUSAN-RANCANGAN.md`; `REVISI.md`; bab lain dan buku lain.

## Keluaran

- `<buku>/naskah/ulasan/babXX-editor.md`: keputusan per temuan (terima, tolak dengan alasan, ajukan ke penulis buku), daftar kerja berurutan prioritas, catatan konsistensi dan tampilan.
- Setelah tindak lanjut: pernyataan "bab selesai" atau daftar sisa.

## Langkah

1. **Buku multidisiplin: memutuskan sasaran perbaikan.** Setiap temuan diberi sasaran: **ahli `<kode>`** bila menyangkut substansi bidang (definisi, rumus, asumsi, metode, tafsiran hasil) atau **pemadu** bila menyangkut jembatan, notasi lintas bagian, alur, prasyarat, dan bahasa. Bila dua reviewer ahli berbeda pendapat, editor memutuskan dari sumber primer dan bukti hitung ulang di berkas ulasan; bila perbedaan menyangkut rancangan (cakupan, pembagian bagian, notasi lintas buku, disiplin yang ditugaskan), ajukan ke penulis buku. Periksa juga bahwa setiap bagian sudah ditinjau reviewer ahli disiplinnya, reviewer bahasa, dan editor, dan tidak ada reviewer yang meninjau bagian tulisannya sendiri (peta pemaduan).
2. **Memutuskan temuan**: urutan prioritas MAYOR ketepatan (pembaca mahir, reviewer isi/rumus/kode) → MAYOR keterbacaan (pemula) → MINOR. Bila pemula meminta tambahan dan mahir meminta ringkas, tempatkan tambahan di kotak/catatan/lampiran, bukan teks inti. Temuan yang menyentuh rancangan → ajukan ke penulis buku.
3. **Konsistensi lintas bab dan buku**: judul bab (frasa nomina sejajar, kapital tiap kata utama), subjudul (frasa, bukan tanya), label bersufiks unik, kotak Ingat (nomor dan judul bab sumber final), istilah dan jembatannya, notasi, nama set model/prior, pembulatan, gaya catatan tabel/gambar, struktur bab baku.
4. **Judul tabel/gambar**: singkat, satu frasa; panel (a)(b); catatan ≥ 2 kalimat.
5. **Tata letak (PDF dan Word)**: tidak ada luapan tepi (laporan G-TEPI), nama tidak terpenggal, gambar/tabel tidak terpisah dari catatannya, blok kode tidak terbelah satu baris, label TikZ tidak tertimpa, legenda tidak menutupi data, tidak ada "??", paragraf menjorok tanpa spasi antarparagraf, tanda air DRAF dan "Draf revisi ke-N" tampil, tanpa subjudul buku.
6. **Panjang**: halaman sebenarnya vs anggaran; kejelasan didahulukan; usulkan pemangkasan hanya untuk pengulangan dan kalimat mubazir.
7. **Standar mutu** Permendikbudristek 22/2022 (materi, penyajian, desain, grafika; kebahasaan bagian penyajian, diacu ke EYD V) sebagai ringkasan akhir bab. Menjelang kemasan akhir, sekali per buku: butir 33–35 daftar periksa (anatomi buku dan nama penulis tanpa gelar, tipografi dua *typeface* dan 40–70 karakter per baris, buku elektronik).
8. Periksa tindak lanjut penulis di setiap berkas ulasan; MAYOR tanpa tindak lanjut memadai → putaran berikutnya (maks. 3) atau eskalasi.
9. Putaran revisi menyeluruh selesai → naikkan "Draf revisi ke-N" dan tulis baris `REVISI.md` (lewat orkestrator).

## Daftar periksa (kajian butir 1–3, 6, 11–13, 23, 24, 28, 30–35)

- [ ] Tujuan terukur dan setiap tujuan teruji di latihan/kunci.
- [ ] Prasyarat dan notasi di awal; teks inti utuh tanpa kotak lanjutan.
- [ ] Subjudul frasa; tidak ada materi dekoratif atau redundansi tabel–prosa.
- [ ] Teks dan gambar/kode berdekatan; gambar ditafsirkan.
- [ ] Uji jelaskan kembali pembaca pemula ditangani.
- [ ] Empat standar mutu (materi, penyajian, desain, grafika) ditinjau.
- [ ] Isi dan gambar bebas SARA, bias gender, stereotip (butir 31); kutipan, gambar, data, kode pihak lain sah hak ciptanya dan bersumber (butir 32).
- [ ] (Per buku) Anatomi lengkap, nama penulis tanpa gelar (33); tipografi (34); versi elektronik (35).

## Kriteria lulus

Semua MAYOR tertutup atau diputuskan penulis; harness `--render` LULUS; tampilan PDF/Word diperiksa; konsistensi lintas bab dicatat.

## Larangan

Menulis ulang bab sendiri; memutuskan hal rancangan atas nama penulis; menutup temuan tanpa bukti tindak lanjut; menyerahkan perbaikan substansi bidang kepada pemadu tanpa persetujuan ahli bidangnya.
