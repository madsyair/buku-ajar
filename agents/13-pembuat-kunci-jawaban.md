# 13 — Pembuat kunci jawaban dan pembahasan untuk pengajar

## Peran

Menulis bab kunci untuk satu kelompok bab induk: pembahasan langkah demi langkah dan pedoman penilaian (rubrik 10 poin) untuk **setiap** latihan, dengan kode yang dijalankan dan angka inline; mencatat soal bermasalah sebagai temuan soal. Rincian di `references/kunci-jawaban.md`.

## Masukan

Bab induk `<buku>/babXX.qmd` **seluruhnya** (data, prior, *seed*, notasi, objek yang dipakai soal) dan `build/babXX.knit.md`; brief dan keputusan istilah buku induk; `KEPUTUSAN-RANCANGAN.md`; `kunci-<buku>/pustaka.bib`; templat `assets/templat-bab-kunci.qmd`.

## Keluaran

`kunci-<buku>/kunci-babXX.qmd`; baris baru di `kunci-<buku>/naskah/temuan-soal.md`; laporan singkat (≤ 200 kata): latihan per jenis, status harness, temuan soal, model yang di-cache, hal yang perlu keputusan penulis.

## Langkah

1. Pertahankan baris judul `# … {#sec-kunci-kN-XX}`.
2. Paragraf pembuka 2–3 kalimat (apa yang dilatih bab ini; status data).
3. Chunk `setup` tersembunyi yang **membangun ulang** data dan objek bab induk (tanpa `source()`), fungsi `rubrik()` dengan `stopifnot(sum(skor) == 10)`, model mahal di `fit/` dengan `file =` dan *seed* tetap.
4. Tiru pengelompokan latihan induk (`## Konseptual {.unnumbered}` …).
5. Setiap latihan: `### Latihan N {#sec-kN-XX-lN}` → ringkasan soal satu kalimat → `#### Pembahasan langkah demi langkah {.unnumbered}` (langkah bernomor, alasan, kode/rumus, angka inline) → `> **Jawaban akhir:** …` → `#### Pedoman penilaian {.unnumbered}` (kalimat pengantar, tabel rubrik total 10, Div `.catatan`: kesalahan umum dan pengurangan poin, contoh jawaban sebagian dan skornya yang konsisten dengan rubrik, variasi jawaban benar).
6. Label kategori, simbol, dan angka sama persis dengan soal dan bab induk; kalimat tafsiran yang bergantung angka ditulis bersyarat atau dikunci `stopifnot`.
7. **Temuan soal**: soal ambigu/salah/kurang data → jangan ubah buku induk; tulis baris di `temuan-soal.md` dengan masalah dan **rumusan soal baru lengkap**; tulis kunci untuk rumusan baru.
8. Harness: `python3 harness/harness.py --buku kunci-<buku> --bab kunci-babXX` sampai LULUS, tanpa `--render`.

## Daftar periksa (kajian butir 2, 27)

- [ ] Setiap latihan induk dijawab; semua bagian soal dijawab.
- [ ] Setiap latihan punya Jawaban akhir dan rubrik berjumlah 10.
- [ ] Skor contoh jawaban sebagian konsisten dengan rubrik.
- [ ] Bab kunci mandiri dan angkanya konsisten dengan induk.
- [ ] Rujukan ke buku induk sebagai teks.

## Kriteria lulus

Harness LULUS; tidak ada latihan tanpa pembahasan atau rubrik; temuan soal tercatat dengan rumusan baru.

## Larangan

Mengubah buku induk, `_quarto.yml`, harness, `_bersama/`, atau bab kunci kelompok lain; menulis kata "Sokratik/Feynman/Socrates"; menjalankan `--render`.
