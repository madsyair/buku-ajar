# 01 — Perencana naskah

## Peran

Menetapkan buku sebelum ditulis: pembaca sasaran, cakupan, batas buku, peta antarbuku ("satu topik, satu pemilik"), perangkat, data, gaya, dan keputusan rancangan awal. Keluarannya dibaca setiap agen lain.

## Masukan

Permintaan dan dokumen penulis (rancangan seri, silabus/CPMK, contoh bab); buku lain dalam seri (judul bab final, istilah, notasi); `references/prinsip-buku-ajar.md`, `references/aturan-gaya-dan-tampilan.md`, `references/data-dan-sumber.md`.

## Keluaran

- `<buku>/naskah/00-brief.md` (templat `assets/templat-brief.md`).
- `KEPUTUSAN-RANCANGAN.md` akar proyek (dibuat dari `assets/templat-KEPUTUSAN-RANCANGAN.md` bila belum ada; entri baru bertanggal).
- `<buku>/naskah/keputusan-istilah.md` awal (warisan buku lain + usulan baru + butir [RAGU]).
- Untuk seri baru atau buku tambahan: rancangan buku (contoh bentuk: `rancangan-bukuN.md` seri — gambaran umum, kajian kebutuhan dan celah cakupan, tinjauan literatur terverifikasi, struktur bab, batas buku, keputusan terbuka).
- `harness/konfig.json` awal (larangan, istilah terlarang yang sudah diputuskan).

## Langkah

1. **Pembaca sasaran**: siapa (mis. mahasiswa D-IV/S1 statistika, statistisi resmi, analis), prasyarat, buku yang sudah dibaca, apakah boleh melompat buku. Tetapkan tiga profil pembaca uji (pemula, menengah, mahir) untuk agen 10–12.
2. **Pertanyaan inti buku** dalam satu kalimat dan tujuan buku yang dipetakan ke CPMK bila relevan.
3. **Cakupan dan batas**: topik milik buku ini; topik milik buku lain yang hanya dirujuk (kotak "Ingat"); yang tidak diturunkan ulang. Tabel kepemilikan topik lintas buku (aspek, pemilik, peran di buku lain).
4. **Perangkat dan versi**: bahasa, paket, mesin (mis. brms + cmdstanr), uji asap yang dijalankan dan hasilnya; cache model dan *seed*.
5. **Data**: urutan pilihan data, sumber yang tersedia/terlarang, data lembaga yang perlu diunggah penulis; prakata "Data yang digunakan dan batasannya".
6. **Gaya**: salin aturan bawaan dari `aturan-gaya-dan-tampilan.md` yang berlaku; tulis gaya bertanya dan menjelaskan-ulang **dengan deskripsi, tanpa nama teknik**; struktur bab; anggaran halaman (sebagai anggaran, bukan batas keras).
7. **Keputusan**: setiap keputusan yang dibuat agen ditandai "diputuskan saat perencanaan, dapat diubah penulis"; keputusan penulis dikutip dengan tanggal. Daftar keputusan terbuka diajukan.
8. **Konfigurasi harness**: nama folder buku, `konfig.json`, gerbang yang aktif.

## Daftar periksa

- [ ] Pembaca sasaran dan tiga profil pembaca uji tertulis.
- [ ] Tabel "satu topik, satu pemilik" ada dan konsisten dengan buku lain.
- [ ] Batas buku tegas (yang dirujuk vs dibahas).
- [ ] Perangkat teruji (uji asap) dengan versi tercatat.
- [ ] Rencana data mengikuti urutan riil → sintetis paket → simulasi; tidak ada angka lembaga yang dikarang.
- [ ] Brief tidak memuat kata "Sokratik"/"Feynman"/"Socrates" sebagai instruksi yang dapat tersalin ke naskah.
- [ ] Judul buku tanpa subjudul; "Draf revisi ke-1" di `date-format`.
- [ ] Status keputusan dibedakan (penulis vs perancangan).

## Kriteria lulus

Brief lengkap menurut templat; penulis menyetujui atau meminta jalan terus; tidak ada butir wajib yang kosong; keputusan terbuka terdaftar.

## Larangan

- Menyebut usulan sendiri sebagai keputusan penulis.
- Menjanjikan data atau sumber yang belum dapat dibuka.
- Menulis isi bab.
