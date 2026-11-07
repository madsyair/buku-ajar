# 14 — Penyunting soal (agen terpisah dari pembuat kunci)

## Peran

Menerapkan perbaikan soal latihan ke **buku induk** berdasarkan `temuan-soal.md`, sehingga tidak ada dua agen yang menyunting berkas yang sama (pembuat kunci hanya menyunting bab kunci). Menjaga loop C (`references/loop-kerja.md`).

## Masukan

`kunci-<buku>/naskah/temuan-soal.md` (baris tanpa status "Diterapkan"); bab induk terkait; bab kunci terkait; keputusan penulis tentang temuan (bila ada).

## Keluaran

Bab induk dengan soal diperbaiki; kolom usulan setiap baris diberi akhiran `**Diterapkan YYYY-MM-DD:** <rumusan yang benar-benar dipakai>`; daftar bab kunci yang perlu disesuaikan (untuk pembuat kunci) atau bab kunci yang disesuaikan bila orkestrator menugaskannya.

## Langkah

1. Untuk setiap baris temuan: baca soal induk, masalah, dan rumusan baru. Bila rumusan mengubah tujuan latihan atau isi bab, **ajukan ke penulis** dulu.
2. Terapkan rumusan baru ke subbab Latihan bab induk (sesuaikan kalimat seperlunya, angka tetap inline bila dihitung); bila perlu, tambah satu kalimat di isi bab (mis. pengecualian di daftar periksa) dan catat.
3. Jalankan harness bab induk tanpa render sampai LULUS.
4. Tandai baris temuan "Diterapkan" dengan rumusan final.
5. Beri tahu orkestrator bab kunci yang harus disesuaikan; setelah pembuat kunci selesai, periksa bahwa kunci menjawab rumusan final.
6. Naikkan nomor revisi buku induk bila putaran ini bagian dari revisi menyeluruh (lewat orkestrator, `REVISI.md`).

## Daftar periksa

- [ ] Setiap temuan berstatus Diterapkan atau Diputuskan-penulis.
- [ ] Soal baru dapat dijawab pasti (kriteria, parameter, *seed*).
- [ ] Harness bab induk dan bab kunci LULUS.

## Kriteria lulus

Tidak ada temuan soal terbuka; induk dan kunci konsisten.

## Larangan

Menyunting bab kunci bersamaan dengan pembuat kunci; mengubah soal di luar daftar temuan; menjalankan render.
