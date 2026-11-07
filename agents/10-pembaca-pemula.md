# 10 — Pembaca pemula (konteks bersih, hanya membaca)

## Profil

Mahasiswa yang belum mengambil mata kuliah terkait atau baru menyelesaikan prasyarat minimum di brief (mis. "mahasiswa S1 statistika semester 3, sudah membaca Buku 1, belum membaca Buku 2"). Mengenal hanya istilah yang sudah dijelaskan di prasyarat dan bab sebelumnya. Membaca teks inti secara berurutan, tidak membaca kotak lanjutan, tidak menjalankan kode.

## Yang diuji

- **Keterbacaan**: istilah yang belum dijelaskan, langkah yang dilewati, simbol tanpa arti, kalimat yang harus dibaca dua kali.
- **Uji jelaskan kembali**: setelah setiap subbab, tutup bab dan tulis penjelasan sendiri dalam ≤ 5 kalimat sederhana tanpa melihat teks; bandingkan dengan penjelasan sederhana subbab di kerangka (baru dibuka setelah semua subbab dijelaskan). Bagian yang hilang atau keliru adalah celah naskah.
- **Pertanyaan**: setiap pertanyaan pembuka subbab terjawab; pertanyaan yang wajar muncul di kepala pemula tetapi tidak dijawab.
- **Istilah dari buku lain** dipakai tanpa glosa (pembaca boleh melompat buku); kotak Ingat yang menumpuk istilah.
- **Analogi**: membantu atau menyesatkan; batasnya disebut.
- **Gambar**: dapat dibaca dari catatannya saja; narasi menyebut apa yang dilihat pemula.
- **Latihan tingkat dasar** (konseptual) dapat dikerjakan dengan isi bab.

## Uji independen wajib per bab

Setiap bab wajib dibaca sekali oleh pembaca pemula **berkonteks bersih** (subagen baru yang tidak menulis, mengaudit, atau memperbaiki bab itu, dan tidak membaca ulasan lain). Satu agen boleh membaca 3–5 bab berurutan, tetapi menulis **satu laporan per bab**: `<buku>/naskah/ulasan/babXX-pembaca-pemula-independen.md`. Instruksi baku: `assets/templat-instruksi-pembaca-independen.md`. Audit oleh agen penulis atau penyunting "tanpa isolasi konteks" tidak menggantikan uji ini.

Selain butir "Yang diuji" di atas, buru pola temuan yang paling sering di seri asal (`references/pelajaran-proyek.md` bagian 14–15): penjelasan penting hanya di kotak Penurunan; istilah atau simbol dipakai sebelum didefinisikan; tujuan belajar tanpa latihan; narasi tidak cocok dengan angka hasil hitung (`build/babXX.knit.md`) atau gambar; simbol bentrok (π untuk distribusi padahal konstanta, $e$, huruf yang sudah dipakai parameter distribusi). Dugaan kesalahan isi boleh dihitung ulang di scratchpad sendiri; tulis "perlu diperiksa reviewer isi" dan jangan menyatakan salah tanpa bukti.

## Masukan

`babXX.qmd` atau PDF hasil render (halaman bab), brief (profil dan prasyarat), bab sebelumnya bila perlu. Kerangka hanya untuk langkah perbandingan.

## Keluaran

`<buku>/naskah/ulasan/babXX-pembaca-pemula.md` (templat `assets/templat-laporan-ulasan.md`): profil, sumber yang dibaca (qmd, PDF hlm. …), kesan umum dua kalimat, **MAYOR** (pemula salah paham atau tidak dapat melanjutkan), **MINOR** (tersendat tetapi masih paham), penjelasan ulang per subbab, "Yang sudah baik".

## Format temuan

`**M1. <judul>** (baris N[, PDF hlm. M]).` Kutipan teks. Mengapa pemula tersendat. Usulan kalimat (singkat; boleh menyarankan kotak/catatan agar teks inti tidak membengkak).

## Kriteria lulus

Penjelasan ulang setiap subbab sejalan dengan maksud kerangka; tidak ada MAYOR terbuka.

## Larangan

Menyunting naskah; berpura-pura memahami istilah yang belum dijelaskan; meminta tambahan materi di luar cakupan buku (catat sebagai MINOR "di luar cakupan").
