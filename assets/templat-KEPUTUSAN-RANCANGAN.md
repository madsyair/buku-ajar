# Keputusan rancangan

Berkas ini mencatat keputusan sesudah rancangan seri/buku. Bila bertentangan dengan rancangan, berkas ini yang berlaku. Setiap entri bertanggal, menyebut **siapa yang memutuskan** ("Keputusan penulis" atau "diputuskan saat perancangan, dapat diubah penulis"), cakupan (semua buku/buku tertentu), berlaku surut atau tidak, dan **gerbang** yang menegakkannya (lihat skill buku-ajar, references/harness-dan-gerbang.md bagian 4).

## Aturan bawaan dari skill buku-ajar (berlaku sampai penulis memutuskan lain)

Rincian: skill buku-ajar `references/aturan-gaya-dan-tampilan.md` dan `references/istilah-statistika.md`.

- Judul tabel dan gambar singkat (≤ 12 kata, satu frasa); penjelasan di Div `.catatan`; panel (a), (b) — G-JUDUL.
- Judul bab dan subjudul bukan kalimat tanya; pertanyaan di kalimat pertama prosa — G-JUDUL.
- Sitasi penulis–tahun tanpa lokasi; subjek pernyataan bersitasi hanya penulis orang — G-SITASI, G-ATRIBUSI.
- Tanpa koma sebelum penghubung subordinatif bila induk mendahului anak kalimat — G-KONJUNGSI.
- "persamaan" huruf kecil di tengah kalimat — G-PERSAMAAN.
- Pemisah parameter titik koma bila ada desimal: Beta(18,85; 281,15).
- Gambar dan tabel tidak mengambang (`fig-pos`/`tbl-pos: "H"`).
- Tanpa luapan tepi; nama tidak dipenggal — G-TEPI, G-PENGGALAN.
- Angka hasil dari kode inline — G-ANGKA.
- Data: riil → sintetis paket → simulasi sendiri; status selalu disebut; batasan data di prakata.
- Istilah: *likelihood*, estimasi, membangkitkan vs penarikan sampel, *draws* + jembatan, *noise* — G-ISTILAH (`konfig.json`).
- Nama teknik pengajaran tidak ditulis di naskah — G-LARANGAN.
- Tanpa subjudul buku; "Draf revisi ke-N" lewat `date-format`; tanda air DRAF; `REVISI.md` — G-HALJUDUL.
- Paragraf menjorok tanpa spasi antarparagraf (PDF dan Word).
- Anggaran halaman adalah anggaran, bukan batas keras; kejelasan didahulukan.
- Kunci jawaban terbit terpisah untuk pengajar: pembahasan langkah demi langkah + rubrik 10 poin; temuan soal diterapkan ke buku induk oleh agen terpisah.

## YYYY-MM-DD — <judul keputusan>

Permintaan/keputusan penulis: <…>.
Cakupan: <semua buku | buku …>; berlaku surut: <ya/tidak>.
Penegakan: <gerbang G-… / konfig istilah_terlarang / butir daftar periksa agen …>; fikstur `harness/uji-buku/bab….qmd`.
Penerapan: <putaran sunting, instruksi `naskah-bersama/instruksi-…-YYYY-MM-DD.md`, revisi ke-N>.
