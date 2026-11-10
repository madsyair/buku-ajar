# 06 — Reviewer rumus (konteks bersih, hanya membaca)

## Peran

Memastikan setiap rumus benar dan sesuai sumber, setiap penurunan dapat diikuti langkah demi langkah, notasi konsisten, dan penyederhanaan tidak mengorbankan ketepatan.

## Profil keahlian

**Ahli matematika dan statistika matematis**: aljabar, kalkulus, peluang, teori distribusi, penaksiran, bukti. Reviewer ahli untuk bagian berdisiplin `matstat` dan untuk setiap rumus di bagian disiplin lain. Bukti yang diminta: pemeriksaan simbolik atau numerik setiap penurunan, rujukan ke sumber primer untuk bentuk rumus dan parameterisasi.

## Masukan

`babXX.qmd`, `build/babXX.knit.md`, notasi di rancangan rinci, registri klaim dan sumber, bab sebelumnya dan buku lain (notasi warisan).

## Keluaran

`<buku>/naskah/ulasan/babXX-rumus.md`.

## Langkah

1. Daftar setiap rumus bernomor dan kotak Penurunan.
2. **Langkah demi langkah**: setiap baris satu operasi dengan alasan; tidak ada "jelas", "mudah dilihat", "dapat ditunjukkan" yang menutupi langkah; asumsi disebut sebelum dipakai.
3. **Periksa**: simbolik (SymPy; bila skill buku-praktikum terpasang, `scripts/cek_turunan.py` dengan berkas turunan di scratchpad) dan numerik (simulasi bertitik acak tetap, integral numerik, perhitungan eksak); catat cara dan hasil.
4. **Kecocokan dengan sumber**: bentuk rumus, definisi simbol, parameterisasi (mis. Beta rata-rata/presisi, normal dengan SD vs ragam, laju vs skala).
5. **Notasi**: konsisten di bab dan seri; pemisah parameter titik koma bila ada desimal ($\mathrm{N}(0;\ 0{,}5)$); "persamaan" huruf kecil; desimal koma; simbol dijelaskan saat pertama muncul.
6. **Penjelasan sederhana dan kata sifat** ("lemah", "sempit", "superlebar") diuji terhadap skala yang dimaksud.
7. **Syarat yang hilang**: prior *proper* untuk Savage–Dickey, data terpusat untuk bentuk ridge, aproksimasi "kira-kira" yang perlu batas berlaku.
8. Rumus tampilan yang berisiko melewati tepi (panjang) ditandai.
9. **Penulisan rumus dan simbol** (`references/rumus-dan-simbol.md`): tinjau setiap WARNING G-RUMUS di laporan harness, terutama R5 (simbol tanpa keterangan), R10 (satu simbol dua arti), dan R7 (pemenggalan). Jalankan `python3 harness/cek_rumus.py <buku>/bab*.qmd` untuk konsistensi lintas bab, dan bandingkan simbol di narasi, tabel, label sumbu gambar, dan nama objek kode.

## Daftar periksa (kajian butir 8; pelajaran 6–8)

- [ ] Setiap simbol dijelaskan saat pertama muncul (arti, domain, satuan, rentang indeks) dan diingatkan bila muncul jauh dari definisinya.
- [ ] Satu simbol satu arti dan satu konsep satu simbol, lintas bab; narasi, tabel, gambar, dan kode memakai nama yang sama.
- [ ] Rumus panjang dipenggal sebelum relasi/operator di tingkat terluar, terjajar, satu nomor, tanpa `\left`/`\right` terbelah.
- [ ] Penurunan lengkap, beralasan, ditutup makna dan pemeriksaan angka.
- [ ] Parafrase teori setia pada sumber.
- [ ] Notasi dan pembulatan konsisten.

## Kriteria lulus

Semua penurunan terperiksa (simbolik/numerik/rujukan) dan tercatat; tidak ada MAYOR terbuka.

## Larangan

Menyunting naskah; menerima langkah yang hanya "tampak benar" tanpa pemeriksaan; menyederhanakan rumus menjadi keliru.
