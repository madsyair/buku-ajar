# 15 — Pengaudit ilustrasi

## Peran

Menemukan narasi yang sulit dibayangkan tanpa gambar dan membuat gambar yang benar-benar menambah pemahaman (maks. 2 per bab secara bawaan), untuk satu kelompok bab. Rincian di `references/ilustrasi.md`; baca skill **dataviz** sebelum kode gambar pertama.

## Masukan

Bab kelompok sendiri (qmd dan PDF); brief dan keputusan istilah buku; `_bersama/gaya_gambar.py`, `_bersama/tikz-preamble.tex`; contoh pola gambar di bab lain buku yang sama.

## Keluaran

`<buku>/naskah/audit-ilustrasi.md` (per bab: lokasi, alasan, jenis gambar, putusan dibuat/tidak beserta alasan); gambar baru di bab (chunk R → parquet, chunk Python atau TikZ, judul, Div catatan, kalimat rujukan); laporan ≤ 200 kata.

## Langkah

1. Baca bab seluruhnya; tandai kandidat: proses bertahap, bentuk/geometri yang hanya dijelaskan kata, perbandingan kondisi yang tidak diperlihatkan, struktur model tanpa DAG, tabel panjang yang polanya lebih jelas sebagai grafik, analogi yang butuh skema.
2. Tolak kandidat yang mengulang gambar yang ada atau tidak menambah pemahaman; catat alasannya.
3. Buat gambar: angka dihitung R dari objek bab; Python hanya membaca parquet; TikZ dengan warna seri dan gaya DAG buku; judul ≤ 12 kata, panel (a)(b) dengan `label_panel()`; catatan ≥ 2 kalimat; label unik `fig-…` bersufiks bab; lebar ≤ 5,2 inci.
4. Rujuk gambar di prosa sebelum muncul; narasinya hanya yang tampak dan dihitung.
5. Harness setiap bab yang diubah sampai LULUS, **tanpa** `--render`.

## Daftar periksa

- [ ] ≤ 2 gambar baru per bab (kecuali bab sangat miskin gambar, dengan alasan).
- [ ] Narasi cocok dengan gambar; ciri yang disebut dihitung.
- [ ] Tidak ada perubahan isi/angka bab selain kalimat rujukan dan penghubung.

## Kriteria lulus

Audit tercatat; harness LULUS; setelah render (orkestrator), pembaca/editor tidak menemukan MAYOR tampilan.

## Larangan

Mengubah isi atau angka bab; menulis "Sokratik/Feynman/Socrates"; menjalankan `--render`; mengubah bab di luar kelompok; klaim/pengecualian tanpa `flock`.
