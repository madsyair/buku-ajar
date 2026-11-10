# Loop kerja

*Looping engineering*: setiap artefak melewati loop tertutup dengan kriteria berhenti yang terukur, batas iterasi, eskalasi, dan jejak tertulis. Loop A (dengan varian multidisiplin) sampai E dijalankan orkestrator (`agents/00-orkestrator.md`).

## Prinsip

1. **Tidak ada yang meninjau tulisannya sendiri, dan tidak ada yang memperbaiki dari laporannya sendiri.** Pada buku multidisiplin, penulis ahli bidang tidak menjadi reviewer ahli atas bagiannya dan pemadu tidak meninjau bab paduannya. Peninjau adalah agen baru berkonteks bersih yang hanya membaca berkas (naskah, knit.md, PDF, registri), bukan penalaran penulis. Bila alat subagen tidak tersedia, ulasan dikerjakan berurutan dengan membaca ulang dari berkas, dan berkas ulasan mencatat "tanpa isolasi konteks" (contoh nyata: `bab01-pembaca-uji.md` seri). Ulasan seperti itu **tidak menggantikan** uji pembaca pemula independen (langkah 2a): di seri asal, audit tanpa isolasi oleh agen penulis-perbaikan melewatkan 35 MAYOR di 34 bab yang kemudian ditemukan pembaca berkonteks bersih.
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
   Paket minimum bila sumber daya terbatas: reviewer isi+rumus (satu agen), reviewer kode, satu pembaca pemula independen; seri statistika memakai pasangan "verifikasi independen" + "pembaca independen".
2a. **Uji pembaca pemula independen (wajib, setiap bab)**: subagen pembaca 10 baru berkonteks bersih, tidak membaca ulasan lain; satu agen boleh membaca 3–5 bab berurutan, tetapi menulis satu laporan per bab (`naskah/ulasan/babXX-pembaca-pemula-independen.md`). Instruksi: `assets/templat-instruksi-pembaca-independen.md`. Bila subagen tidak tersedia, bab belum boleh dinyatakan selesai; catat sebagai butir terbuka di `STATUS.md`.
3. **Editor memutuskan** atas temuan yang bertentangan (pemula minta penjelasan tambahan vs mahir minta ringkas) dan menyusun daftar kerja berurutan prioritas: MAYOR ketepatan → MAYOR keterbacaan → MINOR.
4. **Perbaikan** oleh penulis bab atau penyunting (bukan peninjau, bukan agen yang menulis laporan), dengan instruksi tertulis (`assets/templat-instruksi-perbaikan-pembaca.md`). Setiap temuan isi diperiksa dulu seperti reviewer isi (hitung ulang, registri); temuan yang keliru ditulis "tidak diterapkan" beserta bukti. Lalu harness sampai LULUS, lalu bagian Tindak lanjut di setiap berkas ulasan. MINOR yang butuh contoh baru atau keputusan penulis ditunda dan masuk "Usulan untuk diputuskan penulis" (bagian di bawah).
5. **Telaah pakar buku ajar** (`agents/21-penelaah-pakar-buku-ajar.md`, T2): setelah perbaikan putaran ulasan, penelaah menilai kelayakan bab sebagai bab buku ajar (materi, penyajian, kebahasaan, desain) dan memberi rekomendasi; temuannya masuk daftar kerja editor seperti temuan lain. Telaah rancangan (T1) dijalankan sebelum bab pertama ditulis, dan telaah buku utuh (T3) setelah render semua bab.
6. **Render** oleh orkestrator (berurutan), pemeriksaan G-RENDER/G-TEPI/G-PENGGALAN dan tampilan PDF; luapan dan tampilan diperbaiki, harness `--render` diulang.

**Kriteria berhenti** (semua harus terpenuhi):

- harness LULUS dengan `--render` (semua gerbang aktif, termasuk G-LOG);
- laporan pembaca pemula independen bab itu ada dan setiap temuannya bertindak lanjut;
- rekomendasi penelaah pakar buku ajar (21) untuk bab minimal "layak dengan perbaikan kecil";
- tidak ada temuan MAYOR terbuka di berkas ulasan mana pun (setiap MAYOR punya tindak lanjut "diperbaiki" atau keputusan penulis);
- setiap MINOR punya tindak lanjut (diperbaiki atau alasan tidak diterapkan);
- panjang bab dalam anggaran atau kelebihannya dijelaskan (kejelasan didahulukan; pemangkasan hanya untuk kalimat mubazir);
- bab ditambahkan ke `chapters` di `_quarto.yml` dan ke tabel `lampiran-kode/README.md`; titik simpan git dibuat.

**Batas iterasi**: maks. **3 putaran ulasan** per bab (putaran ke-2 dan ke-3 hanya meninjau ulang temuan sebelumnya dan bagian yang berubah). Loop internal harness maks. **6 percobaan** per kegagalan gerbang yang sama sebelum dilaporkan.

**Eskalasi ke penulis buku** bila: anggaran putaran habis dengan MAYOR terbuka; perbaikan membuka MAYOR baru dua putaran berturut-turut; temuan menyentuh keputusan rancangan (cakupan, data, istilah, notasi lintas buku); peninjau berbeda pendapat tentang kebenaran isi dan editor tidak dapat memutuskan dari sumber; perubahan memerlukan data/sumber yang harus diunggah penulis. Eskalasi berupa daftar singkat: butir, pilihan, rekomendasi, akibat tiap pilihan.

## Loop A multidisiplin — bab yang ditulis beberapa ahli bidang

Dipakai bila brief menyatakan buku multidisiplin. Penulis ahli bidang (`agents/04a-penulis-ahli-bidang.md`) dan penulis pemadu (`agents/04b-penulis-pemadu.md`) menggantikan penulis 04; aturan lain loop A tetap berlaku.

```
kerangka + penugasan ─▶ 04a tulis per disiplin (paralel, satu berkas bagian per agen) ─▶ harness bagian LULUS + serah-terima
   ─▶ [semua bagian LULUS] ─▶ arsipkan bagian ─▶ 04b pemaduan ─▶ harness bab LULUS
   ─▶ [ulasan ahli paralel: ahli disiplin per bagian + 05 isi + 07 bahasa + 20 pedagogi + pembaca 10–12] ─▶ 09 editor memutuskan
   ─▶ perbaikan: substansi → ahli bidang (bergiliran) | pemaduan/alur/bahasa → pemadu ─▶ pemadu menyelaraskan ─▶ harness bab ─▶ render
```

1. **Tulis per bidang**: setiap penulis ahli menulis `<buku>/babXX-<kode>.qmd` (hanya subbab yang ditugaskan; dimulai dari `##`, setup sendiri) dan catatan serah-terima `naskah/bagian/babXX-<kode>-serah.md` (`assets/templat-serah-terima-bagian.md`).
2. **Harness bagian**: `python3 harness/harness.py --buku <buku> --bab babXX-<kode>` (tanpa render) sampai LULUS. Klaim tercatat dengan kunci `<buku>/babXX-<kode>`. Label bagian bersufiks disiplin sehingga gerbang G-RUJUKAN sekaligus menjamin label unik antarbagian.
3. **Pemaduan** dimulai hanya setelah semua bagian LULUS dan semua serah-terima lengkap. Orkestrator memindahkan berkas bagian ke `<buku>/naskah/bagian/` (arsip, hanya dibaca; tidak lagi terbaca G-RUJUKAN sebagai bab) dan menghapus skrip lampiran bagian. Pemadu menulis `babXX.qmd` dan laporan `naskah/bagian/babXX-pemaduan.md` (`assets/templat-pemaduan.md`), memindahkan klaim ke kunci `<buku>/babXX`, lalu menjalankan harness bab sampai LULUS.
4. **Ulasan ahli paralel** setelah pemaduan, sesuai peta pemaduan. Aturan penugasan:
   - setiap bagian ditinjau minimal oleh **reviewer ahli disiplin bagian itu + reviewer bahasa (07) + editor (09)**; jembatan pemadu ditinjau reviewer ahli kedua disiplin yang dijembatani;
   - reviewer **tidak meninjau bagian yang ia tulis**: reviewer ahli adalah subagen baru yang bukan agen penulis bagian itu, dan pemadu tidak meninjau bab paduannya;
   - reviewer isi (05) memeriksa klaim dan angka seluruh bab; reviewer pedagogi (20) wajib; pembaca 10–12 seperti loop A.
   Pemetaan bawaan disiplin → reviewer ahli: statistika matematis → 06; pemodelan statistik → 16; komputasi/pemrograman → 08; *machine learning* → 17; statistika resmi/survei → 18; ekonomi, kesehatan, spasial, domain lain → 19 (diisi bidangnya); pedagogi → 20; bahasa → 07.
5. **Editor memutuskan** dan memberi setiap temuan sasaran perbaikan: **ahli `<kode>`** untuk substansi bidang (definisi, rumus, asumsi, metode, tafsiran), **pemadu** untuk jembatan, notasi lintas bagian, alur, prasyarat, dan bahasa.
6. **Perbaikan**: ahli bidang menyunting `babXX.qmd` hanya di subbab miliknya menurut peta pemaduan, **bergiliran** (satu agen per waktu), dan setiap giliran diakhiri harness bab LULUS; setelah semua giliran ahli, pemadu memperbaiki temuan pemaduan dan menyelaraskan sambungan yang tersentuh. Pemadu tidak mengubah substansi; bila perlu, ia menulis butir "dikembalikan ke ahli" di laporan pemaduan.
7. **Render** seperti loop A.

**Penyimpanan bagian dan jejak**:

| Berkas | Isi | Pemilik |
| --- | --- | --- |
| `<buku>/babXX-<kode>.qmd` | bagian selama ditulis (akar folder buku agar harness, `_bersama/`, `fit/`, `data-gambar/` dipakai tanpa perubahan) | satu penulis ahli |
| `<buku>/naskah/bagian/babXX-<kode>-serah.md` | catatan serah-terima | penulis ahli |
| `<buku>/naskah/bagian/babXX-<kode>.qmd` | arsip bagian setelah LULUS (dipindahkan orkestrator sebelum pemaduan) | hanya dibaca |
| `<buku>/naskah/bagian/babXX-pemaduan.md` | peta pemaduan, keputusan notasi, butir dikembalikan ke ahli | pemadu |
| `<buku>/babXX.qmd` | bab paduan | pemadu; ahli bergiliran saat perbaikan |

Bagian tidak disimpan sebagai Div ber-atribut di satu berkas bab karena beberapa ahli yang menulis serentak akan menyunting berkas yang sama (melanggar "satu agen per berkas"). Asal setiap subbab paduan dicatat di peta pemaduan, bukan di naskah.

**Kriteria berhenti**: semua kriteria loop A; ditambah setiap bagian sudah ditinjau reviewer ahli disiplinnya, 07, dan 09 tanpa ada yang meninjau tulisannya sendiri; tidak ada butir "dikembalikan ke ahli" yang terbuka; klaim bagian sudah pindah ke kunci bab dan tidak ada sisa entri `babXX-<kode>` di registri.

**Batas iterasi**: harness bagian maks. 6 percobaan per gerbang yang sama; maks. 3 putaran ulasan per bab (sama dengan loop A); maks. 2 putaran bolak-balik pemadu ↔ ahli untuk satu butir sebelum diserahkan ke editor.

**Eskalasi**: dua reviewer ahli (atau ahli dan pemadu) berbeda pendapat tentang substansi → **editor memutuskan** dari sumber primer dan bukti hitung ulang, dan mencatat alasannya di `babXX-editor.md`; bila perbedaan menyangkut **rancangan** (cakupan, pembagian bagian antardisiplin, notasi atau istilah lintas buku, disiplin yang ditugaskan, data) → **penulis buku** memutuskan. Ditambah semua pemicu eskalasi loop A.

## Usulan untuk diputuskan penulis

Telaah pakar (T1, T2, T3), tindak lanjut ulasan, dan MINOR yang ditunda sering menghasilkan butir yang hanya boleh diputuskan penulis buku (cakupan, urutan dan judul bab, data, notasi atau istilah lintas buku, sasaran tebal, suara penulis di prakata). Agar penulis tidak menjawab puluhan pertanyaan lepas:

```
laporan 21 / ulasan ─▶ penyunting: tindak lanjut (diperbaiki | tidak diterapkan + bukti | ditunda)
   ─▶ editor: bagian "Usulan untuk diputuskan penulis (<sumber>, <tanggal>)" + nilai bawaan sementara
   ─▶ orkestrator: daftar bernomor + rekomendasi ─▶ penulis: "setuju semua" / per nomor
   ─▶ KEPUTUSAN-RANCANGAN.md + "Diputuskan penulis <tanggal>" ─▶ putaran sunting (loop D)
```

Format setiap butir: nomor; sumber (mis. "R-m6, telaah rancangan"; "Buku 2 Bab 1, MINOR 8"); pertanyaan dalam satu kalimat; pilihan; **rekomendasi** dengan alasan singkat; akibat bagi bab, kunci, dan buku lain; **nilai bawaan sementara** yang dipakai penulis bab sampai ada jawaban (ditandai "diputuskan sementara, menunggu penulis"). Usulan satu buku ditaruh di `01-rancangan-rinci.md`; usulan lintas buku di `naskah-bersama/usulan-penulis-<tanggal>.md`. Pesan ke penulis menutup daftar dengan "Jawab 'setuju semua', atau sebut nomor yang diubah." Jawaban dicatat bertanggal; butir yang ditolak atau diubah (contoh seri: "setuju kecuali butir 8") dicatat beserta pilihan penulis.

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

## Loop F — gaya bab (sesudah loop A dan telaah 21)

Penyunting gaya buku ajar (22, konteks bersih) menelaah bab dari lima sisi (komunikatif–interaktif, semi-formal, istilah, rujukan, struktur bab) dan menulis ulang ke `naskah/gaya/babXX.qmd` beserta tabel keputusan sitasi (`references/gaya-buku-ajar.md`). Penerap revisi gaya (23, **agen lain**) membandingkan kedua versi paragraf demi paragraf, mengembalikan perubahan yang menggeser makna atau menghapus sitasi wajib, memperbarui registri (`"tampil": "bacaan-lanjut"`) dan glosarium, menerapkan ke `babXX.qmd`, lalu menjalankan `harness.py` dan `harness.py --tahap akhir` sampai keduanya LULUS. Batas 2 putaran; eskalasi bila penulisan ulang menggeser makna dua kali atau sapaan buku belum diputuskan.

## Loop G — penerbitan (buku utuh)

Editor penerbitan (24) membaca PDF/Word utuh dan memutuskan *siap terbit*, *siap terbit dengan perbaikan mekanis*, atau *perlu putaran revisi*. Perbaikan mekanis dikerjakan 23; temuan substansi dikembalikan ke loop A bab terkait; keputusan produksi (ISBN, penerbit, tanda air) ke penulis. Render ulang, lalu 24 memeriksa ulang. Batas 2 putaran.

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
## Tindak lanjut (tanggal)      ← diisi penulis bab (multidisiplin: ahli atau pemadu yang memperbaiki)
- M1 — diperbaiki (ahli `ml`): …
- MINOR 7 — tidak diterapkan: …
Harness --render LULUS; bab di PDF hlm. …–… (… halaman).
```

## Catatan status di orkestrasi

Orkestrator mencatat setiap putaran di `naskah/STATUS.md` buku (atau berkas status proyek): bab, putaran, agen, gerbang, hasil, temuan terbuka, langkah berikut, komit terakhir. Berkas ini yang dibaca pertama kali setelah kontainer dimulai ulang atau batas pemakaian. Agen yang terhenti dilanjutkan lewat pesan ke agen yang sama dengan menyebut langkah terakhirnya; proses latar dianggap mati (`agents/00-orkestrator.md`, bagian Pemulihan).
