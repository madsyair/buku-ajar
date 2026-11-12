#!/usr/bin/env bash
# Uji regresi harness: fikstur buruk harus GAGAL, fikstur bersih harus LULUS.
# Jalankan setiap kali harness.py diubah atau gerbang baru ditambahkan.
# Setiap gerbang baru WAJIB disertai satu fikstur gagal di uji-buku/ dan
# namanya ditambahkan ke daftar GAGAL di bawah (lihat
# references/harness-dan-gerbang.md, "Menambah gerbang").
# Dijalankan dari akar proyek setelah skrip disalin ke harness/:
#   bash harness/uji_harness.sh
cd "$(dirname "$0")/.."
status=0
# Setiap fikstur gagal dipasangkan dengan gerbang yang HARUS gagal. Uji lulus hanya
# bila gerbang itu tercatat [GAGAL] dan harness tidak berhenti karena galat Python;
# kode keluar saja tidak cukup (dulu fikstur "gagal" ikut lulus ketika harness
# crash karena Rscript atau Sastrawi tidak terpasang).
# Format: fikstur:gerbang[:R]  (:R = gerbang butuh R + knitr)
GAGAL="babgagal:G-ANGKA babbahasa:G-EYD:R babbocor:G-BOCOR:R babsitasi:G-REFERENSI
babcap:G-BOCOR:R babgayasitasi:G-SITASI babinf:G-BOCOR:R babjudul:G-JUDUL
bablarangan:G-LARANGAN babln:G-LN babrumus:G-RUMUS babstruktur:G-STRUKTUR
babkonjungsi:G-KONJUNGSI"
ADA_R=0; command -v Rscript > /dev/null && Rscript -e 'library(knitr)' > /dev/null 2>&1 && ADA_R=1
for butir in $GAGAL; do
  bab=${butir%%:*}; sisa=${butir#*:}; gerbang=${sisa%%:*}
  if [ "$sisa" != "${sisa%:R}" ] && [ $ADA_R = 0 ]; then
    echo "dilewati: $bab ($gerbang butuh R + knitr)"; continue
  fi
  keluaran=$(python3 harness/harness.py --buku harness/uji-buku --bab "$bab" 2>&1)
  if ! echo "$keluaran" | grep -q "^Status:"; then
    echo "SALAH: $bab membuat harness crash"; echo "$keluaran" | tail -3; status=1
  elif echo "$keluaran" | grep -q "\[GAGAL\] $gerbang\b"; then
    echo "benar: $bab GAGAL di $gerbang"
  else
    echo "SALAH: $bab seharusnya GAGAL di $gerbang"; status=1
  fi
done
if [ $ADA_R = 1 ]; then
  if python3 harness/harness.py --buku harness/uji-buku --bab babbaik > /dev/null 2>&1; then
    echo "benar: babbaik LULUS"
  else
    echo "SALAH: babbaik seharusnya LULUS"; status=1
  fi
else
  echo "dilewati: babbaik LULUS (butuh R + knitr) — uji TIDAK LENGKAP"
fi
# G-GAYA-AJAR hanya aktif pada --tahap akhir (sesudah peran 22–23): babgayaajar
# (gaya artikel: tanpa sapaan, "pembaca" sebagai pelaku, kalimat panjang, sitasi padat) GAGAL.
keluaran=$(python3 harness/harness.py --buku harness/uji-buku --bab babgayaajar --tahap akhir 2>&1)
if echo "$keluaran" | grep -q "\[GAGAL\] G-GAYA-AJAR"; then echo "benar: babgayaajar GAGAL di G-GAYA-AJAR (--tahap akhir)"
else echo "SALAH: babgayaajar seharusnya GAGAL di G-GAYA-AJAR (--tahap akhir)"; status=1; fi
keluaran=$(python3 harness/harness.py --buku harness/uji-buku --bab babbaik --tahap akhir 2>&1)
if echo "$keluaran" | grep -q "\[GAGAL\] G-\(GAYA-AJAR\|STRUKTUR\|RUMUS\|SITASI-ULANG\)"; then
  echo "SALAH: babbaik seharusnya lolos G-GAYA-AJAR, G-STRUKTUR, G-RUMUS, G-SITASI-ULANG (--tahap akhir)"; status=1
else echo "benar: babbaik lolos G-GAYA-AJAR, G-STRUKTUR, G-RUMUS, G-SITASI-ULANG (--tahap akhir)"; fi
# G-KONJUNGSI: "seperti" di kalimat sebelumnya tidak boleh meloloskan ", karena" (baris 3);
# aposisi "seperti … 0,5,", "mis.", dan "Jadi, bila …" tetap sah (baris 5)
temuan=$(python3 -c "import sys, pathlib; sys.path.insert(0, 'harness'); import harness
harness.gerbang_konjungsi(pathlib.Path('harness/uji-buku/babkonjungsi.qmd'), harness.muat_pengecualian())" | grep -o "baris [0-9]*:" | tr '\n' ' ')
# ", jadi" di tengah kalimat (EYD V B.5) ditandai (baris 7)
if [ "$temuan" = "baris 3: baris 7: " ]; then echo "benar: konjungsi lintas kalimat dan ', jadi'"; else echo "SALAH: konjungsi seharusnya baris 3 dan 7 (dapat: $temuan)"; status=1; fi
# G-PERTANYAAN (WARNING, tidak menggagalkan): hanya subbab tanpa pertanyaan di paragraf
# prosa pertamanya yang ditandai (babpertanyaan, baris 5); babbaik tidak memicu peringatan.
temuan=$(python3 -c "import sys, pathlib; sys.path.insert(0, 'harness'); import harness
for p in harness.peringatan_pertanyaan(pathlib.Path('harness/uji-buku/babpertanyaan.qmd').read_text(encoding='utf-8')): print(p)" | grep -o "baris [0-9]*:" | tr '\n' ' ')
if [ "$temuan" = "baris 5: " ]; then echo "benar: G-PERTANYAAN hanya menandai subbab tanpa pertanyaan"; else echo "SALAH: G-PERTANYAAN seharusnya hanya baris 5 (dapat: $temuan)"; status=1; fi
temuan=$(python3 -c "import sys, pathlib; sys.path.insert(0, 'harness'); import harness
print(len(harness.peringatan_pertanyaan(pathlib.Path('harness/uji-buku/babbaik.qmd').read_text(encoding='utf-8'))))")
if [ "$temuan" = "0" ]; then echo "benar: babbaik tanpa peringatan G-PERTANYAAN"; else echo "SALAH: babbaik memicu $temuan peringatan G-PERTANYAAN"; status=1; fi
# WARNING tidak menggagalkan status: babpertanyaan tidak boleh gagal di G-PERTANYAAN
# (gerbang ini tidak tercatat di daftar gerbang) dan harness tidak crash.
keluaran=$(python3 harness/harness.py --buku harness/uji-buku --bab babpertanyaan 2>&1)
if echo "$keluaran" | grep -q "^Status:" && echo "$keluaran" | grep -q "\[PERINGATAN\] G-PERTANYAAN" && ! echo "$keluaran" | grep -q "\[GAGAL\] G-PERTANYAAN"; then
  echo "benar: babpertanyaan memberi PERINGATAN G-PERTANYAAN, bukan GAGAL"
else echo "SALAH: babpertanyaan seharusnya hanya PERINGATAN G-PERTANYAAN"; status=1; fi
# G-SITASI-ULANG (keputusan penulis 2026-11-12): satu sumber disitasi sekali per paragraf.
# babsitasiulang: @gelman2013 dua kali (baris 3), @gelman2021 dengan lokator berbeda (baris 5,
# saran gabung "hlm. 5, 9"), naratif + kurung lintas baris (baris 7), lokator di sitasi kedua
# (baris 8). Rujukan silang berulang, kode sebaris, komentar, blok kode, dua butir daftar, dan
# sumber yang sama di paragraf lain tidak ditandai.
temuan=$(python3 -c "import sys, pathlib; sys.path.insert(0, 'harness'); import harness
for p in harness.temuan_sitasi_ulang(pathlib.Path('harness/uji-buku/babsitasiulang.qmd').read_text(encoding='utf-8')): print(p)")
baris=$(echo "$temuan" | grep -o "^baris [0-9]*: @[a-z0-9]*" | tr '\n' ' ')
if [ "$baris" = "baris 3: @gelman2013 baris 5: @gelman2021 baris 7: @kolmogorov1950 baris 8: @berndt1991 " ] \
   && echo "$temuan" | grep -qF "[@gelman2021, hlm. 5, 9]"; then
  echo "benar: G-SITASI-ULANG menandai 4 sitasi berulang dan menyarankan gabung lokator"
else echo "SALAH: G-SITASI-ULANG seharusnya baris 3, 5, 7, 8 dengan saran [@gelman2021, hlm. 5, 9] (dapat: $baris)"; status=1; fi
# Tahap draf: PERINGATAN, bukan GAGAL; --tahap akhir: GAGAL
keluaran=$(python3 harness/harness.py --buku harness/uji-buku --bab babsitasiulang 2>&1)
if echo "$keluaran" | grep -q "^Status:" && echo "$keluaran" | grep -q "\[PERINGATAN\] G-SITASI-ULANG" \
   && ! echo "$keluaran" | grep -q "\[GAGAL\] G-SITASI-ULANG"; then
  echo "benar: babsitasiulang memberi PERINGATAN G-SITASI-ULANG pada tahap draf"
else echo "SALAH: babsitasiulang seharusnya hanya PERINGATAN G-SITASI-ULANG pada tahap draf"; status=1; fi
keluaran=$(python3 harness/harness.py --buku harness/uji-buku --bab babsitasiulang --tahap akhir 2>&1)
if echo "$keluaran" | grep -q "\[GAGAL\] G-SITASI-ULANG"; then echo "benar: babsitasiulang GAGAL di G-SITASI-ULANG (--tahap akhir)"
else echo "SALAH: babsitasiulang seharusnya GAGAL di G-SITASI-ULANG (--tahap akhir)"; status=1; fi
# Sumber ganda (keputusan 2026-11-12): bukti "berkas" dicari di sumber utama dulu, lalu di
# versi kedua sumber/versi2/<berkas>; laporan menyebut versi yang cocok. babsumberganda memakai
# uji-buku/sumber/: kutipan hanya di utama (hlm. PDF 1), hanya di versi kedua (tanpa penanda
# halaman), di keduanya (utama menang, hlm. PDF 2, melintasi baris), dan di tidak satu pun (GAGAL).
temuan=$(python3 -c "import sys, pathlib; sys.path.insert(0, 'harness'); import harness, referensi
q = pathlib.Path('harness/uji-buku/babsumberganda.qmd'); prosa, _ = harness.pilah_qmd(q.read_text(encoding='utf-8'))
m, r = referensi.periksa(q, 'babsumberganda', prosa, pathlib.Path('harness/uji-buku/pustaka.bib').read_text(encoding='utf-8'))
print(len(m)); print(*m, sep='\n'); print(*r, sep='\n')" 2>&1)
if [ "$(echo "$temuan" | head -1)" = "1" ] \
   && echo "$temuan" | grep -qF "kutipan tidak ditemukan di contoh-sumber.md maupun versi2/contoh-sumber.md: 'This passage appears in neither version'" \
   && echo "$temuan" | grep -qF "contoh-sumber.md [utama] hlm. PDF 1" \
   && echo "$temuan" | grep -qF "versi2/contoh-sumber.md [versi kedua] tanpa penanda halaman" \
   && echo "$temuan" | grep -qF "contoh-sumber.md [utama] hlm. PDF 2" \
   && echo "$temuan" | grep -qF "3 bukti diperiksa ulang otomatis, 0 bukti web tercatat; 1 bukti hanya cocok di sumber versi kedua (versi2/)"; then
  echo "benar: sumber ganda (utama dulu, lalu versi2/; versi yang cocok dilaporkan)"
else echo "SALAH: sumber ganda seharusnya utama → versi2/ dengan satu kutipan hilang (dapat: $temuan)"; status=1; fi
keluaran=$(python3 harness/harness.py --buku harness/uji-buku --bab babsumberganda 2>&1)
if echo "$keluaran" | grep -q "^Status:" && echo "$keluaran" | grep -q "\[GAGAL\] G-REFERENSI"; then
  echo "benar: babsumberganda GAGAL di G-REFERENSI (kutipan tidak ada di versi mana pun)"
else echo "SALAH: babsumberganda seharusnya GAGAL di G-REFERENSI"; status=1; fi
# (bukti jenis hitung memakai Rscript; dilewati tanpa R)
if [ $ADA_R = 1 ]; then
  # Sesudah sitasi digabung: babsitasigabung memuat kalimat "Sumber yang sama juga menunjukkan …"
  # dan paragraf dua baris yang sitasinya di baris pertama sementara penanda klaimnya di baris
  # kedua. Klaim kalimat tanpa @kunci tetap di klaim.json dengan "sitasi_di" dan bukti hitung
  # yang diperiksa ulang. G-SITASI-ULANG, G-REFERENSI, G-SITASI, G-ATRIBUSI harus LULUS.
  keluaran=$(python3 harness/harness.py --buku harness/uji-buku --bab babsitasigabung --tahap akhir 2>&1)
  if echo "$keluaran" | grep -q "\[LULUS\] G-SITASI-ULANG" && echo "$keluaran" | grep -q "3 bukti diperiksa ulang otomatis" \
     && ! echo "$keluaran" | grep -q "\[GAGAL\] G-\(SITASI-ULANG\|REFERENSI\|SITASI\|ATRIBUSI\)\b"; then
    echo "benar: babsitasigabung (sitasi_di) lolos G-SITASI-ULANG, G-REFERENSI, G-SITASI, G-ATRIBUSI"
  else echo "SALAH: babsitasigabung seharusnya lolos G-SITASI-ULANG, G-REFERENSI, G-SITASI, G-ATRIBUSI"; status=1; fi
  # Entri sitasi_di tetap diperiksa: paragraf tanpa sitasi sumbernya dan bukti hitung yang salah GAGAL
  keluaran=$(python3 harness/harness.py --buku harness/uji-buku --bab babsitasilepas 2>&1)
  if echo "$keluaran" | grep -q "\[GAGAL\] G-REFERENSI" && echo "$keluaran" | grep -qF "tidak menyitasi @gelman2021 sebelumnya" \
     && echo "$keluaran" | grep -qF "hitungan 0.666667 ≠ nilai sumber 0.75"; then
    echo "benar: babsitasilepas GAGAL di G-REFERENSI (sitasi_di tak tertaut, bukti salah)"
  else echo "SALAH: babsitasilepas seharusnya GAGAL di G-REFERENSI (sitasi_di tak tertaut, bukti salah)"; status=1; fi
else
  echo "dilewati: babsitasigabung dan babsitasilepas (bukti hitung butuh R)"
fi
# G-TAG (PDF bertag) diuji pada PDF fikstur tanpa render: tag-tanpa.pdf
# (pdfLaTeX/LuaLaTeX tanpa DocumentMetadata) GAGAL, tag-baik.pdf LULUS.
if command -v pdfinfo > /dev/null; then
  if python3 harness/harness.py --tag-pdf harness/uji-buku/tag-tanpa.pdf > /dev/null 2>&1; then
    echo "SALAH: tag-tanpa.pdf seharusnya GAGAL (G-TAG)"; status=1
  else
    echo "benar: tag-tanpa.pdf GAGAL (G-TAG)"
  fi
  if python3 harness/harness.py --tag-pdf harness/uji-buku/tag-baik.pdf > /dev/null 2>&1; then
    echo "benar: tag-baik.pdf LULUS (G-TAG)"
  else
    echo "SALAH: tag-baik.pdf seharusnya LULUS (G-TAG)"; status=1
  fi
else
  echo "dilewati: G-TAG (pdfinfo/poppler-utils tidak terpasang)"
fi
# G-HURUF: huruf tersemat harus keluarga opsi. huruf-baik.pdf (gaya_gambar,
# Libertinus) LULUS untuk libertinus dan GAGAL untuk springer; huruf-asing.pdf
# (matplotlib bawaan: DejaVu Sans + Inter sebagai cadangan glif) GAGAL.
if command -v pdffonts > /dev/null; then
  for kasus in "huruf-baik libertinus LULUS" "huruf-baik springer GAGAL" "huruf-asing libertinus GAGAL"; do
    set -- $kasus
    if python3 harness/harness.py --huruf-pdf harness/uji-buku/huruf/$1.pdf --huruf $2 > /dev/null 2>&1; then
      hasil=LULUS
    else
      hasil=GAGAL
    fi
    if [ "$hasil" = "$3" ]; then echo "benar: G-HURUF $1 ($2) $hasil"; else echo "SALAH: G-HURUF $1 ($2) seharusnya $3"; status=1; fi
  done
else
  echo "dilewati: G-HURUF (pdffonts/poppler-utils tidak terpasang)"
fi
# G-DOCX-RUMUS dan G-DOCX pada DOCX fikstur (dibuat Pandoc dari reference-b5.docx):
# rumus-baik.docx (5 rumus OMML dari rumus-baik.qmd) LULUS; rumus-gagal.docx (TeX
# mentah di teks, gambar beralt "rumus") GAGAL; docx-baik.docx (word-otomatis.lua) LULUS;
# docx-gagal.docx ("??" dan @fig- mentah) GAGAL.
for kasus in "rumus-baik --docx-rumus LULUS" "rumus-gagal --docx-rumus GAGAL" \
             "docx-baik --docx-cek LULUS" "docx-gagal --docx-cek GAGAL"; do
  set -- $kasus
  tambahan=""; [ "$2" = --docx-rumus ] && tambahan="--sumber harness/uji-buku/docx/rumus-baik.qmd"
  if python3 harness/harness.py $2 harness/uji-buku/docx/$1.docx $tambahan > /dev/null 2>&1; then
    hasil=LULUS
  else
    hasil=GAGAL
  fi
  if [ "$hasil" = "$3" ]; then echo "benar: ${2#--} $1 $hasil"; else echo "SALAH: ${2#--} $1 seharusnya $3"; status=1; fi
done
# G-DOCX, fitur otomatis Word (word-otomatis.lua; fikstur dari uji-buku/docx/buat_fikstur.py):
# setiap fikstur GAGAL dengan pesan pemeriksaannya sendiri; docx-baik di atas LULUS.
# Sitasi Zotero (zotero-word.lua): docx-baik memuat 2 bidang ZOTERO_ITEM, 1 ZOTERO_BIBL,
# dan ZOTERO_PREF_1-2; docx-zotero (JSON rusak) dan docx-tanpa-otomatis (sitasi statis
# citeproc biasa) GAGAL.
for kasus in "docx-tanpa-otomatis|bidang SEQ Persamaan" "docx-ref|menunjuk bookmark yang tidak ada" \
             "docx-daftar|TOC Daftar Gambar" "docx-hakcipta|hak cipta sesudah daftar isi" \
             "docx-alt|tanpa teks alternatif" "docx-margin|seharusnya 28/28/22/24 mm" \
             "docx-zotero|JSON ZOTERO_ITEM tidak sah" "docx-tanpa-otomatis|sitasi statis"; do
  f=${kasus%%|*}; pesan=${kasus#*|}
  keluaran=$(python3 harness/harness.py --docx-cek harness/uji-buku/docx/$f.docx 2>&1)
  if [ $? -ne 0 ] && printf '%s' "$keluaran" | grep -qF "$pesan"; then
    echo "benar: docx-cek $f GAGAL ($pesan)"
  else
    echo "SALAH: docx-cek $f seharusnya GAGAL dengan '$pesan'"; status=1
  fi
done
# G-LN: \log tanpa basis di rumus prosa GAGAL (babln); babbaik memuat \ln,
# \log_{10}, kode log() dan R inline log() dan harus bersih.
for bab in babln babbaik; do
  if python3 -c "import sys; sys.path.insert(0, 'harness'); import harness
sys.exit(1 if harness.masalah_ln(open('harness/uji-buku/$bab.qmd', encoding='utf-8').read()) else 0)"; then
    hasil=LULUS
  else
    hasil=GAGAL
  fi
  harap=LULUS; [ "$bab" = babln ] && harap=GAGAL
  if [ "$hasil" = "$harap" ]; then echo "benar: G-LN $bab $hasil"; else echo "SALAH: G-LN $bab seharusnya $harap"; status=1; fi
done
# G-LOG: log LaTeX akhir yang meminta kompilasi ulang atau memuat label ganda
# GAGAL. Fikstur berakhiran .txt karena kemas_sumber.py membuang *.log.
for log in rerun ganda bersih; do
  if python3 -c "import sys; sys.path.insert(0, 'harness'); import harness
sys.exit(1 if harness.masalah_log_latex(open('harness/uji-buku/log/$log.txt', encoding='utf-8').read()) else 0)"; then
    hasil=LULUS
  else
    hasil=GAGAL
  fi
  harap=GAGAL; [ "$log" = bersih ] && harap=LULUS
  if [ "$hasil" = "$harap" ]; then echo "benar: G-LOG $log $hasil"; else echo "SALAH: G-LOG $log seharusnya $harap"; status=1; fi
done
# G-SELARAS (prototipe, WARNING; 2026-11-11): babselaras.qmd memuat kasus salah (tabel 0,254
# tiga desimal, narasi 0,25 dua desimal untuk sel yang sama) dan kasus benar (tabel dan
# narasi R-hat sama-sama tiga desimal). Hanya kasus salah yang ditandai; tingkat WARNING
# tidak menggagalkan (status 0), SELARAS=gagal menggagalkan (status 1).
keluar=$(python3 harness/harness.py --selaras harness/uji-buku/babselaras.qmd 2>&1); kode=$?
if [ $kode -eq 0 ] && echo "$keluar" | grep -q "tbl-selaras-salah" && ! echo "$keluar" | grep -q "tbl-selaras-benar"; then
  echo "benar: G-SELARAS WARNING hanya kasus salah"
else
  echo "SALAH: G-SELARAS seharusnya WARNING untuk tbl-selaras-salah saja (status $kode)"; status=1
fi
if SELARAS=gagal python3 harness/harness.py --selaras harness/uji-buku/babselaras.qmd > /dev/null 2>&1; then
  echo "SALAH: G-SELARAS ketat seharusnya GAGAL"; status=1
else
  echo "benar: G-SELARAS ketat GAGAL"
fi
rm -rf lampiran-kode/harness harness/laporan/harness_uji-buku-*
exit $status
