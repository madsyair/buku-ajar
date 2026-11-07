#!/usr/bin/env python3
"""Harness verifikasi naskah buku ajar (skill buku-ajar).

Digeneralisasi dari harness seri Statistika Bayesian (A. S. Choir, 2026).
Setiap bab harus lolos semua gerbang sebelum dianggap selesai (loop: tulis →
harness → perbaiki → harness lagi). Penjelasan setiap gerbang dan cara menambah
gerbang baru ada di references/harness-dan-gerbang.md skill. Gerbang:

  G-KODE       semua chunk R/Python berjalan saat bab dirajut (knitr)
  G-LAMPIRAN   kode lampiran (R hasil purl + Python gambar) berjalan mandiri
  G-ANGKA      angka hasil hitung di prosa wajib berasal dari kode R inline
  G-KELUARAN   tidak ada keluaran yang diketik tangan di komentar kode
  G-LEBAR-KODE baris R maksimal 72 karakter, Python 79 (tidak terpotong di B5)
  G-BOCOR      tidak ada peringatan, galat, atau repr objek yang tercetak di buku
  G-PYTHON     potongan Python tidak mengambil objek R (r.) dan tidak menghitung model
  G-RUJUKAN    setiap rujukan @fig/@tbl/@eq/@sec dan [@kunci] punya sasaran
  G-SITASI     sitasi penulis–tahun tanpa lokasi; penulis sebagai pelaku → sitasi naratif
  G-REFERENSI  setiap sitasi punya klaim terverifikasi; kutipan bukti ada di sumbernya
  G-EYD        pemeriksa EYD V (skill eyd) tanpa ERROR
  G-GAYA       anti-slop, larangan "di mana", koma, sains (skill math-article)
  G-PARAGRAF   paragraf isi 2–6 kalimat (aturan longgar untuk buku)
  G-RENDER     buku dirender ke PDF dan Word tanpa galat (opsi --render)
  G-PENGGALAN  pemenggalan kata EYD V (kamus Sastrawi + uji contoh resmi; audit PDF)
  G-LEBAR-KELUARAN keluaran kode tercetak <= 78 karakter (TEPI=1)
  G-JUDUL      judul tabel/gambar singkat, panel (a)(b), subjudul bukan kalimat tanya
  G-KONJUNGSI  tanpa koma sebelum penghubung subordinatif (KONJUNGSI=1)
  G-PERSAMAAN  "persamaan" huruf kecil di tengah kalimat; @Eq- di awal kalimat
  G-ATRIBUSI   hanya penulis orang yang menjadi subjek pernyataan bersitasi
  G-SLOP       frasa basa-basi dan kosakata khas tulisan mesin (bahasa Indonesia)
  G-LARANGAN   kata terlarang di naskah (bawaan: nama teknik pengajaran)
  G-ISTILAH    istilah yang sudah diputuskan diganti (konfig.json "istilah_terlarang")
  G-TEPI       tidak ada isi melewati tepi halaman > 3 pt (setelah --render)
  G-TAG        PDF bertag: Tagged yes, pohon struktur Document/H1/P/Figure, /Lang id-ID
               (setelah --render; TAG=0 mematikan untuk proyek tanpa DocumentMetadata)
  G-LOG        log LaTeX akhir stabil: tanpa "Rerun to correct", "Label(s) may have
               changed", "Rerun to get", atau label "multiply defined" (setelah --render)
  G-LN         logaritma natural ditulis ln di rumus naskah; log hanya dengan
               subskrip basis (log_{10}); kode tetap log() (LN=0 mematikan)
  G-HALJUDUL   _quarto.yml tanpa subtitle; date ISO; date-format "[Draf revisi ke-N · ]..." (DRAF=1)

Tata letak proyek yang diharapkan (jalur dapat diubah di harness/konfig.json):
  <proyek>/harness/{harness.py, referensi.py, penggalan.py, klaim.json,
                    referensi.json, pengecualian.json, konfig.json, sumber/}
  <proyek>/_bersama/{gaya_gambar.py, catatan.lua, bahasa-asing.lua, tikz-preamble.tex, ...}
  <proyek>/<buku>/{_quarto.yml, pustaka.bib, bab01.qmd, ...}
  <proyek>/lampiran-kode/<buku>/   (dibangkitkan G-LAMPIRAN)

Pemakaian:
  python3 harness/harness.py --buku buku1 --bab bab02
  python3 harness/harness.py --buku buku1 --bab bab02 --render
  python3 harness/harness.py --tag-pdf buku1/_book/buku.pdf     # G-TAG saja
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
def _cari_skill(env, relatif):
    """Lokasi skrip skill: variabel lingkungan, lalu folder skill yang dikenal."""
    if os.environ.get(env):
        return Path(os.environ[env])
    calon = [Path("/mnt/skills/plugins") / relatif]
    calon += sorted(Path("/root/.claude/skills").glob(f"**/{relatif}"))
    for c in calon:
        if c.exists():
            return c
    return calon[0]


SKILL_EYD = _cari_skill("SKILL_EYD", "eyd/scripts/periksa.py")
SKILL_GAYA = _cari_skill("SKILL_GAYA", "math-article/scripts/harness_check.py")
PENGECUALIAN = AKAR / "harness" / "pengecualian.json"

# ---------------------------------------------------------------- konfigurasi proyek
# Semua yang khusus proyek dipindah ke harness/konfig.json (opsional). Nilai
# bawaan di bawah dipakai bila berkas atau kuncinya tidak ada.
KONFIG_BAWAAN = {
    "bersama": "_bersama",            # folder preamble, filter Lua, gaya_gambar.py
    "lampiran": "lampiran-kode",      # folder skrip lampiran yang dibangkitkan
    "id_bab_polos": [],               # buku yang kunci klaimnya tanpa awalan folder
    "penulis": [],                    # nama penulis tambahan untuk G-SITASI
    # Kata yang tidak boleh muncul di naskah buku (pola regex, tanpa beda huruf besar/kecil)
    "larangan": [
        {"pola": r"\bsokrat\w*|\bsocrat\w*|\bsokrates\b|\bsocrates\b",
         "saran": "nama teknik pengajaran tidak ditulis di naskah; biarkan pertanyaan bekerja tanpa label"},
        {"pola": r"\bfeynman\b",
         "saran": "nama teknik pengajaran tidak ditulis di naskah; hapus labelnya"},
    ],
    # Istilah yang sudah diputuskan penulis: pola regex -> saran (dan tanggal keputusan)
    "istilah_terlarang": [],
}


def muat_konfig():
    k = dict(KONFIG_BAWAAN)
    berkas = AKAR / "harness" / "konfig.json"
    if berkas.exists():
        k.update(json.loads(berkas.read_text(encoding="utf-8")))
    return k


KONFIG = muat_konfig()
BERSAMA = AKAR / KONFIG["bersama"]

hasil = []  # (gerbang, lulus, rincian)


def catat(gerbang, lulus, rincian=""):
    hasil.append((gerbang, lulus, rincian.strip()))
    tanda = "LULUS" if lulus else "GAGAL"
    print(f"[{tanda}] {gerbang}")
    if rincian and not lulus:
        for baris in rincian.strip().splitlines()[:40]:
            print("    " + baris)


def jalankan(perintah, cwd, env=None, batas=3600):
    lingk = dict(os.environ)
    # Python yang memuat matplotlib dan seaborn: variabel lingkungan bila ada,
    # lalu python3 pertama di PATH (dulu dipatok /usr/bin/python3)
    lingk.setdefault("RETICULATE_PYTHON", shutil.which("python3") or "/usr/bin/python3")
    if env:
        lingk.update(env)
    p = subprocess.run(perintah, cwd=cwd, env=lingk, capture_output=True,
                       text=True, timeout=batas)
    return p.returncode, p.stdout + p.stderr


def muat_pengecualian():
    if PENGECUALIAN.exists():
        return json.loads(PENGECUALIAN.read_text(encoding="utf-8"))
    return {"angka-tetap": {}, "eyd-abaikan": [], "gaya-abaikan": []}


# ---------------------------------------------------------------- pemilahan qmd
POLA_CHUNK = re.compile(r"^```\{(\w+)[^}]*\}\s*$")


def pilah_qmd(teks):
    """Kembalikan (baris_prosa, daftar_chunk). Chunk = (bahasa, isi, baris_awal)."""
    baris = teks.splitlines()
    prosa, chunk = [], []
    i, n = 0, len(baris)
    if n and baris[0].strip() == "---":  # YAML depan
        j = 1
        while j < n and baris[j].strip() != "---":
            j += 1
        i = j + 1
    dalam_pagar = None
    while i < n:
        b = baris[i]
        m = POLA_CHUNK.match(b)
        if dalam_pagar is None and m:
            bahasa, isi, awal = m.group(1), [], i + 1
            i += 1
            while i < n and not baris[i].startswith("```"):
                isi.append(baris[i])
                i += 1
            chunk.append((bahasa, "\n".join(isi), awal))
            i += 1
            continue
        if b.startswith("```"):  # blok kode biasa (bukan chunk) → bukan prosa
            dalam_pagar = None if dalam_pagar else "pagar"
            i += 1
            continue
        if dalam_pagar is None:
            prosa.append((i + 1, b))
        i += 1
    return prosa, chunk


def bersihkan_baris_prosa(b):
    b = re.sub(r"<!--.*?-->", " ", b)
    b = re.sub(r"`r [^`]*`", " ", b)       # kode R inline (angka sah)
    b = re.sub(r"`[^`]*`", " ", b)          # kode inline lain
    b = re.sub(r"\$\$.*?\$\$", " ", b)
    b = re.sub(r"\$[^$]*\$", " ", b)        # matematika inline
    b = re.sub(r"\{#[^}]*\}", " ", b)       # label
    b = re.sub(r"\]\([^)]*\)", "]", b)      # URL tautan/gambar
    b = re.sub(r"\[@[^\]]*\]|@\w[\w:-]*", " ", b)  # sitasi dan rujukan silang
    return b


# ---------------------------------------------------------------- G-ANGKA
POLA_ANGKA = [
    ("desimal", re.compile(r"(?<![\w.,])\d+,\d+(?![\w,])")),
    ("persen", re.compile(r"(?<![\w.,])\d+(?:,\d+)?\s?(?:%|persen\b)")),
    ("ribuan", re.compile(r"(?<![\w.,])\d{1,3}(?:\.\d{3})+(?![\w.])")),
]


def id_bab(buku, bab):
    """Kunci bab di klaim.json dan pengecualian.json: nama folder buku + bab,
    mis. 'buku2/bab01', agar bab bernomor sama di buku lain tidak bertabrakan.
    Buku yang terdaftar di konfig 'id_bab_polos' (registri lama) memakai nama
    bab saja."""
    nama = Path(buku).name
    return bab if nama in set(KONFIG["id_bab_polos"]) | {"uji-buku"} else f"{nama}/{bab}"


def gerbang_angka(qmd, bab, peng):
    teks = qmd.read_text(encoding="utf-8")
    prosa, _ = pilah_qmd(teks)
    izin = {d["teks"] for d in peng.get("angka-tetap", {}).get(bab, [])}
    dalam_math = False
    temuan = []
    for nomor, b in prosa:
        if b.strip().startswith("$$"):
            dalam_math = not (b.strip().count("$$") == 2) and not dalam_math
            continue
        if dalam_math:
            continue
        bersih = bersihkan_baris_prosa(b)
        for jenis, pola in POLA_ANGKA:
            for m in pola.finditer(bersih):
                token = m.group(0).strip()
                if token not in izin:
                    temuan.append(f"baris {nomor}: {jenis} '{token}' diketik tangan; "
                                  f"hitung dengan `r ...` atau daftarkan di angka-tetap")
    # Keterangan gambar/tabel yang diketik sebagai teks juga tampil sebagai prosa
    _, chunk = pilah_qmd(teks)
    for bahasa, isi, awal in chunk:
        for k, b in enumerate(isi.splitlines()):
            m = re.match(r"\s*[#%]\|\s*(?:fig|tbl)-cap:\s*(.*)$", b)
            if not m or m.group(1).strip().startswith("!expr"):
                continue
            for jenis, pola in POLA_ANGKA:
                for t in pola.finditer(m.group(1)):
                    if t.group(0).strip() not in izin:
                        temuan.append(f"baris {awal + k + 1}: {jenis} '{t.group(0).strip()}' di keterangan; "
                                      f"pakai fig-cap: !expr dengan angka()")
    catat("G-ANGKA", not temuan, "\n".join(temuan))


# ---------------------------------------------------------------- G-KELUARAN dan G-PYTHON
POLA_KOMENTAR_KELUARAN = re.compile(r"#\s*(?:>|\[1\]|[-−]?\d+(?:[.,]\d+)?(?:\s+[-−]?\d+(?:[.,]\d+)?)*\s*$)")


def gerbang_keluaran_python(qmd):
    _, chunk = pilah_qmd(qmd.read_text(encoding="utf-8"))
    salah_k, salah_p = [], []
    for bahasa, isi, awal in chunk:
        for k, b in enumerate(isi.splitlines()):
            if b.lstrip().startswith("#|"):
                continue
            pos = b.find("#")
            if pos >= 0 and POLA_KOMENTAR_KELUARAN.search(b[pos:]):
                salah_k.append(f"baris {awal + k + 1}: komentar menyerupai keluaran: {b.strip()}")
        if bahasa == "python":
            if re.search(r"\br\.\w", isi):
                salah_p.append(f"chunk baris {awal}: memakai objek R (r.) sehingga lampiran tidak mandiri")
            if re.search(r"\b(numpy\.random|np\.random|scipy\.stats|statsmodels|pymc)\b", isi):
                salah_p.append(f"chunk baris {awal}: Python menghitung angka; semua hitungan harus di R")
    catat("G-KELUARAN", not salah_k, "\n".join(salah_k))
    catat("G-PYTHON", not salah_p, "\n".join(salah_p))


# ---------------------------------------------------------------- G-LEBAR-KODE
# Baris R yang panjang terpotong di halaman B5; Python mengikuti PEP 8.
BATAS_LEBAR = {"r": 72, "python": 79}


def gerbang_lebar_kode(qmd):
    _, chunk = pilah_qmd(qmd.read_text(encoding="utf-8"))
    salah = []
    for bahasa, isi, awal in chunk:
        batas = BATAS_LEBAR.get(bahasa)
        if not batas:
            continue
        for k, b in enumerate(isi.splitlines()):
            if b.lstrip().startswith("#|"):
                continue
            if len(b) > batas:
                salah.append(f"baris {awal + k + 1}: {len(b)} karakter (batas {bahasa} {batas}): {b.strip()[:60]}…")
    catat("G-LEBAR-KODE", not salah, "\n".join(salah))


BATAS_LEBAR_KELUARAN = 78


def gerbang_lebar_keluaran(md):
    """Keluaran kode yang tercetak (baris '## ...' di rajutan) tidak boleh
    melewati tepi kanan; bungkus dengan strwrap()/width = 70 atau ringkas."""
    salah = []
    dalam = False
    for k, b in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
        if b.startswith("```"):
            dalam = not dalam
            continue
        if dalam and b.startswith("##") and len(b) > BATAS_LEBAR_KELUARAN:
            salah.append(f"knit.md baris {k}: keluaran {len(b)} karakter (batas {BATAS_LEBAR_KELUARAN}): {b[:60]}…")
    catat("G-LEBAR-KELUARAN", not salah, "\n".join(salah[:40]))


# ---------------------------------------------------------------- G-KONJUNGSI
# Kajian 2026-11-06 (kajian-koma-konjungsi.md): EYD V B.4 — tanpa koma bila
# induk kalimat mendahului anak kalimat (sehingga, karena, agar, jika, ...).
POLA_KONJ = re.compile(
    r",\s+(sehingga|karena(?!\s+itu)|sebab(?!\s+itu)|agar|supaya|bahwa|jika|bila|apabila|kalau|asalkan"
    r"|meskipun|walaupun|kendatipun|kendati|biarpun|ketika|sewaktu|setelah(?!\s+itu)|sesudah(?!\s+itu)"
    r"|sebelum(?!\s+itu|nya)|sejak(?!\s+itu)|selama(?!\s+itu))\b")


def gerbang_konjungsi(qmd, peng):
    prosa, _ = pilah_qmd(qmd.read_text(encoding="utf-8"))
    abaikan = peng.get("konjungsi-abaikan", [])
    masalah = []
    for nomor, b in prosa:
        if re.match(r"\s*(?:#|:::|\||[-*] |\d+\.)\s*$", b):
            continue
        bersih = re.sub(r"`[^`]*`", "X", b)
        bersih = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", "X", bersih)
        for m in re.finditer(r",\s+(karena|sebab)\s+itu\b", bersih):
            masalah.append(f"baris {nomor}: '{m.group(1)} itu' penghubung antarkalimat di tengah kalimat; "
                           f"pecah kalimat ('. Karena itu, …') atau tulis '… karena …'")
        for m in POLA_KONJ.finditer(bersih):
            sisa = bersih[m.end():]
            sisip = re.match(r"([^,.;:]*),", sisa)
            if sisip and len(sisip.group(1).split()) <= 3:
                continue  # keterangan sisipan, mis. ", bila perlu,"
            segmen = re.split(r"[,;:(]", bersih[:m.start()])
            if len(segmen) >= 2 and re.match(
                    r"\s*(?:bukan|misalnya|yaitu|yakni|seperti|termasuk|terutama|khususnya|antara lain"
                    r"|kecuali|selain|tidak hanya|baik)\b", segmen[-1]):
                continue  # koma menutup sisipan/aposisi (EYD V B.13)
            konteks = bersih[max(0, m.start() - 50):m.end() + 30]
            if any(a in bersih for a in abaikan):
                continue
            masalah.append(f"baris {nomor}: koma sebelum '{m.group(1)}' (induk mendahului anak kalimat; "
                           f"EYD V B.4): …{konteks.strip()}…")
    catat("G-KONJUNGSI", not masalah, "\n".join(masalah[:60]))


# ---------------------------------------------------------------- G-BOCOR
# Keluaran yang tidak boleh tampil di buku: peringatan pustaka, repr objek, galat.
POLA_BOCOR = [
    (r"findfont", "peringatan fon matplotlib"),
    (r"object at 0x[0-9a-f]+", "repr objek Python"),
    (r"^## (?:Warning|Peringatan)", "peringatan R"),
    (r"^## Error|Traceback \(most recent", "galat"),
    (r"<matplotlib\.|<Figure size", "repr gambar matplotlib"),
    # fig-cap: !expr yang tidak dievaluasi (mis. di chunk Python) tercetak
    # sebagai nama variabel: keterangan berupa satu pengenal tanpa spasi
    (r"!\[[A-Za-z_][\w.]*\]\(|alt=\"[A-Za-z_][\w.]*\"|fig-cap=\"[A-Za-z_][\w.]*\"",
     "keterangan gambar tak dievaluasi (nama variabel)"),
]


def gerbang_bocor(md):
    teks = md.read_text(encoding="utf-8")
    temuan = []
    for pola, jenis in POLA_BOCOR:
        for m in re.finditer(pola, teks, flags=re.M):
            baris = teks[:m.start()].count("\n") + 1
            temuan.append(f"{md.name} baris {baris}: {jenis}: {teks[m.start():m.start()+70].strip()}")
    # nilai tak hingga / tak terdefinisi yang tercetak di prosa (hasil R inline)
    prosa = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), teks, flags=re.S)
    prosa = re.sub(r"`[^`\n]*`", " ", prosa)
    for m in re.finditer(r"(?<![\w.])[\u2212-]?(?:Inf|NaN)\b|(?<![\w.])NA\b|&infin;", prosa):
        baris = prosa[:m.start()].count("\n") + 1
        temuan.append(f"{md.name} baris {baris}: nilai Inf/NaN/NA tercetak di prosa: "
                      f"{prosa[max(0, m.start()-40):m.start()+30].strip()}")
    catat("G-BOCOR", not temuan, "\n".join(temuan[:30]))


# ---------------------------------------------------------------- G-RUJUKAN
def gerbang_rujukan(qmd, buku):
    teks = qmd.read_text(encoding="utf-8")
    label = set(re.findall(r"[#%]\|\s*label:\s*((?:fig|tbl)-[\w-]+)", teks))
    label |= set(re.findall(r"\{#((?:fig|tbl|eq|sec)-[\w-]+)", teks))
    # label dari bab lain (rujukan antarbab)
    for lain in buku.glob("*.qmd"):
        if lain != qmd:
            t = lain.read_text(encoding="utf-8")
            label |= set(re.findall(r"\{#(sec-[\w-]+)", t))
            label |= set(re.findall(r"\{#(eq-[\w-]+)", t))
            label |= set(re.findall(r"[#%]\|\s*label:\s*((?:fig|tbl)-[\w-]+)", t))
    teks_tanpa_kode = re.sub(r"```\{.*?```", " ", teks, flags=re.S)
    dirujuk = {r[0].lower() + r[1:] for r in re.findall(r"@((?:fig|tbl|eq|sec|Fig|Tbl|Eq|Sec)-[\w-]+)", teks_tanpa_kode)}
    masalah = [f"rujukan @{r} tidak punya sasaran" for r in sorted(dirujuk - label)]
    masalah_ganda = []
    milik = set(re.findall(r"[#%]\|\s*label:\s*((?:fig|tbl)-[\w-]+)", teks))
    # label harus unik di seluruh buku: label ganda membuat rujukan menunjuk bab lain
    sendiri = milik | set(re.findall(r"\{#((?:sec|eq|fig|tbl)-[\w-]+)", teks))
    for lain in buku.glob("*.qmd"):
        if lain != qmd:
            t = lain.read_text(encoding="utf-8")
            punya = set(re.findall(r"[#%]\|\s*label:\s*((?:fig|tbl)-[\w-]+)", t))
            punya |= set(re.findall(r"\{#((?:sec|eq|fig|tbl)-[\w-]+)", t))
            for l in sorted(sendiri & punya):
                masalah_ganda.append(f"label {l} juga dipakai di {lain.name}; buat unik")
    masalah += [f"{l} tidak pernah dirujuk di teks" for l in sorted(milik - dirujuk)]
    bib = (buku / "pustaka.bib").read_text(encoding="utf-8") if (buku / "pustaka.bib").exists() else ""
    kunci = set(re.findall(r"@\w+\{([^,]+),", bib))
    for grup in re.findall(r"\[([^\]]*@[^\]]*)\]", teks_tanpa_kode):
        for k in re.findall(r"@([\w:-]+)", grup):
            if not re.match(r"(fig|tbl|eq|sec|Fig|Tbl|Eq|Sec)-", k) and k not in kunci:
                masalah.append(f"sitasi @{k} tidak ada di pustaka.bib")
    masalah += masalah_ganda
    catat("G-RUJUKAN", not masalah, "\n".join(masalah))



# ---------------------------------------------------------------- G-SITASI
# Gaya sitasi seri (keputusan penulis 2026-11-02): hanya penulis–tahun, tanpa
# lokasi bagian/halaman (lokasi disimpan di klaim.json sebagai catatan periksa);
# bila penulis disebut sebagai pelaku kalimat, pakai sitasi naratif @kunci.
def daftar_penulis(buku):
    """Nama keluarga penulis orang dari pustaka.bib buku, ditambah konfig 'penulis'.
    Dipakai G-SITASI untuk mengenali nama penulis yang ditulis manual di kalimat
    bersitasi kurung (seharusnya sitasi naratif @kunci)."""
    nama = set(KONFIG["penulis"])
    bib = buku / "pustaka.bib"
    if bib.exists():
        for m in re.finditer(r"\bauthor\s*=\s*\{(.*)\}\s*,?\s*$", bib.read_text(encoding="utf-8"), flags=re.M):
            nilai = m.group(1).strip()
            if nilai.startswith("{") and " and " not in nilai and "," not in nilai:
                continue  # penulis lembaga
            for orang in re.split(r"\s+and\s+", nilai):
                keluarga = orang.split(",")[0] if "," in orang else orang.split()[-1] if orang.split() else ""
                keluarga = re.sub(r"[{}\\\"'`^~]", "", keluarga).strip()
                if len(keluarga) >= 3 and keluarga[0].isupper() and keluarga.lower() != "others":
                    nama.add(keluarga)
    return sorted(nama)

POLA_LOKASI = re.compile(r"\[[^\]]*@[A-Za-z][\w:.-]*\s*,\s*[^\];]+[^\]]*\]|(?<![\w@])@(?!fig-|tbl-|eq-|sec-)[A-Za-z][\w:.-]*\s\[[^\]@]+\]")


def gerbang_sitasi(qmd, buku=None):
    prosa, _ = pilah_qmd(qmd.read_text(encoding="utf-8"))
    PENULIS = daftar_penulis(buku or qmd.parent)
    temuan = []
    for nomor, b in prosa:
        bersih = re.sub(r"`[^`]*`", " ", b)
        for m in POLA_LOKASI.finditer(bersih):
            temuan.append(f"baris {nomor}: sitasi memuat lokasi '{m.group(0)[:60]}'; tulis penulis–tahun saja "
                          f"dan simpan lokasi di klaim.json")
        for kal in re.split(r"(?<=[.!?])\s+(?=[A-Z])", bersih):
            kurung = re.findall(r"\[[^\]]*@[A-Za-z][^\]]*\]", kal)
            if not kurung:
                continue
            tanpa_kurung = re.sub(r"\[[^\]]*\]", " ", kal)
            for nama in PENULIS:
                if re.search(r"(?<![@\w])" + nama + r"\b", tanpa_kurung):
                    temuan.append(f"baris {nomor}: '{nama}' disebut di kalimat bersitasi kurung; "
                                  f"pakai sitasi naratif @kunci (mis. '@gelman2013 menyebut'): {kal.strip()[:80]}")
    catat("G-SITASI", not temuan, "\n".join(temuan))

# ---------------------------------------------------------------- G-KODE (rajut)
def gerbang_kode(buku, bab):
    build = buku / "build"
    build.mkdir(exist_ok=True)
    keluar = build / f"{bab}.knit.md"
    r = (f'knitr::opts_chunk$set(error = FALSE, fig.path = "build/fig-{bab}/"); '
         f'knitr::knit("{bab}.qmd", output = "build/{bab}.knit.md", quiet = TRUE, envir = new.env())')
    kode, log = jalankan(["Rscript", "-e", r], cwd=buku)
    ok = kode == 0 and keluar.exists()
    catat("G-KODE", ok, log[-3000:] if not ok else "")
    return keluar if ok else None


# ---------------------------------------------------------------- G-LAMPIRAN
def ekstrak_python(qmd, bab):
    _, chunk = pilah_qmd(qmd.read_text(encoding="utf-8"))
    bagian = [
        f'"""Kode gambar {bab} (Python: matplotlib dan seaborn).',
        "",
        f"Jalankan setelah {bab}.R: skrip R menulis data ke data-gambar/,",
        'skrip ini hanya membaca data itu dan menggambar."""',
        "",
    ]
    for bahasa, isi, awal in chunk:
        if bahasa != "python":
            continue
        baris = [b for b in isi.splitlines() if not b.lstrip().startswith("#|")]
        label = re.search(r"#\|\s*label:\s*(\S+)", isi)
        bagian.append(f"# ---- {label.group(1) if label else 'chunk-' + str(awal)} ----")
        bagian.extend(baris)
        bagian.append("")
    return "\n".join(bagian) if len(bagian) > 5 else None


def gerbang_lampiran(buku, bab, folder_lampiran):
    folder_lampiran.mkdir(parents=True, exist_ok=True)
    qmd = buku / f"{bab}.qmd"
    keluar_r = folder_lampiran / f"{bab}.R"
    r = f'knitr::purl("{qmd}", output = "{keluar_r}", documentation = 1, quiet = TRUE)'
    kode, log = jalankan(["Rscript", "-e", r], cwd=buku)
    if kode != 0:
        catat("G-LAMPIRAN", False, "purl gagal:\n" + log[-2000:])
        return
    # purl menyalin chunk Python sebagai komentar; buang agar skrip R murni
    isi = keluar_r.read_text(encoding="utf-8")
    kepala = (f"# Kode R {bab} — {buku.name}\n"
              f"# Diekstrak otomatis dari {bab}.qmd dan diuji berjalan mandiri oleh harness.\n"
              f"# Jalankan dari folder ini: Rscript {bab}.R\n\n")
    keluar_r.write_text(kepala + isi, encoding="utf-8")
    py = ekstrak_python(qmd, bab)
    shutil.copy(BERSAMA / "gaya_gambar.py", folder_lampiran / "gaya_gambar.py")
    kode, log = jalankan(["Rscript", f"{bab}.R"], cwd=folder_lampiran)
    pesan = []
    if kode != 0:
        pesan.append(f"{bab}.R gagal dijalankan mandiri:\n{log[-2500:]}")
    if py:
        (folder_lampiran / f"{bab}_gambar.py").write_text(py, encoding="utf-8")
        kode2, log2 = jalankan(["python3", f"{bab}_gambar.py"], cwd=folder_lampiran)
        if kode2 != 0:
            pesan.append(f"{bab}_gambar.py gagal dijalankan mandiri:\n{log2[-2500:]}")
    # Gambar TikZ: setiap chunk tikz menjadi berkas .tex mandiri yang harus terkompilasi
    _, chunk = pilah_qmd(qmd.read_text(encoding="utf-8"))
    berkas_pre = BERSAMA / "tikz-preamble.tex"
    pre = berkas_pre.read_text(encoding="utf-8") if berkas_pre.exists() else ""
    for bahasa, isi, awal in chunk:
        if bahasa != "tikz":
            continue
        label = re.search(r"%\|\s*label:\s*(\S+)", isi)
        nama = f"{bab}_{label.group(1) if label else 'tikz-' + str(awal)}"
        tubuh = "\n".join(b for b in isi.splitlines() if not b.lstrip().startswith("%|"))
        tex = ("% Gambar TikZ " + nama + " — diekstrak otomatis dari " + bab + ".qmd\n"
               "% Kompilasi: pdflatex " + nama + ".tex\n"
               "\\documentclass[border=4pt]{standalone}\n\\usepackage{tikz}\n" + pre +
               "\\begin{document}\n" + tubuh + "\n\\end{document}\n")
        (folder_lampiran / f"{nama}.tex").write_text(tex, encoding="utf-8")
        kode3, log3 = jalankan(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                                f"{nama}.tex"], cwd=folder_lampiran, batas=300)
        for ext in [".aux", ".log"]:
            (folder_lampiran / f"{nama}{ext}").unlink(missing_ok=True)
        if kode3 != 0:
            pesan.append(f"{nama}.tex gagal dikompilasi:\n{log3[-1500:]}")
    catat("G-LAMPIRAN", not pesan, "\n".join(pesan))


# ---------------------------------------------------------------- prosa dari hasil rajut
def prosa_dari_rajutan(md, bab):
    """Buat dua berkas: prosa untuk EYD (judul dan butir ikut) dan prosa untuk gaya
    (hanya paragraf isi). Angka sudah berupa hasil hitung karena diambil dari hasil rajut."""
    teks = md.read_text(encoding="utf-8")
    teks = re.sub(r"^---\n.*?\n---\n", "", teks, flags=re.S)
    teks = re.sub(r"```.*?```", "\n", teks, flags=re.S)          # kode dan keluaran
    teks = re.sub(r"\$\$.*?\$\$", "\n", teks, flags=re.S)        # rumus tampilan
    teks = re.sub(r"<!--.*?-->", " ", teks, flags=re.S)
    teks = re.sub(r"\\begin\{.*?\\end\{[^}]*\}", "\n", teks, flags=re.S)
    nomor = {"fig": "Gambar 2", "tbl": "Tabel 2", "eq": "persamaan (2)", "sec": "Subbab 2",
             "Fig": "Gambar 2", "Tbl": "Tabel 2", "Eq": "Persamaan (2)", "Sec": "Subbab 2"}
    teks = re.sub(r"@(fig|tbl|eq|sec|Fig|Tbl|Eq|Sec)-[\w-]+", lambda m: nomor[m.group(1)], teks)
    teks = re.sub(r"\[@[^\]]*\]", "(Penulis, 2020)", teks)
    teks = re.sub(r"\{#[^}]*\}", "", teks)
    teks = re.sub(r"\{\.[^}]*\}", "", teks)
    eyd, gaya = [], []
    for blok in re.split(r"\n\s*\n", teks):
        baris = [b for b in blok.strip().splitlines() if b.strip()]
        if not baris:
            continue
        baris = [b for b in baris if not b.strip().startswith(":::")]
        if not baris:
            continue
        isi = "\n".join(baris)
        gambar = re.match(r"!\[(.*?)\]\(.*?\)", isi.strip(), flags=re.S)
        if gambar:
            eyd.append(gambar.group(1).strip().rstrip(".") + ".")
            continue
        if re.search(r"<(div|img|p|span)\b", isi):  # gambar yang dikeluarkan knitr sebagai HTML
            alt = re.findall(r'alt="([^"]*)"', isi)
            eyd.extend(a.strip().rstrip(".") + "." for a in alt if a.strip())
            continue
        if isi.lstrip().startswith("|") or re.match(r"^\s*[-:| ]+$", isi):
            continue  # tabel pipa
        eyd.append(isi)
        awal = isi.lstrip()
        if awal.startswith("#") or re.match(r"^([-*+]|\d+\.)\s", awal) or awal.startswith(">"):
            continue
        gaya.append(" ".join(b.strip() for b in baris))
    berkas_eyd = md.parent / f"{bab}.prosa-eyd.md"
    berkas_gaya = md.parent / f"{bab}.prosa-gaya.md"
    berkas_eyd.write_text("\n\n".join(eyd) + "\n", encoding="utf-8")
    berkas_gaya.write_text("\n\n".join(gaya) + "\n", encoding="utf-8")
    return berkas_eyd, berkas_gaya


# ---------------------------------------------------------------- G-EYD
def gerbang_eyd(berkas, peng):
    kode, log = jalankan(["python3", str(SKILL_EYD), str(berkas), "--json"], cwd=berkas.parent)
    try:
        data = json.loads(log[log.index("{"):])
    except ValueError:
        catat("G-EYD", False, "keluaran pemeriksa tidak terbaca:\n" + log[-1500:])
        return []
    abaikan = peng.get("eyd-abaikan", [])

    def diabaikan(t):
        for a in abaikan:
            if a["temuan"].lower() == str(t["temuan"]).lower() and \
               a.get("kategori", t["kategori"]) == t["kategori"]:
                return True
        return False

    error = [t for t in data["temuan"] if t["tingkat"] == "ERROR" and not diabaikan(t)]
    warning = [t for t in data["temuan"] if t["tingkat"] == "WARNING" and not diabaikan(t)]
    rinci = "\n".join(f"{t['kategori']}: '{t['temuan']}' → {t['saran']}" for t in error)
    catat("G-EYD", not error, rinci)
    return warning


# ---------------------------------------------------------------- G-GAYA dan G-PARAGRAF
SINGKATAN = ["dkk.", "dll.", "dsb.", "dst.", "hlm.", "s.d.", "No.", "Prof.", "Dr.", "et al.", "misal.", "Jl."]


def kalimat(paragraf):
    t = paragraf
    for s in SINGKATAN:
        t = t.replace(s, s.replace(".", "§"))
    t = re.sub(r"\$[^$]*\$", "RUMUS", t)
    potongan = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"(*“])", t.strip())
    return [p for p in potongan if p.strip()]


GAYA_CADANGAN = [
    (r"\bdi mana\b(?!\s*\?)", "G-DIMANA: 'di mana' sebagai penghubung; pakai 'yang', 'tempat', atau pecah kalimat"),
    (r"\bdimana\b|\byang mana\b", "G-DIMANA: penghubung tidak baku"),
    (r"(?<!,) sedangkan\b", "G-KOMA: koma sebelum 'sedangkan'"),
    (r"(?<!,) tetapi\b", "G-KOMA: koma sebelum 'tetapi'"),
    (r"(?<!,) melainkan\b", "G-KOMA: koma sebelum 'melainkan'"),
    (r"^(?:Oleh karena itu|Dengan demikian|Akibatnya|Namun|Jadi|Selain itu)\s(?!,)", "G-KOMA: koma setelah ungkapan penghubung antarkalimat"),
]


def gaya_cadangan(berkas):
    """Pemeriksa gaya cadangan bila skrip skill math-article tidak terpasang:
    larangan 'di mana' sebagai penghubung dan koma pada konjungsi baku."""
    keluar = []
    for k, par in enumerate(berkas.read_text(encoding="utf-8").split("\n\n"), start=1):
        for kal in kalimat(par):
            for pola, pesan in GAYA_CADANGAN:
                if pesan and re.search(pola, kal.strip(), flags=re.M):
                    keluar.append(f"- {pesan} — P{k}: {kal.strip()[:80]}")
    return "\n".join(keluar)


def gerbang_gaya(berkas, peng):
    if SKILL_GAYA.exists():
        kode, log = jalankan(["python3", str(SKILL_GAYA), "--file", str(berkas), "--lang", "id"],
                             cwd=berkas.parent)
    else:
        print("    G-GAYA: skrip math-article tidak ditemukan; memakai pemeriksa cadangan")
        log = gaya_cadangan(berkas)
    abaikan = [a["pola"] for a in peng.get("gaya-abaikan", [])]
    gagal = []
    for b in log.splitlines():
        b = b.strip()
        if not b.startswith("- "):
            continue
        if b.startswith("- G-RHYTHM"):  # aturan ritme artikel diganti G-PARAGRAF (longgar)
            continue
        if any(re.search(p, b) for p in abaikan):
            continue
        gagal.append(b[2:])
    catat("G-GAYA", not gagal, "\n".join(gagal))
    # G-PARAGRAF
    salah = []
    for k, par in enumerate(berkas.read_text(encoding="utf-8").split("\n\n"), start=1):
        par = par.strip()
        if not par:
            continue
        jumlah = len(kalimat(par))
        if jumlah < 2 and not par.endswith(":"):
            salah.append(f"P{k}: {jumlah} kalimat (minimal 2, kecuali pengantar yang diakhiri titik dua): {par[:90]}…")
        if jumlah > 6:
            salah.append(f"P{k}: {jumlah} kalimat (maksimal 6): {par[:90]}…")
    catat("G-PARAGRAF", not salah, "\n".join(salah))


# ---------------------------------------------------------------- G-SLOP (bahasa Indonesia)
# Disarikan dari references/stop-slop-id/frasa.md dan references/humanizer-id/frasa.md
# (skill math-article). Ditambahkan karena harness_check.py tidak menangkapnya.
SLOP_ID = [
    (r"\bberikut (?:adalah|ini)\b", "pembuka berbasa-basi; langsung nyatakan isinya"),
    (r"\binilah\b", "pembuka berbasa-basi"),
    (r"\bperlu (?:dicatat|diketahui|ditegaskan) bahwa\b", "frasa pengisi; hapus"),
    (r"\bpenting untuk dicatat\b", "frasa pengisi; hapus"),
    (r"\bpada (?:dasarnya|intinya|hakikatnya|akhirnya)\b", "frasa pengisi; hapus"),
    (r"\bsecara (?:keseluruhan|harfiah|fundamental|inheren|mendasar|efektif)\b", "penguat kosong"),
    (r"\bsangat\b|\bamat\b|\bbenar-benar\b|\bsungguh\b|\bbetul-betul\b", "penguat kosong; ganti dengan ukuran atau hapus"),
    (r"\bsejatinya\b|\bmenariknya\b|\bpentingnya,|\byang terpenting,", "penguat kosong"),
    (r"\bkrusial\b|\bpivotal\b", "kosakata khas AI; sebutkan mengapa penting"),
    (r"\bkomprehensif\b|\bholistik\b", "kata keren; sebutkan cakupannya"),
    (r"\bmemainkan peran (?:penting|kunci)\b|\bmenjadi kunci\b", "sebutkan apa yang dilakukannya"),
    (r"\bdi era\b|\bdi zaman sekarang\b", "frasa pengisi"),
    (r"\b(?:tak|tidak) dapat (?:dipungkiri|disangkal)\b", "frasa pengisi"),
    (r"\bseperti yang (?:kita ketahui|akan kita lihat)\b", "komentar meta"),
    (r"\bmari kita\b|\bmari saya\b", "komentar meta; langsung kerjakan"),
    (r"\bpada (?:bagian|bab) ini,? (?:kita|kami) akan\b", "komentar meta"),
    (r"\bfaktanya,|\bkenyataannya adalah\b|\bternyata\b", "frasa pengisi"),
    (r"\bkesimpulannya,|\bsebagai penutup,|\bakhir kata,|\bsemoga bermanfaat\b", "penutup otomatis"),
    (r"\bmenyoroti\b|\bmenggarisbawahi\b|\bmenyelami\b|\bmengupas tuntas\b|\bmembedah\b", "kosakata khas AI"),
    (r"\blanskap\b|\bpermadani\b|\bmozaik\b|\bsinergi\b|\bmenavigasi\b", "kosakata khas AI"),
    (r"\bmemberdayakan\b|\bmengakselerasi\b|\bmentransformasi\b|\byang pada gilirannya\b", "kosakata khas AI"),
    (r"\bselaras dengan\b|\bsejalan dengan\b", "ganti: cocok dengan, mengikuti"),
    (r"\bimplikasinya signifikan\b|\bdampaknya nyata\b|\btantangannya kompleks\b", "pernyataan kabur"),
]


def gerbang_slop(berkas, peng):
    abaikan = [a["pola"] for a in peng.get("gaya-abaikan", [])]
    temuan = []
    for k, par in enumerate(berkas.read_text(encoding="utf-8").split("\n\n"), start=1):
        for pola, saran in SLOP_ID:
            for m in re.finditer(pola, par, flags=re.I):
                pesan = f"P{k}: '{m.group(0)}' — {saran}"
                if not any(re.search(p, pesan) for p in abaikan):
                    temuan.append(pesan)
    catat("G-SLOP", not temuan, "\n".join(temuan))


# ---------------------------------------------------------------- G-RENDER
def gerbang_render(buku):
    # Kedua format dirender dalam satu proses; render terpisah membuat Quarto
    # membersihkan folder keluaran sehingga berkas format pertama hilang.
    pesan = []
    kode, log = jalankan(["quarto", "render"], cwd=buku, batas=5400)
    (buku / "build" / "render.log").write_text(log, encoding="utf-8")
    if kode != 0:
        galat = [b for b in log.splitlines() if re.search(r"ERROR|^!|Error", b)]
        pesan.append("render gagal:\n" + "\n".join(galat[:20]) + "\n" + log[-1500:])
    for ext in ["pdf", "docx"]:
        if not list((buku / "_book").glob(f"*.{ext}")):
            pesan.append(f"berkas .{ext} tidak ditemukan di _book/")
    peringatan = [b for b in log.splitlines()
                  if re.search(r"WARN.*(cross|unable to resolve|not found|citation)", b, re.I)]
    if peringatan:
        pesan.append("render memberi peringatan rujukan:\n" + "\n".join(peringatan[:20]))
    catat("G-RENDER", not pesan, "\n".join(pesan))
    gerbang_log(buku)
    if os.environ.get("TAG", "1") == "1":
        gerbang_tag(buku)
    if os.environ.get("TEPI", "1") == "1":
        gerbang_tepi(buku)


# ---------------------------------------------------------------- G-LOG
# Telaah pakar seri Bayesian (2026-11-07): Quarto hanya mengulang LuaLaTeX bila
# log memuat "Rerun to get", "Please (re)run", atau "Rerun LaTeX", tidak untuk
# "Rerun to correct this" dari hook lastpage, sehingga daftar isi tertinggal satu
# putaran (Indeks hilang, nomor halaman salah). Obatnya latex-min-runs: 4 di
# _quarto.yml; label ganda dari kepala longtable diobati \endhead di preamble.tex.
POLA_LOG_TIDAK_STABIL = [
    (r"Rerun to correct", "LaTeX meminta kompilasi ulang (hook lastpage); daftar isi/nomor halaman belum stabil"),
    (r"Label\(s\) may have changed", "label berubah; rujukan silang dan daftar isi belum stabil"),
    (r"Rerun to get (?:cross-references|outlines) right", "LaTeX meminta kompilasi ulang"),
    (r"Label `[^']+' multiply defined", "label terdefinisi ganda"),
]


def masalah_log_latex(teks):
    """Daftar masalah kestabilan dari isi log LaTeX akhir."""
    masalah = []
    for pola, arti in POLA_LOG_TIDAK_STABIL:
        temuan = sorted(set(m.group(0) for m in re.finditer(pola, teks)))
        if temuan:
            masalah.append(f"{arti}: " + "; ".join(temuan[:8]))
    return masalah


def log_latex_utama(buku):
    """Log kompilasi buku (bukan log tikz), yang terakhir ditulis."""
    logs = sorted((p for p in buku.glob("*.log") if not p.name.startswith("tikz")),
                  key=lambda p: p.stat().st_mtime)
    return logs[-1] if logs else None


def gerbang_log(buku):
    """Log LaTeX putaran terakhir tidak boleh meminta kompilasi ulang dan tidak
    boleh memuat label ganda (perlu latex-clean: false dan latex-min-runs: 4)."""
    log = log_latex_utama(buku)
    if log is None:
        catat("G-LOG", False, "log LaTeX tidak ditemukan; set format.pdf.latex-clean: false di _quarto.yml")
        return
    masalah = masalah_log_latex(log.read_text(encoding="utf-8", errors="replace"))
    catat("G-LOG", not masalah, "\n".join(f"{log.name}: {m}" for m in masalah))


def gerbang_tag(buku, pdf=None):
    """PDF bertag (LuaLaTeX + \\DocumentMetadata di _bersama/doc-class.tex):
    pdfinfo melaporkan Tagged: yes, pohon struktur berakar Document dengan
    H1, P, dan Figure, serta /Lang id-ID (bila pikepdf terpasang)."""
    if pdf is None:
        daftar = list((buku / "_book").glob("*.pdf"))
        if not daftar:
            catat("G-TAG", False, "PDF tidak ditemukan di _book/")
            return
        pdf = daftar[0]
    if not shutil.which("pdfinfo"):
        catat("G-TAG", False, "pdfinfo (poppler-utils) tidak terpasang")
        return
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True,
                          errors="replace").stdout
    pesan = []
    if not re.search(r"^Tagged:\s+yes", info, re.M):
        pesan.append("pdfinfo: PDF tidak bertag (Tagged: no); periksa pdf-engine: lualatex "
                     "dan template-partials doc-class.tex di _quarto.yml")
    # Tagged: yes dari poppler berarti /MarkInfo /Marked true; pohon struktur
    # (/StructTreeRoot) dibaca dengan pdfinfo -struct.
    struktur = subprocess.run(["pdfinfo", "-struct", str(pdf)], capture_output=True,
                              text=True, errors="replace").stdout
    if not struktur.lstrip().startswith("Document"):
        pesan.append("pohon struktur (/StructTreeRoot) kosong atau tidak berakar Document")
    for tag in ("H1", "P", "Figure"):
        if not re.search(rf"^\s*{tag} ", struktur, re.M):
            pesan.append(f"tag {tag} tidak ditemukan di pohon struktur")
    try:
        import pikepdf
        with pikepdf.open(pdf) as dok:
            if str(dok.Root.get("/Lang", "")) != "id-ID":
                pesan.append("bahasa dokumen /Lang bukan id-ID")
    except ImportError:
        lang = re.search(r"/Lang\s*\(([^)]*)\)", Path(pdf).read_bytes()[:400000].decode("latin-1"))
        if lang and lang.group(1) != "id-ID":
            pesan.append(f"bahasa dokumen /Lang {lang.group(1)}, bukan id-ID")
    catat("G-TAG", not pesan, "\n".join(pesan))


BATAS_TEPI_PT = 3.0


def gerbang_tepi(buku):
    """Tidak ada rumus, gambar, tabel, kode, atau teks yang melewati tepi
    halaman lebih dari 3 pt (Overfull hbox di log LaTeX; perlu latex-clean: false)."""
    logs = sorted(buku.glob("*.log"), key=lambda p: p.stat().st_mtime)
    logs = [p for p in logs if not p.name.startswith("tikz")]
    if not logs:
        catat("G-TEPI", False, "log LaTeX tidak ditemukan; set format.pdf.latex-clean: false di _quarto.yml")
        return
    log = logs[-1].read_text(encoding="utf-8", errors="replace")
    tex_p = logs[-1].with_suffix(".tex")
    if not tex_p.exists():  # Quarto menamai log menurut berkas pertama (index.log)
        kandidat = [t for t in buku.glob("*.tex") if not t.name.startswith("preamble")]
        tex_p = kandidat[0] if kandidat else tex_p
    tex = tex_p.read_text(encoding="utf-8").split("\n") if tex_p.exists() else []
    bab = [(i, re.match(r"\\chapter\*?\{([^}]*)", l).group(1)[:40])
           for i, l in enumerate(tex, 1) if re.match(r"\\chapter\*?\{", l)]
    masalah = []
    for m in re.finditer(r"Overfull \\hbox \(([\d.]+)pt too wide\) (?:in paragraph at lines (\d+)--\d+"
                         r"|detected at line (\d+)|in alignment at lines (\d+)--\d+)", log):
        lebar = float(m.group(1))
        if lebar <= BATAS_TEPI_PT:
            continue
        ln = int(m.group(2) or m.group(3) or m.group(4))
        nama = [t for i, t in bab if i <= ln]
        isi = tex[ln - 1].strip()[:70] if ln <= len(tex) else ""
        masalah.append(f"{lebar:.1f} pt melewati tepi | bab '{nama[-1] if nama else '-'}' | tex {ln}: {isi}")
    catat("G-TEPI", not masalah, "\n".join(masalah[:60]))


# ---------------------------------------------------------------- G-REFERENSI
def gerbang_referensi(qmd, bab, buku):
    """Setiap sitasi punya klaim terverifikasi; kutipan bukti dicocokkan ulang
    dengan sumbernya (lihat harness/referensi.py)."""
    sys.path.insert(0, str(AKAR / "harness"))
    import referensi
    prosa, _ = pilah_qmd(qmd.read_text(encoding="utf-8"))
    bib = (buku / "pustaka.bib").read_text(encoding="utf-8") if (buku / "pustaka.bib").exists() else ""
    masalah, ringkas = referensi.periksa(qmd, bab, prosa, bib)
    for r in ringkas[:1]:
        print("    G-REFERENSI: " + r)
    catat("G-REFERENSI", not masalah, "\n".join(masalah))
    return ringkas


# ---------------------------------------------------------------- G-PENGGALAN
def gerbang_penggalan(buku, sesudah_render):
    """Pemenggalan kata EYD V: daftar pengecualian diperbarui, pemenggal lulus
    uji contoh resmi EYD V, dan (setelah render) setiap kata yang terpenggal di
    akhir baris PDF dipenggal pada titik yang sah menurut EYD V."""
    sys.path.insert(0, str(AKAR / "harness"))
    import penggalan
    pesan = []
    if "harness" not in buku.relative_to(AKAR).parts:  # fikstur uji tidak menimpa daftar buku
        penggalan.tulis(buku)
    pesan += penggalan.uji() + penggalan.uji_tex()
    if sesudah_render:
        tex = list(buku.glob("*.tex"))
        isi = tex[0].read_text(encoding="utf-8") if tex else ""
        if "indonesian" not in isi or "penggalan-id.tex" not in isi:
            pesan.append("berkas .tex tidak memuat babel indonesian atau penggalan-id.tex")
        berkas_asing = BERSAMA / "istilah-asing.txt"
        asing = [b for b in berkas_asing.read_text(encoding="utf-8").splitlines()
                 if b and not b.startswith("#")] if berkas_asing.exists() else []
        if asing and "english" not in isi:
            pesan.append("istilah asing tidak ditandai bahasa Inggris di .tex")
        pdf = list((buku / "_book").glob("*.pdf"))
        if pdf:
            teks = subprocess.run(["pdftotext", "-raw", str(pdf[0]), "-"], capture_output=True,
                                  text=True).stdout
            baris = teks.splitlines()
            diperiksa = 0
            berkas_nama = BERSAMA / "nama-diri.txt"
            nama = {w.lower() for w in berkas_nama.read_text(encoding="utf-8").split()} \
                if berkas_nama.exists() else set()
            for b, lanjut in zip(baris, baris[1:]):
                m = re.search(r"([A-Za-zÀ-ž]+)-$", b.rstrip())
                n = re.match(r"\s*([a-zà-ž]+)", lanjut)
                if m and n and n.group(1) not in ("nya", "lah", "kah", "pun") \
                        and (m.group(1) + n.group(1)).lower() in nama:  # "X-nya" = tanda hubung tertulis
                    pesan.append(f"PDF: nama '{m.group(1)}-{n.group(1)}' terpenggal di akhir baris "
                                 f"(nama tidak boleh dipenggal)")
            for b, lanjut in zip(baris, baris[1:]):
                m = re.search(r"([A-Za-z]+)-$", b.rstrip())
                n = re.match(r"\s*([a-z]+)", lanjut)
                if not m or not n:
                    continue
                kata = m.group(1) + n.group(1)
                p = penggalan.penggal(kata)
                if p is None:
                    continue  # bukan kata Indonesia yang dikenal (istilah asing, nama)
                diperiksa += 1
                if len(m.group(1)) not in penggalan.titik(p):
                    pesan.append(f"PDF: '{m.group(1)}-{n.group(1)}' tidak sesuai EYD V ({p})")
            print(f"    G-PENGGALAN: {diperiksa} kata terpenggal di akhir baris PDF diaudit")
        docx = list((buku / "_book").glob("*.docx"))
        if docx:
            import zipfile
            z = zipfile.ZipFile(docx[0])
            if "autoHyphenation" not in z.read("word/settings.xml").decode():
                pesan.append("Word: pemenggalan otomatis tidak aktif")
            if 'w:val="id-ID"' not in z.read("word/styles.xml").decode():  # tag lengkap untuk Word
                pesan.append("Word: bahasa dokumen bukan id-ID")
    catat("G-PENGGALAN", not pesan, "\n".join(pesan))


# ---------------------------------------------------------------- G-JUDUL
# Keputusan penulis 2026-11-06: judul tabel pendek (satu frasa, <= 12 kata);
# penjelasan masuk ke blok ::: {.catatan}. Gambar berpanel banyak memakai
# label (a), (b), ... (gaya_gambar.label_panel) dan keterangannya menyebut
# isi setiap huruf; rujukan di prosa memakai @fig-x(a), bukan "kiri/kanan".
MAKS_KATA_JUDUL_TABEL = 12
POLA_ARAH = re.compile(r"\b(?:Kiri|Kanan|Atas|Bawah|Tengah)\s*:|\bpanel\s+(?:kiri|kanan|atas|bawah|tengah)\b",
                       re.I)


def _teks_judul(nilai):
    nilai = nilai.strip()
    if nilai.startswith("!expr"):
        lit = re.findall(r'"((?:[^"\\]|\\.)*)"', nilai[5:])
        nilai = " N ".join(lit) if lit else "N"
    nilai = nilai.strip().strip('"').strip("'")
    nilai = re.sub(r"\$[^$]*\$", "X", nilai)
    nilai = re.sub(r"`[^`]*`", "X", nilai)
    return re.sub(r"[*_]", "", nilai)


def _multipanel(isi):
    m = re.search(r"subplots\(([^)]*)\)", isi)
    if m:
        arg = m.group(1)
        pos = re.findall(r"^\s*(\d+)\s*,\s*(\d+)", arg)
        if pos and int(pos[0][0]) * int(pos[0][1]) > 1:
            return True
        kw = dict(re.findall(r"(nrows|ncols)\s*=\s*(\d+)", arg))
        if int(kw.get("nrows", 1)) * int(kw.get("ncols", 1)) > 1:
            return True
        if re.match(r"^\s*(\d+)\s*(?:,|$)", arg) and int(re.match(r"^\s*(\d+)", arg).group(1)) > 1:
            return True
    return bool(re.search(r"subplot_mosaic|GridSpec|add_subplot\([^)]*\)[\s\S]*add_subplot\(", isi))


MAKS_KATA_JUDUL_GAMBAR = 12
MAKS_KATA_PANEL = 6


def _cek_judul_gambar(teks):
    """Keputusan penulis 2026-11-06: judul gambar singkat; penjelasan ke
    ::: {.catatan}. Judul utama (sebelum '(a)') <= 12 kata, satu frasa;
    frasa tiap panel <= 6 kata."""
    masalah = []
    judul = [(m.group(1), teks[:m.start()].count("\n") + 1)
             for m in re.finditer(r"[#%]\|\s*fig-cap:\s*(.+)$", teks, flags=re.M)]
    judul += [(m.group(1), teks[:m.start()].count("\n") + 1)
              for m in re.finditer(r"!\[([^\]]+)\]\([^)]*\)\{[^}]*#fig-", teks)]
    for nilai, baris in judul:
        t = _teks_judul(nilai).strip()
        bagian = re.split(r"\(([a-h])\)", t)
        utama = bagian[0].strip().rstrip(":;,. ")
        n = len(utama.split())
        if n > MAKS_KATA_JUDUL_GAMBAR:
            masalah.append(f"baris {baris}: judul gambar {n} kata (maks. {MAKS_KATA_JUDUL_GAMBAR}); "
                           f"pindahkan penjelasan ke ::: {{.catatan}}: '{t[:60]}…'")
        if re.search(r"[.!?;]\s+\S", t.rstrip(".")) or re.search(r":\s+\S", utama):
            masalah.append(f"baris {baris}: judul gambar lebih dari satu kalimat/klausa; "
                           f"sisanya ke ::: {{.catatan}}: '{t[:60]}…'")
        for huruf, isi in zip(bagian[1::2], bagian[2::2]):
            k = len(isi.strip(" ,;.:").replace(" dan ", " ").split())
            if k > MAKS_KATA_PANEL:
                masalah.append(f"baris {baris}: frasa panel ({huruf}) {k} kata (maks. {MAKS_KATA_PANEL}); "
                               f"rincian ke ::: {{.catatan}}")
    return masalah


_KATA_KERJA_ATRIBUSI = (r"(?:menyebut|menyatakan|mencatat|menjelaskan|menganjurkan|menyarankan|memberi|mendefinisikan"
                        r"|menggambarkan|menulis|merekomendasikan|mengingatkan|menegaskan|memperingatkan|mengaitkan"
                        r"|menunjukkan|menyediakan|memakai|membahas|melaporkan|mengatakan|menetapkan|memuat"
                        r"|merangkum|menamai|mencontohkan|menekankan|menguraikan|menggunakan)")
POLA_ATRIBUSI_MANUAL = re.compile(
    r"\b(?:Menurut|Dalam|Di)\s+(?:[Pp]anduan|[Mm]anual|Referensi Fungsi|[Dd]okumentasi|[Hh]alaman bantuan|[Gg]losarium"
    r"|[Vv]ignette|[Ss]itus|[Ll]aman|[Pp]ublikasi|[Rr]ilis|Berita Resmi Statistik|BRS|BPS|Badan Pusat Statistik"
    r"|Stan Development Team|R Core Team|tim pengembang)\b"
    r"|\b(?:Panduan(?: Pengguna)?(?: Stan| CmdStan)?|Manual (?:Referensi|Rujukan)(?: Stan)?|Rujukan Fungsi(?: Stan)?|Panduan Pengguna(?: Stan)?|Referensi Fungsi(?: Stan)?"
    r"|[Dd]okumentasi(?: paket)? [\w.]+|[Hh]alaman bantuan `?[?\w:.]+`?|[Gg]losarium [\w.]+|[Vv]ignette [\w.]+"
    r"|BPS|Badan Pusat Statistik|Berita Resmi Statistik|Stan Development Team|R Core Team|[Tt]im pengembang \w+)"
    r"(?:\s+\(\d{4}\w?\))?(?:\s+(?:yang sama|itu|ini|juga|pun|sendiri))*\s+" + _KATA_KERJA_ATRIBUSI + r"\b")


def _kunci_korporat(buku):
    """Kunci bib yang penulisnya lembaga (author = {{...}})."""
    bib = (buku / "pustaka.bib").read_text(encoding="utf-8") if (buku / "pustaka.bib").exists() else ""
    hasil = set()
    for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", bib, flags=re.S):
        a = re.search(r"\bauthor\s*=\s*\{(.*)\}\s*,?\s*$", m.group(2), flags=re.M)
        if not a:
            if not re.search(r"\beditor\s*=", m.group(2)):
                hasil.add(m.group(1))
            continue
        nilai = a.group(1).strip()
        if nilai.startswith("{") and " and " not in nilai and "," not in nilai:
            hasil.add(m.group(1))
    return hasil


def cek_atribusi_manual(qmd, buku=None):
    """Keputusan penulis 2026-11-06: hanya penulis (orang) yang boleh menjadi
    subjek pernyataan ('Gelman dkk. (2026) menyatakan'). Manual, panduan,
    dokumentasi, lembaga, rilis: tulis faktanya langsung dengan sitasi [@kunci]."""
    prosa, _ = pilah_qmd(qmd.read_text(encoding="utf-8"))
    korporat = _kunci_korporat(buku or qmd.parent)
    masalah = []
    for nomor, b in prosa:
        bersih = re.sub(r"`[^`]*`", lambda m: m.group(0) if "?" in m.group(0) else "X", b)
        for m in POLA_ATRIBUSI_MANUAL.finditer(bersih):
            masalah.append(f"baris {nomor}: '{m.group(0)}' — tulis faktanya langsung dengan sitasi "
                           f"[@kunci]; hanya penulis orang yang boleh menjadi subjek")
        tanpa_kurung = re.sub(r"\[[^\]]*\]", " ", bersih)
        for m in re.finditer(r"(?<![\w@])@([\w:.-]+)", tanpa_kurung):
            k = m.group(1).rstrip(".:")
            if k in korporat:
                masalah.append(f"baris {nomor}: sitasi naratif @{k} (penulis lembaga/tanpa penulis); "
                               f"tulis faktanya langsung dengan sitasi [@{k}]")
    return masalah


def cek_persamaan(qmd):
    """Keputusan penulis 2026-11-07: kata 'persamaan' huruf kecil di tengah
    kalimat; rujukan @eq- di awal kalimat ditulis @Eq- agar berkapital."""
    prosa, _ = pilah_qmd(qmd.read_text(encoding="utf-8"))
    masalah = []
    for nomor, b in prosa:
        bersih = re.sub(r"`[^`]*`", "X", b)
        for m in re.finditer(r"(?:[^.!?\s#>*-]|\d)\s+(Persamaan)\b", bersih):
            masalah.append(f"baris {nomor}: 'Persamaan' di tengah kalimat; tulis 'persamaan'")
        for m in re.finditer(r"(?:^|[.!?]\s+)@eq-", bersih):
            masalah.append(f"baris {nomor}: @eq- di awal kalimat; tulis @Eq- agar berkapital")
    return masalah


def gerbang_judul(qmd, md):
    teks = qmd.read_text(encoding="utf-8")
    prosa, chunk = pilah_qmd(teks)
    masalah = _cek_judul_gambar(teks) if os.environ.get("JUDUL_GAMBAR", "1") == "1" else []
    judul = [(m.group(1), teks[:m.start()].count("\n") + 1)
             for m in re.finditer(r"[#%]\|\s*tbl-cap:\s*(.+)$", teks, flags=re.M)]
    judul += [(m.group(1), teks[:m.start()].count("\n") + 1)
              for m in re.finditer(r"^:\s+(.+?)\s*\{#tbl-", teks, flags=re.M)]
    for nilai, baris in judul:
        t = _teks_judul(nilai)
        n = len(t.split())
        if n > MAKS_KATA_JUDUL_TABEL:
            masalah.append(f"baris {baris}: judul tabel {n} kata (maks. {MAKS_KATA_JUDUL_TABEL}); "
                           f"pindahkan penjelasan ke ::: {{.catatan}}: '{t[:60]}…'")
        if re.search(r"[.!?;:]\s+\S", t.rstrip(".")):
            masalah.append(f"baris {baris}: judul tabel lebih dari satu kalimat/klausa; "
                           f"sisanya ke ::: {{.catatan}}: '{t[:60]}…'")
    knit = md.read_text(encoding="utf-8") if md else ""
    for bahasa, isi, awal in chunk:
        if bahasa != "python":
            continue
        lab = re.search(r"#\|\s*label:\s*(fig-[\w-]+)", isi)
        if not lab or not _multipanel(isi):
            continue
        lab = lab.group(1)
        if "label_panel(" not in isi:
            masalah.append(f"baris {awal}: {lab} berpanel banyak tetapi tidak memanggil label_panel()")
        if knit:
            m = re.search(r'src="[^"]*/' + re.escape(lab) + r'-1\.png"[^>]*alt="([^"]*)"', knit) or \
                re.search(r'!\[([^\]]*)\]\([^)]*/' + re.escape(lab) + r'-1\.png', knit)
            cap = m.group(1) if m else ""
            if m and not ("(a)" in cap and "(b)" in cap):
                masalah.append(f"baris {awal}: keterangan {lab} tidak menyebut panel (a), (b), …")
            if m and POLA_ARAH.search(cap):
                masalah.append(f"baris {awal}: keterangan {lab} memakai arah panel "
                               f"('{POLA_ARAH.search(cap).group(0)}'); pakai (a), (b), …")
    for nomor, b in prosa:
        if re.match(r"#{1,6}\s", b) and "?" in re.sub(r"\{[^}]*\}\s*$", "", b):
            masalah.append(f"baris {nomor}: judul/subjudul berupa kalimat tanya; ubah menjadi frasa "
                           f"pernyataan (pertanyaan boleh di prosa): '{b.strip()[:70]}'")
        bersih = re.sub(r"`[^`]*`", " ", b)
        for m in re.finditer(r"@fig-[\w-]+\s*\((?:kiri|kanan|atas|bawah|tengah)[^)]*\)", bersih, flags=re.I):
            masalah.append(f"baris {nomor}: rujukan panel '{m.group(0)}'; tulis @fig-x(a)")
        for m in POLA_ARAH.finditer(bersih):
            if m.group(0).lower().startswith("panel"):
                masalah.append(f"baris {nomor}: '{m.group(0)}' di prosa; tulis @fig-x(a), @fig-x(b)")
    catat("G-JUDUL", not masalah, "\n".join(masalah[:40]))


# ---------------------------------------------------------------- G-LARANGAN dan G-ISTILAH
# Keputusan penulis yang dapat diperiksa dengan pola kata ditambahkan sebagai
# entri konfig.json, bukan dengan menyunting harness (lihat
# references/harness-dan-gerbang.md, "Menambah gerbang dari keputusan penulis").
def _prosa_bersih(qmd):
    prosa, chunk = pilah_qmd(qmd.read_text(encoding="utf-8"))
    keluar = []
    for nomor, b in prosa:
        b = re.sub(r"`[^`]*`", " ", b)
        b = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", " ", b)
        b = re.sub(r"\{#[^}]*\}|\[@[^\]]*\]|@\w[\w:-]*", " ", b)
        keluar.append((nomor, b))
    # judul dan catatan di opsi chunk juga tercetak
    for _, isi, awal in chunk:
        for k, b in enumerate(isi.splitlines()):
            m = re.match(r"\s*[#%]\|\s*(?:fig|tbl)-cap:\s*(.*)$", b)
            if m:
                keluar.append((awal + k + 1, m.group(1)))
    return keluar


def _cocokkan(qmd, aturan, abaikan):
    temuan = []
    for nomor, b in _prosa_bersih(qmd):
        for a in aturan:
            for m in re.finditer(a["pola"], b, flags=re.I):
                konteks = b[max(0, m.start() - 30):m.end() + 30].strip()
                if any(x in b for x in abaikan):
                    continue
                temuan.append(f"baris {nomor}: '{m.group(0)}' — {a['saran']}: …{konteks}…")
    return temuan


def gerbang_larangan(qmd, peng):
    t = _cocokkan(qmd, KONFIG["larangan"], peng.get("larangan-abaikan", []))
    catat("G-LARANGAN", not t, "\n".join(t[:40]))


def gerbang_istilah(qmd, peng):
    aturan = KONFIG["istilah_terlarang"]
    if not aturan:
        return
    t = _cocokkan(qmd, aturan, peng.get("istilah-abaikan", []))
    catat("G-ISTILAH", not t, "\n".join(t[:60]))


# ---------------------------------------------------------------- G-LN
# Keputusan seri Bayesian 2026-11-07 (bawaan skill): logaritma natural ditulis
# ln di naskah (prosa, rumus, tabel, gambar); kode R/Stan dan keluarannya tetap
# log(). Gerbang ini memeriksa rumus prosa dan judul chunk: \log tanpa subskrip
# basis gagal; \log_{10}, \log_2, blok kode, R inline, dan kode sebaris dilewati.
POLA_LOG_NATURAL = re.compile(r"\\log(?![A-Za-z])(?!\s*_)")


def masalah_ln(teks):
    prosa, chunk = pilah_qmd(teks)
    baris = list(prosa)
    for _, isi, awal in chunk:  # fig-cap/tbl-cap tercetak sebagai prosa
        for k, b in enumerate(isi.splitlines()):
            if re.match(r"\s*[#%]\|\s*(?:fig|tbl)-(?:cap|subcap|alt)\s*:", b):
                baris.append((awal + k + 1, b))
    temuan = []
    for nomor, b in baris:
        b = re.sub(r"<!--.*?-->", " ", b)
        b = re.sub(r"`[^`]*`", " ", b)  # R inline dan kode sebaris
        for m in POLA_LOG_NATURAL.finditer(b):
            konteks = b[max(0, m.start() - 30):m.end() + 30].strip()
            temuan.append(f"baris {nomor}: \\log tanpa basis — tulis \\ln (basis lain: \\log_{{b}}): …{konteks}…")
    return temuan


def gerbang_ln(qmd, peng):
    abaikan = peng.get("ln-abaikan", [])
    t = [x for x in masalah_ln(qmd.read_text(encoding="utf-8")) if not any(a in x for a in abaikan)]
    catat("G-LN", not t, "\n".join(t[:60]))


# ---------------------------------------------------------------- G-HALJUDUL
# Keputusan penulis 2026-11-07: buku tidak memakai subjudul (judul saja,
# termasuk sampul); halaman judul draf memuat "Draf revisi ke-N" sebelum
# tanggal lewat date-format (teks di kolom date menghasilkan "Invalid Date").
def gerbang_haljudul(buku):
    q = buku / "_quarto.yml"
    if not q.exists():
        return
    teks = q.read_text(encoding="utf-8")
    masalah = []
    if re.search(r"^\s*subtitle\s*:", teks, flags=re.M):
        masalah.append("_quarto.yml memuat subtitle; buku hanya memakai judul")
    m = re.search(r"^\s*date\s*:\s*\"?([^\"\n]*)", teks, flags=re.M)
    if m and not re.fullmatch(r"\d{4}-\d{2}-\d{2}|today|last-modified", m.group(1).strip()):
        masalah.append(f"date '{m.group(1).strip()}' bukan tanggal ISO; teks revisi ditaruh di date-format")
    if os.environ.get("DRAF", "1") == "1" and not re.search(
            r"date-format\s*:\s*\"\[Draf revisi ke-\d+", teks):
        masalah.append('date-format tidak memuat "[Draf revisi ke-N · ]" (set DRAF=0 untuk versi terbit)')
    catat("G-HALJUDUL", not masalah, "\n".join(masalah))


# ---------------------------------------------------------------- utama
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--buku")
    ap.add_argument("--bab")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--tag-pdf", metavar="PDF",
                    help="hanya jalankan G-TAG pada PDF ini (uji fikstur, PDF hasil render)")
    a = ap.parse_args()
    if a.tag_pdf:
        gerbang_tag(None, pdf=Path(a.tag_pdf))
        sys.exit(0 if all(ok for _, ok, _ in hasil) else 1)
    if not (a.buku and a.bab):
        ap.error("--buku dan --bab wajib (kecuali dengan --tag-pdf)")
    buku = AKAR / a.buku
    qmd = buku / f"{a.bab}.qmd"
    peng = muat_pengecualian()
    print(f"Harness {a.buku}/{a.bab} — {datetime.now():%Y-%m-%d %H:%M}")

    ident = id_bab(buku, a.bab)
    gerbang_haljudul(buku)
    gerbang_angka(qmd, ident, peng)
    gerbang_keluaran_python(qmd)
    gerbang_lebar_kode(qmd)
    gerbang_rujukan(qmd, buku)
    gerbang_sitasi(qmd, buku)
    gerbang_larangan(qmd, peng)
    gerbang_istilah(qmd, peng)
    if os.environ.get("LN", "1") == "1":
        gerbang_ln(qmd, peng)
    bukti_ref = gerbang_referensi(qmd, ident, buku)
    md = gerbang_kode(buku, a.bab)
    if md:
        gerbang_bocor(md)
        if os.environ.get("TEPI", "1") == "1":
            gerbang_lebar_keluaran(md)
    gerbang_judul(qmd, md)
    if os.environ.get("KONJUNGSI", "1") == "1":
        gerbang_konjungsi(qmd, peng)
    m_eq = cek_persamaan(qmd)
    catat("G-PERSAMAAN", not m_eq, "\n".join(m_eq[:30]))
    if os.environ.get("ATRIBUSI_MANUAL", "1") == "1":
        m = cek_atribusi_manual(qmd, buku)
        catat("G-ATRIBUSI", not m, "\n".join(m[:40]))
    gerbang_lampiran(buku, a.bab, AKAR / KONFIG["lampiran"] / a.buku)
    warning = []
    if md:
        f_eyd, f_gaya = prosa_dari_rajutan(md, a.bab)
        warning = gerbang_eyd(f_eyd, peng)
        gerbang_gaya(f_gaya, peng)
        gerbang_slop(f_eyd, peng)
    gerbang_penggalan(buku, sesudah_render=False)
    if a.render:
        gerbang_render(buku)
        gerbang_penggalan(buku, sesudah_render=True)

    lulus = all(ok for _, ok, _ in hasil)
    laporan = AKAR / "harness" / "laporan" / f"{a.buku.replace('/', '_')}-{a.bab}.md"
    baris = [f"# Laporan harness {a.buku}/{a.bab}", "",
             f"Waktu: {datetime.now():%Y-%m-%d %H:%M}", f"Status: {'LULUS' if lulus else 'GAGAL'}", "",
             "| Gerbang | Status |", "| --- | --- |"]
    baris += [f"| {g} | {'LULUS' if ok else 'GAGAL'} |" for g, ok, _ in hasil]
    for g, ok, r in hasil:
        if r:
            baris += ["", f"## {g}", "", "```", r, "```"]
    if bukti_ref:
        baris += ["", "## Bukti referensi", ""] + [f"- {r}" for r in bukti_ref]
    if warning:
        baris += ["", "## WARNING EYD yang ditinjau manual", ""]
        baris += [f"- {t['kategori']}: '{t['temuan']}' → {t['saran']}" for t in warning]
    laporan.parent.mkdir(parents=True, exist_ok=True)
    laporan.write_text("\n".join(baris) + "\n", encoding="utf-8")
    print(f"\nStatus: {'LULUS' if lulus else 'GAGAL'} — laporan: {laporan}")
    if warning:
        print(f"Catatan: {len(warning)} WARNING EYD perlu ditinjau manual (lihat laporan).")
    sys.exit(0 if lulus else 1)


if __name__ == "__main__":
    main()
