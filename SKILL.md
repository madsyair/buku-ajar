---
name: buku-ajar
description: Alur multi-agen untuk menulis, menyunting, mengulas, dan menerbitkan buku ajar berbahasa Indonesia (EYD V) bidang statistika, sains data, dan komputasi dengan Quarto, R/Python, Stan/brms; termasuk seri buku, buku kunci jawaban untuk pengajar (rubrik 10 poin), audit ilustrasi, dan revisi setelah keputusan penulis. Menegakkan gerbang mutu yang dapat dieksekusi (angka dari kode, klaim berkutipan verbatim, judul singkat, sitasi penulis–tahun, koma konjungsi, tanpa luapan tepi) dan loop tulis → harness → ulasan paralel (isi, rumus, bahasa, kode, editor, pembaca pemula/menengah/mahir) → perbaikan → render. Gunakan setiap kali pengguna ingin membuat, melanjutkan, merevisi, atau mengaudit buku ajar, diktat, modul, bab buku, seri buku, atau kunci jawaban berbasis data dan kode, atau menyebut "bab berikutnya", "kerangka bab", "ulasan pembaca", "kunci jawaban", "draf revisi", meskipun tidak menyebut skill ini.
---

# Buku ajar (multi-agen, harness, loop)

Skill ini menyarikan proses nyata penulisan seri buku statistika Bayesian (Choir, STIS, 2026: tiga buku induk, tiga buku kunci, ±1.200 klaim terverifikasi) menjadi alur yang dapat diulang. Tiga janji: **benar** (setiap angka dihitung kode, setiap klaim berkutipan verbatim dari sumber yang dibuka), **dipahami** (alur digerakkan pertanyaan pembaca dan diuji dengan penjelasan ulang oleh pembaca berlapis), dan **rapi dicetak** (gerbang tampilan sampai PDF dan Word).

## Kapan dipakai

- Buku/diktat/modul baru, satu bab baru, atau seri beberapa buku dengan pembagian topik.
- Putaran sunting setelah keputusan gaya penulis (judul, istilah, koma, atribusi) yang harus diterapkan ke semua buku.
- Audit buku jadi; buku kunci jawaban untuk pengajar; audit dan pembuatan ilustrasi; kemasan kode sumber.
- Permintaan kecil (satu paragraf, satu gambar): cukup terapkan `references/aturan-gaya-dan-tampilan.md`, jalankan kode, dan harness bab itu; tidak perlu agen penuh.

## Prinsip gaya yang tertanam

Label internal skill: gaya **bertanya** ("Sokratik") dan gaya **menjelaskan-ulang** ("Feynman"). **Kedua nama itu (dan "Socrates", "teknik Feynman") tidak pernah muncul di naskah buku**; gerbang G-LARANGAN menolaknya. Brief buku menulis gayanya dengan deskripsi, bukan nama.

1. Alur prosa digerakkan **pertanyaan wajar pembaca** di kalimat pertama subbab; subjudul **bukan** kalimat tanya.
2. Setiap subbab harus dapat **dijelaskan ulang** pembaca sasaran dalam beberapa kalimat sederhana; penulis menulis penjelasan tanpa notasi sebelum rumus; pembaca uji mengujinya.
3. **Intuisi → rumus → interpretasi angka** dari kode buku sendiri, dengan satuan dan ketidakpastian.
4. Contoh dari **pengetahuan umum dan konteks Indonesia**; analogi dipetakan dan diberi batas.
5. Istilah asing tanpa padanan lazim **dicetak miring dan dijelaskan** pada kemunculan pertama di setiap bab; satu istilah baru per kalimat; **jembatan istilah** antarbab/antarbuku.
6. Data **riil → sintetis paket → simulasi sendiri**; status data selalu disebut; batasan data di prakata.
7. 5W1H dipakai sebagai **daftar periksa perencanaan** (versi statistika: apa, mengapa, kapan dipakai, bagaimana menghitung, bagaimana menafsirkan, kapan gagal), bukan subjudul.

Rinci: `references/prinsip-buku-ajar.md` (ringkasan operasional kajian; daftar periksa butir 1–35), `references/aturan-gaya-dan-tampilan.md`, `references/istilah-statistika.md`.

## Peran

Setiap peran punya berkas di `agents/` (masukan, keluaran, langkah, daftar periksa, kriteria lulus, larangan). Baca berkas peran sebelum menjalankannya; beri subagen jalur berkas, bukan ringkasan dari ingatan.

| No. | Peran | Berkas | Keluaran utama | Menyunting naskah? |
|---|---|---|---|---|
| 00 | Orkestrator | `agents/00-orkestrator.md` | `naskah/STATUS.md`, instruksi, render, komit | tidak |
| 01 | Perencana naskah | `agents/01-perencana-naskah.md` | `00-brief.md`, `KEPUTUSAN-RANCANGAN.md`, peta antarbuku | — |
| 02 | Perancang kerangka | `agents/02-perancang-kerangka.md` | `01-rancangan-rinci.md`, `03-kerangka/babXX.md` | — |
| 03 | Peninjau literatur | `agents/03-peninjau-literatur.md` | `pustaka.bib`, `referensi.json`, klaim, daftar unggahan | — |
| 04 | Penulis (dan penyunting) | `agents/04-penulis.md` | `babXX.qmd`, klaim, tindak lanjut ulasan | **ya** |
| 05 | Reviewer isi | `agents/05-reviewer-isi.md` | `ulasan/babXX-isi.md` | tidak |
| 06 | Reviewer rumus | `agents/06-reviewer-rumus.md` | `ulasan/babXX-rumus.md` | tidak |
| 07 | Reviewer bahasa | `agents/07-reviewer-bahasa.md` | `ulasan/babXX-bahasa.md` (mode sunting: bahasa saja) | hanya mode sunting |
| 08 | Reviewer kode | `agents/08-reviewer-kode.md` | `ulasan/babXX-kode.md` | tidak |
| 09 | Editor | `agents/09-editor.md` | `ulasan/babXX-editor.md`: keputusan atas temuan, daftar kerja | tidak |
| 10–12 | Pembaca pemula, menengah, mahir | `agents/10-…`, `11-…`, `12-…` | `ulasan/babXX-pembaca-*.md` (MAYOR/MINOR) | tidak |
| 13 | Pembuat kunci jawaban | `agents/13-pembuat-kunci-jawaban.md` | `kunci-<buku>/kunci-babXX.qmd`, `temuan-soal.md` | bab kunci saja |
| 14 | Penyunting soal | `agents/14-penyunting-soal.md` | soal induk diperbaiki, status "Diterapkan" | soal induk saja |
| 15 | Pengaudit ilustrasi | `agents/15-pengaudit-ilustrasi.md` | `audit-ilustrasi.md`, gambar baru | rujukan gambar saja |

Peninjau (05–12, pemeriksa kunci) adalah **subagen baru berkonteks bersih** yang hanya membaca berkas. Bila alat subagen tidak tersedia, jalankan peran berurutan dengan membaca ulang dari berkas dan tulis "tanpa isolasi konteks" di berkas ulasan. Penulis tidak pernah meninjau tulisannya sendiri.

## Alur tahap demi tahap

```
Proyek   : siapkan_proyek.py → uji_harness.sh hijau
Buku     : 01 brief ─▶ 03 sumber+registri ─▶ 02 rancangan rinci ─▶ [persetujuan penulis]
Bab (A)  : 02 kerangka ─▶ 04 tulis ─▶ harness LULUS ─▶ 05–12 paralel ─▶ 09 putuskan ─▶ 04 perbaiki
           ─▶ harness LULUS ─▶ 00 render berurutan + G-RENDER/G-TEPI/G-PENGGALAN ─▶ komit
Kunci (C): 13 kunci ─▶ temuan-soal ─▶ 14 terapkan ke induk ─▶ 13 sesuaikan ─▶ pemeriksa independen
Keputusan baru (D): catat ─▶ gerbang/konfig + fikstur ─▶ audit semua buku ─▶ sunting paralel ─▶ render ─▶ REVISI.md
Ilustrasi (E): 15 audit ─▶ gambar ─▶ harness ─▶ render ─▶ pembaca/editor
Akhir    : render semua buku berurutan ─▶ anatomi/tipografi (butir 33–35) ─▶ kemas_sumber.py
```

| Tahap | Gerbang keluar |
|---|---|
| Brief | butir wajib templat terisi; pembaca dan tiga profil uji; peta "satu topik, satu pemilik"; G-HALJUDUL pada `_quarto.yml` |
| Sumber | setiap kunci yang akan disitasi terverifikasi di `referensi.json`; kutipan klaim ada verbatim |
| Rancangan/kerangka | setiap subbab punya pertanyaan, penjelasan sederhana, sumber; enam pertanyaan perencanaan per metode; data per bab terperiksa (status Rd); latihan dapat dijawab pasti; persetujuan penulis untuk bab pertama |
| Draf bab | `harness.py` LULUS tanpa render (semua gerbang aktif) |
| Ulasan | tidak ada MAYOR terbuka; setiap temuan punya tindak lanjut tertulis |
| Render | `harness.py --render` LULUS: G-RENDER, G-TEPI, G-PENGGALAN; tampilan PDF/Word diperiksa editor |
| Kunci | setiap latihan: pembahasan, Jawaban akhir, rubrik = 10; temuan soal Diterapkan/Diputuskan |

## Harness engineering

Aturan yang dapat diperiksa mesin **wajib** menjadi gerbang yang dapat dieksekusi, bukan sekadar instruksi. Harness (`scripts/harness.py`, disalin ke `<proyek>/harness/`) menjalankan 25 gerbang per bab: kode berjalan dan lampiran mandiri (G-KODE, G-LAMPIRAN), angka inline (G-ANGKA), keluaran/lebar (G-KELUARAN, G-LEBAR-KODE, G-LEBAR-KELUARAN, G-BOCOR, G-PYTHON), rujukan dan sitasi (G-RUJUKAN, G-SITASI, G-ATRIBUSI, **G-REFERENSI** dengan registri klaim berkutipan verbatim), tampilan (G-JUDUL, G-PERSAMAAN, G-HALJUDUL), bahasa (G-EYD lewat skill eyd, G-KONJUNGSI, G-GAYA, G-PARAGRAF, G-SLOP, G-ISTILAH, G-LARANGAN), dan render (G-RENDER, G-TEPI, G-PENGGALAN).

```bash
python3 harness/harness.py --buku <buku> --bab babXX            # agen bab
python3 harness/harness.py --buku <buku> --bab babXX --render   # orkestrator, berurutan
bash harness/uji_harness.sh                                     # setiap kali harness/konfig berubah
```

- **Setiap keputusan gaya penulis yang dapat diperiksa mesin menjadi gerbang baru** (pola kata → `konfig.json`; struktur → fungsi `gerbang_x`), disertai **fikstur gagal** di `harness/uji-buku/` dan uji regresi hijau, lalu diaudit ke semua buku. Prosedur enam langkah: `references/harness-dan-gerbang.md` bagian 4.
- Pengecualian hanya di `pengecualian.json` dan wajib beralasan; tidak ada penghapusan massal.
- Lulus harness adalah syarat perlu, bukan bukti mutu: kebenaran isi, narasi gambar, ambang tipis, dan kepaduan diperiksa peninjau.

Rinci: `references/harness-dan-gerbang.md`, `scripts/README.md`.

## Looping engineering

Loop tertutup dengan kriteria berhenti, batas iterasi, eskalasi, dan jejak tertulis (`references/loop-kerja.md`):

| Loop | Isi | Berhenti bila | Batas | Eskalasi ke penulis |
|---|---|---|---|---|
| A bab | tulis → harness → ulasan independen paralel → editor → perbaikan → harness → render | `--render` LULUS, 0 MAYOR terbuka, semua temuan bertindak lanjut | 3 putaran ulasan; 6 percobaan per gerbang | MAYOR bertahan; perbaikan membuka MAYOR baru 2×; temuan menyentuh rancangan |
| B literatur | usul klaim → registri → G-REFERENSI → cek parafrase | semua sitasi terbukti | 3 putaran | sumber harus diunggah |
| C kunci → soal induk | temuan soal → penyunting soal → harness induk → kunci disesuaikan → pemeriksa | semua temuan Diterapkan/Diputuskan | 2 putaran | rumusan mengubah tujuan latihan |
| D keputusan → gerbang → audit | keputusan → gerbang + fikstur → audit semua buku → sunting → render → `REVISI.md` | semua buku LULUS gerbang baru | per kelompok bab | pola gerbang ambigu |
| E ilustrasi | audit → gambar → harness → render → periksa narasi | narasi cocok, harness LULUS | 2 putaran | — |

Tindak lanjut ditulis penulis di bagian `## Tindak lanjut (tanggal)` setiap berkas ulasan; status putaran di `naskah/STATUS.md`.

## Paralelisasi aman

- **Satu agen per berkas**; kelompok bab tanpa irisan; pembuat kunci dan penyunting soal tidak pernah menyunting berkas yang sama.
- Berkas bersama (`harness/klaim.json`, `pengecualian.json`) hanya lewat `flock <scratchpad>/klaim.lock`, mengganti entri bab sendiri.
- Agen bab **tidak** menjalankan `--render` dan tidak mengubah `_quarto.yml`, `harness/`, `_bersama/`, bab/buku lain.
- **Render berurutan** oleh orkestrator, satu buku sekali jalan, PDF + Word dalam satu `quarto render`.
- Cache model dan parquet bernama unik per bab; peninjau menghitung ulang di subfolder scratchpad sendiri.
- **Pemulihan setelah kontainer dimulai ulang**: baca `STATUS.md`, `git status/log`, laporan harness; anggap proses latar mati; bersihkan kunci basi; jalankan ulang harness bab "sedang dikerjakan"; lanjutkan dari langkah tercatat.
- **Titik simpan git** setelah setiap bab lulus, setiap putaran sunting, setiap perubahan harness (dengan fikstur), dan setiap render; jangan komit `fit/`, `_book/`, `build/`, `harness/sumber/`.

Rinci: `agents/00-orkestrator.md`.

## Kriteria selesai

- **Bab**: kriteria berhenti loop A terpenuhi; bab ada di `chapters` dan `lampiran-kode/README.md`; halaman sebenarnya tercatat; komit.
- **Buku**: semua bab selesai; prakata (tujuan, pembaca, cara pakai, "Data yang digunakan dan batasannya"); lampiran Sumber Data; daftar pustaka; anatomi dan tipografi (butir 33–35); tanpa subjudul buku; "Draf revisi ke-N" dan `REVISI.md` mutakhir; render bersih PDF dan Word.
- **Kunci**: setiap latihan induk berpembahasan dan berubrik 10; pemeriksa independen tanpa MAYOR; temuan soal tertutup.
- Laporan ke penulis menyebut yang belum terverifikasi; jangan menyatakan selesai sebelum gerbang lulus.

## Skill pendukung

- **eyd** (wajib untuk naskah Indonesia): `scripts/periksa.py` dipanggil G-EYD; reviewer bahasa memakai `references/kalimat-efektif.md`, `kata-hubung.md`, `inventaris-kesalahan.md`, `istilah-dan-kbbi.md`, `pemenggalan-kata.md`. Bila tidak terpasang, G-EYD gagal terbaca: set `SKILL_EYD` atau laporkan bahwa pemeriksaan EYD otomatis tidak berjalan.
- **humanizer-id**: reviewer bahasa memakainya untuk membuang pola tulisan mesin tanpa mengarang fakta (G-SLOP hanya menangkap frasa).
- **buku-praktikum**: untuk modul praktikum kecil atau bila diperlukan `scripts/cek_turunan.py` (pemeriksa penurunan SymPy) bagi reviewer rumus. Untuk seri buku dengan keputusan penulis yang terus bertambah, pakai skill ini.
- **dataviz**: dibaca sebelum kode gambar pertama proyek (palet, kontras, bentuk grafik); konvensi gambar buku tetap di `references/ilustrasi.md`.
- **docx / pdf**: memeriksa atau memperbaiki keluaran Word (gaya *Body Text*/*First Paragraph*, pemenggalan, bahasa id-ID) dan PDF (ekstraksi teks, halaman bab) setelah render.
- Skill riset (mis. deep-research) boleh dipakai peninjau literatur untuk menemukan sumber, tetapi hasilnya tetap masuk registri dengan kutipan dari teks yang dibuka.

## Berkas rujukan

| Berkas | Isi | Dibaca oleh |
|---|---|---|
| `references/prinsip-buku-ajar.md` | ringkasan operasional kajian; 5W1H; Permendikbudristek 22/2022; daftar periksa 35 butir | 02, 04, 05–12 |
| `references/kajian-prinsip-buku-ajar.md` | kajian lengkap (status sumber [A]/[S]/[A, terverifikasi]) | bila perlu dasar |
| `references/aturan-gaya-dan-tampilan.md` | semua keputusan gaya bawaan: prosa, judul, tabel/gambar, rumus, sitasi, angka/kode, struktur bab, cetak, halaman judul, bahasa | semua |
| `references/istilah-statistika.md` | kebijakan istilah, keputusan bawaan, jembatan istilah | 01, 04, 07, 09 |
| `references/data-dan-sumber.md` | urutan data, status data, peta, prakata; registri klaim dan identitas | 01–05, 13 |
| `references/harness-dan-gerbang.md` | setiap gerbang, konfig, menambah gerbang, registri aman, render | 00, 04, 08 |
| `references/loop-kerja.md` | loop A–E, kriteria berhenti, batas, eskalasi, format ulasan | 00, 09, peninjau |
| `references/kunci-jawaban.md` | bentuk kunci, rubrik, temuan soal, pemeriksaan kunci | 13, 14 |
| `references/ilustrasi.md` | jalur Python/TikZ, keterangan, audit | 04, 15 |
| `references/pelajaran-proyek.md` | kesalahan berulang dan pencegahannya | 04, 05, 08, 09 |

Templat di `assets/`: brief, rancangan rinci, kerangka bab, bab `.qmd` dan bab kunci `.qmd` (keduanya lulus harness), laporan ulasan, temuan soal, `KEPUTUSAN-RANCANGAN`, `REVISI`, `STATUS`, `_quarto.yml`, `preamble.tex`, `tikz-preamble.tex`, `konfig.json`, `apa.csl`, `reference-b5.docx`.

## Kemasan akhir

1. Render semua buku (induk lalu kunci) berurutan dengan `--render`; semua gerbang render lulus.
2. Editor memeriksa butir 33–35 per buku; hapus tanda air dan set `DRAF=0` hanya untuk versi terbit yang diputuskan penulis.
3. `python3 harness/kemas_sumber.py <folder>` → `<proyek>-<buku>-sumber.zip` per buku (induk + kunci + folder bersama + lampiran kode, tanpa sumber berhak cipta, cache, dan berkas antara) dengan `BANGUN.md`.
4. Komit akhir; laporan ke penulis: berkas PDF/Word, zip, status gerbang, keputusan terbuka.
