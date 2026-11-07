# Ilustrasi: gambar data, diagram, dan audit

Dipakai oleh penulis, reviewer isi, dan `agents/15-pengaudit-ilustrasi.md`. Sebelum menulis kode gambar pertama di proyek, baca skill **dataviz** untuk palet, kontras, dan bentuk grafik.

## Dua jalur pembuatan

| Jenis | Alat | Pola |
|---|---|---|
| Gambar data/fungsi (densitas, garis posterior, PPC, peta nilai) | R menghitung, **Python matplotlib/seaborn menggambar** | Chunk R menulis `data-gambar/<buku>-babXX-<nama>.parquet` (`arrow::write_parquet`); chunk Python (`echo: false`, `results: hide`, `dpi: 300`) membaca parquet dan menggambar dengan `gaya_gambar.py`. Ringkasan (kuantil, pita) dihitung di R. |
| Skema, DAG, alur, peta konsep | **TikZ** (chunk `{tikz}`) | Warna seri dari `tikz-preamble.tex`; pustaka `bayesnet` untuk DAG; opsi `fig-ext: !expr if (knitr::is_latex_output()) "pdf" else "png"` dan `engine-opts: !expr list(extra.preamble = readLines("../_bersama/tikz-preamble.tex"))`. |

Alasan pemisahan: angka hanya dihitung di satu tempat (R) sehingga gambar dan prosa tidak pernah berbeda; skrip Python lampiran berjalan mandiri dari parquet (G-LAMPIRAN, G-PYTHON).

Konvensi DAG (dari seri): data teramati lingkaran abu-abu, parameter lingkaran berwarna seri, besaran deterministik belah ketupat, kuantitas turunan lingkaran putus-putus, plat untuk indeks pengamatan/kelompok. Formula model ditulis di keterangan atau prosa agar pembaca melihat hubungan formula–model. Periksa bahwa panah tidak menimpa label plat dan simpul berindeks berada di dalam platnya.

## Keterangan gambar

- Judul ≤ 12 kata, satu frasa; multipanel "Judul: (a) frasa, (b) frasa" (frasa ≤ 6 kata); `label_panel()` dipanggil.
- Judul yang memuat angka dibangun di chunk R tersembunyi lalu dipasang lewat `knitr::opts_chunk$set(fig.cap = …)` sebelum chunk Python dan direset sesudahnya (`fig.cap = NULL`), karena opsi `!expr` tidak dievaluasi di chunk Python (G-BOCOR menangkap keterangan yang tercetak sebagai nama variabel).
- Div `::: {.catatan}` di bawah gambar (≥ 2 kalimat): apa yang digambar, makna warna/garis/pita, data, cara membaca, sumbu yang berbeda antarpanel.
- Prosa merujuk gambar sebelum gambar muncul dan menceritakan **hanya yang tampak**. Ciri yang disebut (mana yang paling lebar, berapa garis keluar pita, arah) dihitung di R dan, bila menjadi dasar kalimat, dikunci dengan `stopifnot` atau kalimat bersyarat.

## Ukuran dan tampilan

- Lebar ≤ 5,2 inci (B5); tinggi 2–3,2 inci; dua panel berdampingan cukup `figsize=(LEBAR, 2.1)`.
- Fon gambar sama dengan fon teks (Libertinus Serif, juga untuk *mathtext*; disematkan Type 3; satu keluarga huruf, lihat `aturan-gaya-dan-tampilan.md` bagian 8); desimal koma di sumbu (`koma_desimal`); tanda minus Unicode.
- Label sumbu bahasa Indonesia, huruf kecil kecuali nama diri; istilah asing di label miring bila memungkinkan (`$\it{…}$`).
- Legenda tidak menutupi data; pindahkan ke luar sumbu bila perlu.
- Warna terang (isian/pita) dibedakan dari warna tua (garis/titik); jangan mengandalkan warna saja untuk membedakan seri (pakai gaya garis atau label langsung).

## Audit ilustrasi (per bab)

Cari narasi yang sulit dibayangkan tanpa gambar:

- proses atau algoritme bertahap (langkah MCMC, *leapfrog*, alur keputusan, alur kerja);
- hubungan geometris atau bentuk distribusi yang hanya dijelaskan dengan kata/angka (ekor, kemencengan, penyusutan, korelasi, corong, campuran);
- perbandingan beberapa kondisi yang disebut di prosa tetapi tidak diperlihatkan (prior lebar vs sempit, sebelum/sesudah, banyak n);
- struktur model (DAG, hierarki, plat) yang belum digambar;
- tabel angka panjang yang polanya lebih jelas sebagai grafik;
- analogi (lift, kelereng, pencacah) yang lebih jelas dengan skema.

Jangan menambah gambar yang mengulang gambar yang ada atau tidak menambah pemahaman. Batas bawaan: **paling banyak 2 gambar baru per bab** kecuali bab sangat miskin gambar; bab yang sudah cukup bergambar boleh tidak ditambah.

Hasil audit dicatat di `<buku>/naskah/audit-ilustrasi.md`: per bab, lokasi (baris/subbab), alasan, jenis gambar yang diusulkan, putusan (dibuat/tidak dibuat beserta alasan). Pengaudit hanya mengubah kalimat rujukan dan penghubung yang perlu; isi dan angka bab tidak diubah.

## Verifikasi

Setiap bab yang diubah: `python3 harness/harness.py --buku <buku> --bab babXX` sampai LULUS, **tanpa** `--render`. Render buku dijalankan orkestrator secara berurutan setelah semua kelompok selesai, lalu pembaca/editor memeriksa tampilan PDF (label tertimpa, legenda menutupi, gambar terlalu kecil, catatan terpisah).
