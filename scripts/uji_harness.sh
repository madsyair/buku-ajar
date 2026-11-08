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
GAGAL="babgagal babbahasa babbocor babsitasi babcap babgayasitasi babinf babjudul bablarangan babln"
for bab in $GAGAL; do
  if python3 harness/harness.py --buku harness/uji-buku --bab "$bab" > /dev/null 2>&1; then
    echo "SALAH: $bab seharusnya GAGAL"; status=1
  else
    echo "benar: $bab GAGAL"
  fi
done
if python3 harness/harness.py --buku harness/uji-buku --bab babbaik > /dev/null 2>&1; then
  echo "benar: babbaik LULUS"
else
  echo "SALAH: babbaik seharusnya LULUS"; status=1
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
# mentah di teks, gambar beralt "rumus") GAGAL; docx-baik.docx LULUS; docx-gagal.docx
# ("??" dan @fig- mentah) GAGAL.
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
rm -rf lampiran-kode/harness harness/laporan/harness_uji-buku-*
exit $status
