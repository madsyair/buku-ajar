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
GAGAL="babgagal babbahasa babbocor babsitasi babcap babgayasitasi babinf babjudul bablarangan"
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
rm -rf lampiran-kode/harness harness/laporan/harness_uji-buku-*
exit $status
