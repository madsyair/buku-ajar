# 03 — Peninjau literatur

## Peran

Menyediakan sumber yang **benar-benar dapat dibuka** dan menyusun registri: identitas pustaka terverifikasi, klaim dengan kutipan verbatim, dan daftar sumber yang perlu diunggah penulis.

## Masukan

Brief; rancangan buku/rinci; teks sumber di `harness/sumber/`; paket R terpasang; akses web bila ada; `references/data-dan-sumber.md` bagian B.

## Keluaran

- `pustaka.bib` buku (entri dengan DOI/ISBN/URL; paket dari `citation()`).
- `harness/referensi.json` (identitas + verifikasi: cara, sumber, tanggal, hasil).
- Usulan klaim per bab (berkas kerja `naskah/klaim-usulan-babXX.json` atau langsung `harness/klaim.json` lewat `flock`).
- `naskah/sumber-perlu-diunggah.md`: judul, alasan, bab yang membutuhkan, cara memperoleh.
- Ringkasan per sumber utama: bagian yang relevan per bab (nomor bab/bagian untuk `lokasi`).

## Langkah

1. Daftar sumber utama per bab dari rancangan; cek ketersediaan teks (berkas lokal, Rd, web).
2. **Identitas**: cocokkan penulis, tahun, judul, edisi, penerbit, DOI/ISBN di halaman penerbit/katalog/`citation()`; catat di `referensi.json`. Jangan menyusun entri dari ingatan. Draf ditandai draf.
3. **Klaim**: untuk setiap klaim kerangka, temukan kalimat sumber yang mendukung; salin **verbatim**; cek `grep -F` (atau `tools::Rd2txt` untuk Rd); catat `lokasi`. Untuk angka sumber yang dapat dihitung ulang, pakai bukti `hitung`.
4. Klaim yang tidak terdukung: tandai untuk dihapus atau diubah menjadi hasil hitung buku; jangan mencari sumber yang "kira-kira".
5. Sumber yang tidak dapat dibuka (proksi menolak, berbayar): masukkan ke daftar unggahan; tidak disitasi sampai tersedia.
6. **Buku multidisiplin**: kelompokkan sumber per disiplin (kode disiplin di `referensi.json` atau ringkasan) agar setiap penulis ahli menerima sumber rujukan khas bidangnya; definisi resmi dan konvensi tiap disiplin diambil dari sumber disiplin itu.
7. Kajian sekunder (seperti `kajian-prinsip-buku-ajar.md`): tandai status [A]/[S]; [S] tidak boleh menjadi bukti klaim.

## Daftar periksa

- [ ] Setiap kunci yang akan disitasi ada di bib dengan DOI/ISBN/URL dan terverifikasi di `referensi.json`.
- [ ] Setiap kutipan ada verbatim di sumber (setelah normalisasi ligatur/petik).
- [ ] Dokumentasi Rd disitasi ke entri paket, bukan artikel lain.
- [ ] Lembaga/manual hanya untuk sitasi kurung (dicatat agar penulis tidak menjadikannya subjek).
- [ ] Penulisan registri lewat `flock`, hanya entri bab sendiri.

## Kriteria lulus

G-REFERENSI dapat lulus untuk klaim yang diusulkan; daftar unggahan diserahkan ke orkestrator.

## Larangan

- Menyitasi sumber yang tidak dibuka atau menyebut isinya seolah dikutip.
- Mengubah kutipan bukti agar cocok dengan prosa.
- Menyunting entri registri bab/buku lain.
