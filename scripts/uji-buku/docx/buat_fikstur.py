#!/usr/bin/env python3
"""Bangun ulang fikstur G-DOCX (fitur otomatis Word) dengan Pandoc dan Pillow:
  docx-baik.docx            docx-baik.md + tiruan-quarto.lua + word-otomatis.lua (LULUS)
  docx-tanpa-otomatis.docx  tanpa word-otomatis.lua: SEQ, TOC, hak cipta (GAGAL)
  docx-ref.docx             REF ke bookmark yang tidak ada (GAGAL)
  docx-daftar.docx          tanpa bidang TOC Daftar Gambar (GAGAL)
  docx-hakcipta.docx        halaman hak cipta sesudah daftar isi (GAGAL)
  docx-alt.docx             gambar tanpa teks alternatif (GAGAL)
  docx-margin.docx          margin kiri 22 mm, bukan 28 mm (GAGAL)
docx-gagal.docx ("??", @fig- mentah, gambar lebar) tidak dibangun di sini.
Pemakaian (dari folder ini): python3 buat_fikstur.py
"""
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

DI = Path(__file__).resolve().parent
SKRIP = DI.parent.parent          # scripts/ (skill) atau harness/ (proyek)
REF = next(p for p in [SKRIP.parent / "assets" / "reference-b5.docx",
                       SKRIP.parent / "_bersama" / "reference-b5.docx"] if p.exists())
LUA = next(p for p in [SKRIP / "word-otomatis.lua", SKRIP.parent / "_bersama" / "word-otomatis.lua"]
           if p.exists())


def render(tujuan, otomatis=True):
    from PIL import Image
    with tempfile.TemporaryDirectory() as t:
        Image.new("RGB", (400, 200), "white").save(Path(t) / "kecil.png", dpi=(100, 100))
        shutil.copy(DI / "docx-baik.md", Path(t) / "a.md")
        perintah = ["pandoc", "a.md", "-t", "docx", "--reference-doc", str(REF),
                    "--lua-filter", str(DI / "tiruan-quarto.lua")]
        if otomatis:
            perintah += ["--lua-filter", str(LUA)]
        subprocess.run(perintah + ["-o", str(tujuan)], cwd=t, check=True)


def ubah(sumber, tujuan, fungsi):
    with zipfile.ZipFile(sumber) as zin, zipfile.ZipFile(tujuan, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                baru = fungsi(data.decode("utf-8"))
                assert baru != data.decode("utf-8"), tujuan
                data = baru.encode("utf-8")
            zout.writestr(item, data)


def pindah_hak_cipta(x):
    pars = re.findall(r'<w:p><w:pPr><w:pStyle w:val="HakCipta" ?/>.*?</w:p>', x, flags=re.S)
    for par in pars:
        x = x.replace(par, "", 1)
    return x.replace("<w:sectPr", "".join(pars) + "<w:sectPr", 1)


baik = DI / "docx-baik.docx"
render(baik)
render(DI / "docx-tanpa-otomatis.docx", otomatis=False)
ubah(baik, DI / "docx-ref.docx", lambda x: x.replace("REF _Ref_fig_kecil", "REF _Ref_fig_hilang", 1))
ubah(baik, DI / "docx-daftar.docx", lambda x: x.replace('\\c &quot;Gambar&quot;', '\\c &quot;Foto&quot;')
     .replace('\\c "Gambar"', '\\c "Foto"'))
ubah(baik, DI / "docx-hakcipta.docx", pindah_hak_cipta)
ubah(baik, DI / "docx-alt.docx", lambda x: re.sub(r'descr="[^"]*"', 'descr=""', x))
ubah(baik, DI / "docx-margin.docx", lambda x: re.sub(r'(<w:pgMar [^>]*w:left=)"\d+"', r'\1"1247"', x))
print("fikstur G-DOCX dibangun ulang di", DI)
