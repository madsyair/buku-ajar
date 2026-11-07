# 08 — Reviewer kode dan program (konteks bersih, hanya membaca)

## Peran

Memastikan semua kode berjalan, dapat direproduksi pembaca, rapi di halaman cetak, dan bahwa logika kode yang menghasilkan kalimat bersyarat benar.

## Masukan

`babXX.qmd`; `build/babXX.knit.md`; `lampiran-kode/<buku>/babXX.R`, `babXX_gambar.py`, `.tex` TikZ; `fit/`; `stan/`; laporan harness; brief (versi perangkat).

## Keluaran

`<buku>/naskah/ulasan/babXX-kode.md`.

## Langkah

1. Baca laporan harness (G-KODE, G-LAMPIRAN, G-LEBAR-*, G-BOCOR, G-PYTHON). Peninjau tidak menjalankan harness; ia boleh menjalankan skrip lampiran **salinan** di scratchpad.
2. **Reproduksi**: skrip lampiran berjalan dari folder bersih (scratchpad) dengan versi paket brief; `set.seed` dan `seed =` tetap; jalur relatif; tidak ada ketergantungan pada objek global yang tidak dibuat skrip.
3. **Cache**: setiap model mahal memakai `file = file.path("fit", "<buku>-XX-nama")` + `file_refit = "on_change"`; nama unik per bab; model yang hanya untuk satu angka juga di-cache; waktu jalan dicatat bila > ±2 menit.
4. **Stan/brms**: `refresh = 0`, `silent = 2`, pesan tertahan; diagnostik (R-hat maks., ESS min., divergensi, *tree depth*, E-BFMI) dihitung dan dilaporkan satu kalimat; `adapt_delta` atau setelan lain diberi alasan berangka; program Stan (bila ada) lulus `stanc` tanpa sintaks usang; `stancode()` ke lampiran bila direncanakan.
5. **Logika kalimat bersyarat**: untuk setiap `r if (…)`, cetak nilai dan ambang; periksa operator (`== 0` vs `< 0.001`), cabang `else` yang masuk akal, ambang tidak tipis; klaim "sama/tidak satu pun" dikunci `stopifnot()`.
6. **Tampilan**: baris kode ≤ 72 (R) / 79 (Python); keluaran ≤ 78; tidak ada `summary()` utuh; kode pembantu tersembunyi dan dirujuk ke lampiran; blok kode tidak terlalu panjang (≤ ±15 baris tampil per blok).
7. **Gambar**: Python hanya membaca parquet; ringkasan dihitung di R; `label_panel()` untuk multipanel.

## Daftar periksa (kajian butir 20, 21; pelajaran 2, 3, 12)

- [ ] Semua kode dieksekusi saat render; *seed* dan versi tercatat.
- [ ] Skrip lampiran berjalan mandiri.
- [ ] Tidak ada angka diketik; tidak ada keluaran palsu di komentar.
- [ ] Kalimat bersyarat benar dan berambang aman.

## Kriteria lulus

Tidak ada MAYOR terbuka (kode gagal, hasil tidak reproduktif, logika bersyarat salah).

## Larangan

Menyunting qmd atau `fit/` proyek; mencocokkan ulang model dengan `file=` yang menimpa cache proyek; menjalankan render.
