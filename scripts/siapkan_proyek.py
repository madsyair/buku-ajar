#!/usr/bin/env python3
"""Siapkan tata letak proyek buku ajar dari skill buku-ajar.

Membuat (tanpa menimpa berkas yang sudah ada, kecuali --timpa):
  <proyek>/harness/       harness.py, referensi.py, penggalan.py, cek_rumus.py, kemas_sumber.py,
                          uji_harness.sh, uji-buku/, klaim.json, referensi.json,
                          pengecualian.json, konfig.json, sumber/, laporan/
  <proyek>/_bersama/      gaya_gambar.py, catatan.lua, bahasa-asing.lua,
                          tikz-preamble.tex, preamble.tex, doc-class.tex,
                          apa.csl, reference-b5.docx
  <proyek>/KEPUTUSAN-RANCANGAN.md, REVISI.md, .gitignore
  <proyek>/<buku>/        _quarto.yml, pustaka.bib, index.qmd, references.qmd,
                          naskah/{00-brief.md, 01-rancangan-rinci.md, keputusan-istilah.md,
                          STATUS.md, 03-kerangka/, ulasan/}
  <proyek>/lampiran-kode/<buku>/

Pemakaian:
  python3 <skill>/scripts/siapkan_proyek.py --proyek ~/sumber/seri-x --buku buku1 \
      --judul "Dasar-Dasar Statistika" --penulis "Nama Penulis"
  python3 <skill>/scripts/siapkan_proyek.py --proyek ~/sumber/seri-x --buku kunci-buku1 \
      --judul "Kunci Jawaban dan Pembahasan untuk Pengajar"
"""
import argparse
import json
import shutil
from datetime import date
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SKRIP = SKILL / "scripts"
ASET = SKILL / "assets"


def salin(sumber, tujuan, timpa):
    tujuan.parent.mkdir(parents=True, exist_ok=True)
    if tujuan.exists() and not timpa:
        print(f"  ada, dilewati: {tujuan}")
        return
    if sumber.is_dir():
        shutil.copytree(sumber, tujuan, dirs_exist_ok=True)
    else:
        shutil.copy(sumber, tujuan)
    print(f"  dibuat: {tujuan}")


def tulis(tujuan, isi, timpa):
    tujuan.parent.mkdir(parents=True, exist_ok=True)
    if tujuan.exists() and not timpa:
        print(f"  ada, dilewati: {tujuan}")
        return
    tujuan.write_text(isi, encoding="utf-8")
    print(f"  dibuat: {tujuan}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proyek", required=True)
    ap.add_argument("--buku", required=True, help="nama folder buku, mis. buku1 atau kunci-buku1")
    ap.add_argument("--judul", required=True)
    ap.add_argument("--penulis", default="Nama Penulis (tanpa gelar)")
    ap.add_argument("--timpa", action="store_true")
    a = ap.parse_args()
    P = Path(a.proyek).expanduser().resolve()
    B = P / a.buku
    t = a.timpa
    print(f"Proyek {P}, buku {a.buku}")

    # harness
    for f in ["harness.py", "referensi.py", "penggalan.py", "cek_rumus.py", "kemas_sumber.py", "uji_harness.sh"]:
        salin(SKRIP / f, P / "harness" / f, t)
    salin(SKRIP / "uji-buku", P / "harness" / "uji-buku", t)
    tulis(P / "harness" / "klaim.json", "[]\n", False)
    tulis(P / "harness" / "referensi.json", "{}\n", False)
    tulis(P / "harness" / "pengecualian.json", json.dumps(
        {"angka-tetap": {}, "eyd-abaikan": [], "gaya-abaikan": [], "konjungsi-abaikan": [],
         "larangan-abaikan": [], "istilah-abaikan": [], "ln-abaikan": []}, indent=1) + "\n", False)
    salin(ASET / "konfig.json", P / "harness" / "konfig.json", False)
    (P / "harness" / "sumber").mkdir(parents=True, exist_ok=True)
    (P / "harness" / "laporan").mkdir(parents=True, exist_ok=True)

    # folder bersama
    for f in ["gaya_gambar.py", "catatan.lua", "bahasa-asing.lua"]:
        salin(SKRIP / f, P / "_bersama" / f, t)
    for f in ["tikz-preamble.tex", "preamble.tex", "doc-class.tex", "apa.csl",
              "reference-b5.docx", "hak-cipta.tex"]:
        salin(ASET / f, P / "_bersama" / f, t)

    # dokumen proyek
    salin(ASET / "templat-KEPUTUSAN-RANCANGAN.md", P / "KEPUTUSAN-RANCANGAN.md", False)
    salin(ASET / "templat-REVISI.md", P / "REVISI.md", False)
    tulis(P / ".gitignore", "\n".join([
        "_book/", "build/", ".quarto/", "fit/", "*_files/", "__pycache__/",
        "harness/sumber/", "harness/laporan/", "*.log", "*.aux", "*.rds", ""]), False)

    # buku
    q = (ASET / "_quarto.yml").read_text(encoding="utf-8")
    q = q.replace('"JUDUL BUKU"', json.dumps(a.judul, ensure_ascii=False))
    q = q.replace('"PENULIS"', json.dumps(a.penulis, ensure_ascii=False))
    q = q.replace("{JUDUL BUKU}{PENULIS}{2026}", "{" + a.judul + "}{" + a.penulis + "}{" + f"{date.today():%Y}" + "}")
    q = q.replace('date: "2026-11-07"', f'date: "{date.today():%Y-%m-%d}"')
    tulis(B / "_quarto.yml", q, t)
    tulis(B / "pustaka.bib", "", False)
    tulis(B / "index.qmd", "# Prakata {.unnumbered}\n\nTujuan penulisan, pembaca sasaran, "
          "keunggulan buku, dan cara memakai buku ini.\n\n## Data yang digunakan dan batasannya "
          "{.unnumbered}\n\nJenis data (riil, sintetis paket, simulasi), alasannya, dan rujukan ke "
          "lampiran Sumber Data.\n", False)
    tulis(B / "references.qmd", "# Daftar Pustaka {.unnumbered}\n\n::: {#refs}\n:::\n", False)
    N = B / "naskah"
    salin(ASET / "templat-brief.md", N / "00-brief.md", False)
    salin(ASET / "templat-rancangan-rinci.md", N / "01-rancangan-rinci.md", False)
    salin(ASET / "templat-STATUS.md", N / "STATUS.md", False)
    tulis(N / "keputusan-istilah.md", "# Keputusan istilah\n\nLihat skill buku-ajar "
          "references/istilah-statistika.md (format tabel dan keputusan bawaan).\n\n"
          "| Istilah Inggris | Bentuk di buku | Keputusan | Alasan | Bab |\n"
          "| --- | --- | --- | --- | --- |\n", False)
    if a.buku.startswith("kunci-"):
        salin(ASET / "templat-temuan-soal.md", N / "temuan-soal.md", False)
    (N / "03-kerangka").mkdir(parents=True, exist_ok=True)
    (N / "ulasan").mkdir(parents=True, exist_ok=True)
    (P / "lampiran-kode" / a.buku).mkdir(parents=True, exist_ok=True)
    print("Selesai. Langkah berikut: isi naskah/00-brief.md, sesuaikan harness/konfig.json, "
          "lalu jalankan: bash harness/uji_harness.sh")


if __name__ == "__main__":
    main()
