# Brief <Buku N> — <Judul>

Dokumen ini dibaca setiap agen sebelum mengerjakan bab <Buku N>. Yang mengikat, berurutan dari yang paling berlaku:

1. `../../KEPUTUSAN-RANCANGAN.md` (keputusan penulis bertanggal; entri yang relevan: …).
2. `naskah/01-rancangan-rinci.md` (bab, isi, data, contoh utama, rujukan "Ingat", sumber, anggaran).
3. Rancangan seri/buku: `<jalur>` (bagian …).
4. Brief ini, `naskah/keputusan-istilah.md`, pola buku lain (`../<buku-lain>/naskah/00-brief.md`).

Status keputusan: butir yang ditandai **(perancangan)** diputuskan agen saat perancangan dan dapat diubah penulis; jangan menyebutnya "keputusan penulis".

## Pembaca dan perangkat

- Pembaca sasaran: <siapa; prasyarat; buku yang sudah dibaca; boleh melompat buku?>.
- Profil pembaca uji: pemula <…>; menengah <…>; mahir <…>.
- Perangkat dan versi teruji (uji asap <tanggal>): <R x.y; paket; mesin; perintah lingkungan>.
- Tebal: ±<…> halaman isi (anggaran per bab di bawah; anggaran, bukan batas keras).

## Instruksi gaya dari penulis (wajib)

1. EYD V di seluruh naskah; desimal koma di prosa, titik di kode.
2. Istilah: Indonesia bila padanannya lazim; istilah Inggris miring bila belum lazim, dijelaskan dengan kata sehari-hari pada kemunculan pertama di setiap bab. Rincian `naskah/keputusan-istilah.md`. Verba tidak hibrida.
3. Istilah baru dijelaskan utuh (arti sehari-hari, alasan, contoh angka); satu istilah baru per kalimat.
4. **Alur digerakkan pertanyaan pembaca**: setiap subbab dibuka dengan pertanyaan wajar yang muncul di kepala pembaca (kalimat tanya di kalimat pertama prosa), dijawab dengan penjelasan sederhana, analogi berbatas, dan contoh angka sebelum rumus; setiap subbab harus dapat dijelaskan ulang pembaca dalam beberapa kalimat sederhana. Judul bab dan subjudul **bukan** kalimat tanya. Metode pengajaran ini tidak diberi nama di naskah.
5. Pola tiga langkah: intuisi → rumus → interpretasi dengan angka dari kode.
6. Paragraf 2–6 kalimat; tanpa basa-basi (G-SLOP); tanpa "di mana" sebagai penghubung.
7. Contoh dari pengetahuan umum dan konteks Indonesia.

## Batas buku

- Satu topik, satu pemilik. Buku ini memiliki: <…>. Dirujuk saja (kotak "Ingat dari Buku N, Bab M", maks. satu paragraf, ≤ 2 per bab): <…>.
- Tidak menurunkan ulang: <…>.

| Aspek | Pemilik | Peran di buku lain |
| --- | --- | --- |
| … | … | … |

## Struktur bab

1. `# Judul Bab {#sec-…}` (frasa nomina, kapital tiap kata utama) dan chunk setup tersembunyi (`assets/templat-bab.qmd`).
2. Pembuka; kotak Ingat; kotak Tujuan belajar (3–5 butir berkata kerja terukur).
3. Isi; kotak Penurunan.
4. Contoh utama enam langkah: Pertanyaan dan data, Model, Hitung, Periksa, Interpretasikan, Uji kepekaan.
5. Ringkasan (≤ 1 halaman, ditutup tafsiran bagi pembaca terapan); Latihan: Konseptual, Penurunan sederhana, Hitungan, Pemrograman; satu "tiru alurnya"; minimal satu soal campuran berjarak.

## Aturan kode, angka, gambar

- Angka hasil hitung dari R inline (G-ANGKA); komentar kode bukan keluaran (G-KELUARAN); baris R ≤ 72, Python ≤ 79; keluaran ≤ 78.
- Label unik bersufiks bab: `fig-…-<kode>-XX`, `tbl-…`, `eq-…`, `sec-…`; chunk `setup-<kode>babXX`.
- Model: `seed`, `chains = 4`, `refresh = 0`, `silent = 2`, `file = file.path("fit", "<kode>-XX-nama")`, `file_refit = "on_change"`.
- Gambar: R → `data-gambar/<buku>-babXX-*.parquet` → Python `gaya_gambar` (palet `<PALET>`); TikZ untuk diagram/DAG (warna `<…>`).
- Judul tabel/gambar ≤ 12 kata, satu frasa; panel (a)(b); Div `.catatan` ≥ 2 kalimat.

## Data

- Urutan: riil → sintetis paket → simulasi sendiri (seed tetap); status disebut saat diperkenalkan; tidak mengarang angka lembaga.
- Data per bab: `01-rancangan-rinci.md`. Data lembaga yang menunggu unggahan penulis: <…>.
- Prakata memuat "Data yang digunakan dan batasannya"; lampiran Sumber Data ditulis setelah bab terakhir.

## Referensi

- Sumber yang boleh disitasi (teks tersedia di `harness/sumber/` atau dokumentasi paket): <kunci: berkas>.
- Sitasi penulis–tahun tanpa lokasi; subjek hanya penulis orang; setiap kalimat bersitasi tercatat di `harness/klaim.json` (kutipan verbatim) lewat `flock <scratchpad>/klaim.lock`.

## Harness

```bash
<perintah lingkungan>
python3 harness/harness.py --buku <buku> --bab bab01      # JANGAN --render (orkestrator)
```

Setelah LULUS dan ulasan selesai: orkestrator menambahkan bab ke `chapters` dan ke `lampiran-kode/README.md`.

## Anggaran halaman

| Bab | Hlm. | Bab | Hlm. |
| --- | --- | --- | --- |
| 1 | … | … | … |

Perkiraan: ±400 kata prosa per halaman; satu gambar ½ halaman; 15 baris kode ≈ ⅓ halaman. Kejelasan didahulukan; pemangkasan hanya untuk pengulangan.

## Versi perangkat

<daftar versi dan hasil uji asap>
