# Loop kerja

*Looping engineering*: setiap artefak melewati loop tertutup dengan kriteria berhenti yang terukur, batas iterasi, eskalasi, dan jejak tertulis. Empat loop dijalankan orkestrator (`agents/00-orkestrator.md`).

## Prinsip

1. **Tidak ada yang meninjau tulisannya sendiri.** Peninjau adalah agen baru berkonteks bersih yang hanya membaca berkas (naskah, knit.md, PDF, registri), bukan penalaran penulis. Bila alat subagen tidak tersedia, ulasan dikerjakan berurutan dengan membaca ulang dari berkas, dan berkas ulasan mencatat "tanpa isolasi konteks" (contoh nyata: `bab01-pembaca-uji.md` seri).
2. **Peninjau hanya membaca.** Peninjau tidak menyunting naskah, tidak menjalankan render, tidak menulis registri; hitung ulang dilakukan di scratchpad.
3. **Temuan tertulis dan berstatus.** Setiap temuan berlabel MAYOR/MINOR, menyebut baris, kutipan, masalah, usulan. Penulis menanggapi setiap butir di bagian `## Tindak lanjut (tanggal)` berkas ulasan: diperbaiki (bagaimana), tidak diterapkan (alasan), atau diajukan ke penulis buku.
4. **Harness sebelum dan sesudah ulasan.** Ulasan dimulai hanya dari bab yang LULUS harness; perbaikan ditutup dengan harness LULUS lagi.
5. **Kriteria berhenti terukur**, bukan "sudah cukup baik".

## Loop A — bab (inti)

```
kerangka ─▶ tulis ─▶ harness ─▶ [ulasan independen paralel] ─▶ editor memutuskan ─▶ perbaikan ─▶ harness ─▶ render (berurutan) ─▶ pemeriksaan render
              ▲         │ GAGAL                                                         │
              └─────────┘                                                               └─▶ putaran berikutnya bila masih ada MAYOR terbuka
```

1. **Tulis** (penulis): bab dari kerangka; loop internal tulis → harness → perbaiki sampai Status LULUS (tanpa render).
2. **Ulasan independen paralel** (beberapa agen sekaligus, masing-masing satu berkas laporan, tidak menyunting apa pun):
   - reviewer isi (`naskah/ulasan/babXX-isi.md`), reviewer rumus (`-rumus.md`), reviewer kode (`-kode.md`), reviewer bahasa (`-bahasa.md`);
   - pembaca pemula, menengah, mahir (`-pembaca-pemula.md`, `-menengah.md`, `-mahir.md`);
   - verifikasi independen angka dan klaim (bagian dari reviewer isi/kode: hitung ulang dari `fit/*.rds`, cek kutipan registri).
   Paket minimum bila sumber daya terbatas: reviewer isi+rumus (satu agen), reviewer kode, satu pembaca pemula; seri statistika memakai pasangan "verifikasi independen" + "pembaca independen".
3. **Editor memutuskan** atas temuan yang bertentangan (pemula minta penjelasan tambahan vs mahir minta ringkas) dan menyusun daftar kerja berurutan prioritas: MAYOR ketepatan → MAYOR keterbacaan → MINOR.
4. **Perbaikan** oleh penulis bab (bukan peninjau), lalu harness sampai LULUS, lalu bagian Tindak lanjut di setiap berkas ulasan.
5. **Render** oleh orkestrator (berurutan), pemeriksaan G-RENDER/G-TEPI/G-PENGGALAN dan tampilan PDF; luapan dan tampilan diperbaiki, harness `--render` diulang.

**Kriteria berhenti** (semua harus terpenuhi):

- harness LULUS dengan `--render` (semua gerbang aktif);
- tidak ada temuan MAYOR terbuka di berkas ulasan mana pun (setiap MAYOR punya tindak lanjut "diperbaiki" atau keputusan penulis);
- setiap MINOR punya tindak lanjut (diperbaiki atau alasan tidak diterapkan);
- panjang bab dalam anggaran atau kelebihannya dijelaskan (kejelasan didahulukan; pemangkasan hanya untuk kalimat mubazir);
- bab ditambahkan ke `chapters` di `_quarto.yml` dan ke tabel `lampiran-kode/README.md`; titik simpan git dibuat.

**Batas iterasi**: maks. **3 putaran ulasan** per bab (putaran ke-2 dan ke-3 hanya meninjau ulang temuan sebelumnya dan bagian yang berubah). Loop internal harness maks. **6 percobaan** per kegagalan gerbang yang sama sebelum dilaporkan.

**Eskalasi ke penulis buku** bila: anggaran putaran habis dengan MAYOR terbuka; perbaikan membuka MAYOR baru dua putaran berturut-turut; temuan menyentuh keputusan rancangan (cakupan, data, istilah, notasi lintas buku); peninjau berbeda pendapat tentang kebenaran isi dan editor tidak dapat memutuskan dari sumber; perubahan memerlukan data/sumber yang harus diunggah penulis. Eskalasi berupa daftar singkat: butir, pilihan, rekomendasi, akibat tiap pilihan.

## Loop B — literatur dan klaim

Peninjau literatur mengusulkan sumber dan klaim → registri (`klaim.json`, `referensi.json`) → G-REFERENSI → reviewer isi memeriksa parafrase setia pada kutipan → klaim yang tak terbukti dihapus atau diubah menjadi pernyataan hasil hitung buku. Batas: 3 putaran per bab; sumber yang tidak dapat dibuka masuk daftar "perlu diunggah penulis" (eskalasi), bukan dikarang.

## Loop C — lintas buku: kunci jawaban → soal induk

```
pembuat kunci menemukan soal bermasalah ─▶ catat di kunci-<buku>/naskah/temuan-soal.md (rumusan soal baru lengkap)
   ─▶ pembuat kunci menulis kunci untuk rumusan baru
   ─▶ penyunting soal (agen terpisah) menerapkan ke bab induk ─▶ harness bab induk LULUS ─▶ baris temuan "Diterapkan YYYY-MM-DD: …"
   ─▶ kunci disesuaikan dengan soal yang benar-benar diterapkan ─▶ harness bab kunci LULUS
   ─▶ pemeriksa independen kunci (hitung ulang mandiri) ─▶ temuan → perbaikan kunci / temuan soal baru
```

Berhenti bila setiap baris `temuan-soal.md` berstatus Diterapkan atau Diputuskan-penulis, bab induk dan kunci LULUS, dan pemeriksa kunci tidak punya MAYOR terbuka. Perubahan soal yang mengubah tujuan latihan dieskalasi. Dua agen tidak pernah menyunting berkas yang sama: penulis kunci hanya `kunci-babXX.qmd` dan `temuan-soal.md`; penyunting soal hanya bab induk dan kolom status temuan.

## Loop D — lintas buku: keputusan penulis baru → gerbang → audit

```
keputusan penulis ─▶ KEPUTUSAN-RANCANGAN.md (bertanggal) ─▶ gerbang baru/konfig + fikstur gagal (uji_harness.sh hijau)
   ─▶ audit: gerbang dijalankan pada semua bab semua buku (induk + kunci), tanpa render
   ─▶ instruksi penyuntingan tertulis (naskah-bersama/instruksi-<topik>-<tanggal>.md) ─▶ agen penyunting per kelompok bab (paralel)
   ─▶ harness per bab LULUS ─▶ render tiap buku berurutan ─▶ "Draf revisi ke-N" naik + REVISI.md ─▶ titik simpan git
```

Keputusan yang tidak dapat diperiksa mesin (mis. "setiap kalimat utuh", "kepaduan paragraf") masuk daftar periksa reviewer bahasa dan dijalankan sebagai audit baca per kelompok bab. Berhenti bila semua buku LULUS dengan gerbang baru dan render bersih. Keputusan yang dibuat agen saat perancangan ditandai "dapat diubah penulis" dan tidak disebut keputusan penulis.

## Loop E — ilustrasi

Pengaudit ilustrasi per kelompok bab: audit → `audit-ilustrasi.md` → buat ≤ 2 gambar per bab → harness LULUS → render berurutan → pembaca/editor memeriksa narasi cocok dengan gambar → perbaikan. Batas 2 putaran.

## Format berkas ulasan

Lihat `assets/templat-laporan-ulasan.md`. Inti:

```
# Ulasan <peran> — Bab N "<judul>" (tanggal)
Peninjau, profil, apa yang dibaca (qmd, knit.md, PDF hlm.), apa yang tidak dijalankan.
## Ringkasan (tabel pemeriksaan; jumlah MAYOR/MINOR)
## MAYOR
**M1. <judul temuan>** (baris …) Kutipan … Masalah … Usulan …
## MINOR
1. **Baris …** …
## Yang sudah baik
## Tindak lanjut (tanggal)      ← diisi penulis bab
- M1 — diperbaiki: …
- MINOR 7 — tidak diterapkan: …
Harness --render LULUS; bab di PDF hlm. …–… (… halaman).
```

## Catatan status di orkestrasi

Orkestrator mencatat setiap putaran di `naskah/STATUS.md` buku (atau berkas status proyek): bab, putaran, agen, gerbang, hasil, temuan terbuka, langkah berikut, komit terakhir. Berkas ini yang dibaca pertama kali setelah kontainer dimulai ulang.
