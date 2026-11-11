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
  G-LEBAR-KODE baris R maksimal 72 karakter, Python 79 (konfig batas_kode, batas_kode_python)
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
  G-LEBAR-KELUARAN keluaran kode tercetak <= 78 karakter (konfig batas_keluaran; TEPI=1)
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
  G-RUMUS      rumus dan simbol (cek_rumus.py R1–R12): ERROR menggagalkan; WARNING
               (simbol tanpa keterangan, arti ganda, pemenggalan) untuk reviewer rumus
  G-STRUKTUR   pengantar bab 120+ kata (studi kasus/cerita), subbab ringkas
               (≤ subbab_maks_kata), Rangkuman/Ringkasan di akhir bab (bukan buku kunci)
  G-PERTANYAAN (WARNING, tidak menggagalkan) subbab bernomor tanpa kalimat tanya di paragraf
               prosa pertamanya; pengecualian judul: konfig "pertanyaan_kecuali"
  G-GAYA-AJAR  (hanya --tahap akhir) sapaan (bawaan kita, tanpa Anda), kata "pembaca" sebagai pelaku,
               panjang kalimat, kepadatan sitasi per 1.000 kata (references/gaya-buku-ajar.md)
  G-HALJUDUL   _quarto.yml tanpa subtitle; date ISO; date-format "[Draf revisi ke-N · ]..." (DRAF=1)
  G-DOCX-RUMUS rumus Word asli (OMML) di DOCX: jumlah m:oMath >= rumus sumber - toleransi,
               tanpa TeX mentah di teks biasa, tanpa gambar rumus (setelah --render; DOCX_RUMUS=0)
  G-DOCX       Word: ukuran halaman dan margin = ukuran buku, gambar di dalam bidang teks dan
               berteks alternatif, tanpa ikon kotak, tanpa "??"/@rujukan mentah, judul Heading1
               bernomor; dengan word-otomatis.lua: SEQ = objek bernomor, REF ke bookmark yang ada,
               TOC isi/gambar/tabel, hak cipta sebelum daftar isi; dengan zotero-word.lua: setiap
               sitasi bidang ADDIN ZOTERO_ITEM berJSON sah (itemData tersemat, plainCitation =
               hasil), tanpa sitasi statis, satu ZOTERO_BIBL, ZOTERO_PREF_n (setelah --render; DOCX=0)
  G-HURUF      semua huruf tersemat di PDF buku dan PDF gambar termasuk keluarga opsi
               "huruf" di konfig.json (_bersama/huruf.py; setelah --render; HURUF=0 mematikan)

Tata letak proyek yang diharapkan (jalur dapat diubah di harness/konfig.json):
  <proyek>/harness/{harness.py, referensi.py, penggalan.py, klaim.json,
                    referensi.json, pengecualian.json, konfig.json, sumber/}
  <proyek>/_bersama/{gaya_gambar.py, catatan.lua, bahasa-asing.lua, tikz-preamble.tex, ...}
  <proyek>/<buku>/{_quarto.yml, pustaka.bib, bab01.qmd, ...}
  <proyek>/lampiran-kode/<buku>/   (dibangkitkan G-LAMPIRAN)

Pemakaian:
  python3 harness/harness.py --buku buku1 --bab bab02
  python3 harness/harness.py --buku buku1 --bab bab02 --render
  python3 harness/harness.py --buku buku1 --bab bab02 --tahap akhir   # sesudah tahap gaya (22–23)
  python3 harness/harness.py --tag-pdf buku1/_book/buku.pdf     # G-TAG saja
  python3 harness/harness.py --docx-rumus buku.docx --sumber bab01.qmd ...   # G-DOCX-RUMUS saja
  python3 harness/harness.py --docx-cek buku.docx [--ukuran unesco]          # G-DOCX saja
  python3 harness/harness.py --huruf-pdf gambar/x.pdf [--huruf springer]   # G-HURUF saja
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
    # Struktur bab dan gaya buku ajar (references/gaya-buku-ajar.md)
    "pengantar_min_kata": 120,
    "subbab_maks_kata": 800,
    "rangkuman_min_kata": 40,
    "rangkuman_maks_kata": 450,
    "struktur_abaikan_buku": ["kunci"],   # awalan nama folder buku yang tidak diperiksa G-STRUKTUR
    "sapaan": "kita",                    # "kita", "Anda", atau "kita+Anda"
    "anda_maks": 0,
    "sapaan_per_1000_kata_min": 3,
    "pembaca_pelaku_maks": 3,
    "rerata_kata_kalimat_maks": 20,
    "kalimat_maks_kata": 35,
    "sitasi_per_1000_kata_maks": 4,
    # G-PERTANYAAN (WARNING): judul subbab (awalan, tanpa beda huruf besar/kecil) yang tidak
    # diperiksa kalimat tanya di paragraf prosa pertamanya
    "pertanyaan_kecuali": ["Ringkasan", "Rangkuman", "Latihan", "Contoh utama", "Bacaan lanjut"],
    # Istilah yang sudah diputuskan penulis: pola regex -> saran (dan tanggal keputusan)
    "istilah_terlarang": [],
    # Opsi huruf (libertinus, springer, crc, stix), profil ukuran (seri, springer,
    # crc, wiley), dan gaya Word ("windows": Times New Roman/Courier New/Cambria Math);
    # diterapkan oleh _bersama/huruf.py, diperiksa G-HURUF.
    "huruf": "libertinus",
    "profil": "seri",
    "docx_huruf": "",
    # Ukuran buku (b5, unesco, a5, a4, 6x9, 7x10) dan batas baris kode/keluaran
    "ukuran": "b5",
    "batas_kode": 72,
    "batas_kode_python": 79,
    "batas_keluaran": 78,
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
    try:
        p = subprocess.run(perintah, cwd=cwd, env=lingk, capture_output=True,
                           text=True, timeout=batas)
    except FileNotFoundError:
        # Interpreter tidak terpasang: gerbang dicatat GAGAL dengan pesan jelas,
        # bukan menghentikan harness (gerbang lain tetap dijalankan dan dilaporkan).
        return 127, f"perintah tidak ditemukan: {perintah[0]} (pasang dulu, mis. R + knitr)"
    except subprocess.TimeoutExpired:
        return 124, f"melewati batas waktu {batas} detik: {' '.join(perintah[:3])}"
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
# Baris R yang panjang terpotong di kolom; Python mengikuti PEP 8. Batas dibaca
# dari konfig.json ("batas_kode", "batas_kode_python") karena ukuran buku kecil
# (unesco, a5) memerlukan batas lebih kecil atau huruf mono lebih kecil
# (_bersama/huruf.py menghitung ukuran mono dari batas ini).
BATAS_LEBAR = {"r": int(KONFIG.get("batas_kode", 72)), "python": int(KONFIG.get("batas_kode_python", 79))}


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


BATAS_LEBAR_KELUARAN = int(KONFIG.get("batas_keluaran", 78))


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


# Singkatan bertitik yang bukan akhir kalimat (selain SINGKATAN di G-PARAGRAF).
SINGKATAN_KONJ = ["mis.", "misal.", "dkk.", "dll.", "dsb.", "dst.", "hlm.", "s.d.", "vs.", "bdk.",
                  "a.l.", "sbb.", "No.", "no.", "Vol.", "vol.", "ed.", "Ed.", "Prof.", "Dr.", "et al.",
                  "e.g.", "i.e.", "cf.", "Jl.", "Bab.", "Gbr."]
POLA_AKHIR_KALIMAT = re.compile(r"[.!?][\"”’)*_]*\s+(?=[\"“‘(*_]*[A-Z0-9])")


def _awal_kalimat_konj(teks, posisi):
    """Indeks awal kalimat yang memuat teks[posisi]. Titik pada singkatan (dkk., mis.)
    dan angka (1.000; desimal seri memakai koma, 0,5) bukan batas kalimat."""
    t = teks[:posisi]
    for s in sorted(set(SINGKATAN_KONJ + SINGKATAN), key=len, reverse=True):
        t = re.sub(r"(?<![\w.])" + re.escape(s), lambda m: m.group(0).replace(".", "§"), t)
    t = re.sub(r"(?<=\d)\.(?=\d)", "§", t)
    awal = 0
    for m in POLA_AKHIR_KALIMAT.finditer(t):
        awal = m.end()
    return awal


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
        for m in re.finditer(r",\s+jadi\b(?!\s+(?:sebuah|satu|dua|bahan|masalah)\b)", bersih):
            masalah.append(f"baris {nomor}: 'jadi' penghubung antarkalimat (EYD V B.5) di tengah kalimat; "
                           f"pecah kalimat ('. Jadi, …') atau tulis '… sehingga …'/'… maka …'")
        for m in POLA_KONJ.finditer(bersih):
            sisa = bersih[m.end():]
            sisip = re.match(r"([^,.;:]*),", sisa)
            if sisip and len(sisip.group(1).split()) <= 3:
                continue  # keterangan sisipan, mis. ", bila perlu,"
            awal = _awal_kalimat_konj(bersih, m.start())
            segmen = re.split(r"[;:(]|,(?!\d)", bersih[awal:m.start()])  # 0,5 bukan pemisah
            if len(segmen) >= 2 and re.match(
                    r"\s*(?:bukan|misalnya|yaitu|yakni|seperti|termasuk|terutama|khususnya|antara lain"
                    r"|kecuali|selain|tidak hanya|baik)\b", segmen[-1]):
                continue  # koma menutup sisipan/aposisi (EYD V B.13)
            if len(segmen) == 1 and re.fullmatch(
                    r"\s*[*_]*(?:Jadi|Namun|Akibatnya|Artinya|Maka|Sebaliknya|Selain itu|Oleh karena itu"
                    r"|Karena itu|Dengan demikian|Dengan kata lain|Misalnya|Contohnya)[*_]*\s*", segmen[0]):
                continue  # "Jadi, bila …": anak kalimat mendahului induk di awal kalimat
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
    # Sapaan "kita" dianjurkan (gaya-buku-ajar.md §1, keputusan 2026-11-10); yang ditolak hanya pengumuman meta.
    (r"\bmari (?:kita|saya) (?:lihat|bahas|pelajari|simak|telusuri|selami|mulai|ulas|eksplorasi|kupas)\b|\bmari saya\b",
     "komentar meta; langsung kerjakan (sapaan kita tetap boleh)"),
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
    if os.environ.get("HURUF", "1") == "1":
        gerbang_huruf(buku)
    if os.environ.get("DOCX_RUMUS", "1") == "1":
        gerbang_docx_rumus(buku)
    if os.environ.get("DOCX", "1") == "1":
        gerbang_docx(buku)


# ---------------------------------------------------------------- G-DOCX-RUMUS
# Rumus di Word harus persamaan Word asli (OMML) agar dapat disunting dan
# dikonversi (mis. ke MathType), bukan gambar atau teks TeX mentah.
TEX_MENTAH = re.compile(r"\\(?:frac|sum|prod|int|sqrt|alpha|beta|gamma|delta|theta|lambda|mu|sigma|"
                        r"pi|hat|bar|mathbf|mathrm|operatorname|left|right|begin|end)\b|\^\{|_\{")
GAMBAR_RUMUS = re.compile(r"(?:^|[-_ ])(?:eq|rumus|persamaan|equation)(?:[-_ ]|$)|\\(?:frac|sum|alpha)", re.I)
TOLERANSI_RUMUS = (0.02, 2)   # boleh kurang 2% atau 2 rumus (yang lebih besar)


def hitung_rumus(teks):
    r"""Jumlah rumus Pandoc di prosa .qmd: blok $$...$$ dan $...$ sebaris
    (aturan Pandoc tex_math_dollars: $ pembuka tidak diikuti spasi, $ penutup
    tidak didahului spasi dan tidak diikuti angka), di luar chunk, kode
    sebaris, R inline, komentar HTML, dan \$."""
    prosa, _ = pilah_qmd(teks)
    isi = "\n".join(b for _, b in prosa)
    isi = re.sub(r"<!--.*?-->", " ", isi, flags=re.S)
    isi = re.sub(r"`[^`\n]*`", " ", isi)
    isi = isi.replace(r"\$", " ")
    blok = len(re.findall(r"\$\$.+?\$\$", isi, flags=re.S))
    isi = re.sub(r"\$\$.+?\$\$", " ", isi, flags=re.S)
    sebaris = len(re.findall(r"\$(?=\S)[^$\n]*?(?<=\S)\$(?!\d)", isi))
    return blok + sebaris


def masalah_docx_rumus(docx, harap=None):
    """Daftar masalah rumus di DOCX; harap = jumlah rumus di sumber."""
    import zipfile
    with zipfile.ZipFile(docx) as z:
        xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    masalah = []
    n_omath = len(re.findall(r"<m:oMath[ >]", xml))
    if harap is not None:
        batas = harap - max(TOLERANSI_RUMUS[1], int(TOLERANSI_RUMUS[0] * harap))
        if n_omath < batas:
            masalah.append(f"(a) {n_omath} m:oMath di DOCX, sumber memuat {harap} rumus (minimal {batas})")
    tanpa_math = re.sub(r"<m:oMath(?:Para)?[ >].*?</m:oMath(?:Para)?>", " ", xml, flags=re.S)
    for par in re.findall(r"<w:p[ >].*?</w:p>", tanpa_math, flags=re.S):
        if re.search(r'<w:pStyle w:val="SourceCode"', par):
            continue
        for run in re.findall(r"<w:r[ >].*?</w:r>", par, flags=re.S):
            if re.search(r'<w:rStyle w:val="(?:VerbatimChar|[A-Za-z]*Tok)"', run):
                continue
            teks = "".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", run))
            m = TEX_MENTAH.search(teks)
            if m:
                masalah.append(f"(b) TeX mentah di teks biasa: '{teks.strip()[:60]}'")
    for tag in re.findall(r"<wp:docPr [^>]*>", xml):
        nama = (re.search(r'name="([^"]*)"', tag) or [None, ""])[1]
        alt = (re.search(r'descr="([^"]*)"', tag) or [None, ""])[1]
        if GAMBAR_RUMUS.search(nama) or GAMBAR_RUMUS.search(alt or ""):
            masalah.append(f"(c) gambar tampak seperti rumus: name='{nama[:40]}', alt='{(alt or '')[:40]}'")
    return masalah, n_omath


def gerbang_docx_rumus(buku, docx=None, sumber=None):
    if docx is None:
        daftar = list((buku / "_book").glob("*.docx"))
        if not daftar:
            catat("G-DOCX-RUMUS", False, "DOCX tidak ditemukan di _book/")
            return
        docx = daftar[0]
        yml = (buku / "_quarto.yml").read_text(encoding="utf-8")
        sumber = [buku / f for f in re.findall(r"^\s*-\s*(\S+\.qmd)", yml, flags=re.M) if (buku / f).exists()]
    harap = sum(hitung_rumus(Path(s).read_text(encoding="utf-8")) for s in sumber) if sumber else None
    masalah, n = masalah_docx_rumus(docx, harap)
    # (d) fon rumus Word: m:mathFont di settings.xml sama dengan fon rumus opsi
    # (gaya Word Windows: Cambria Math); dipasang huruf.py --pasca-render.
    modul = _modul_huruf()
    if modul is not None and buku is not None:
        import zipfile
        harap_fon = modul.fon_rumus_docx(KONFIG.get("huruf", "libertinus"), KONFIG.get("docx_huruf", ""))
        with zipfile.ZipFile(docx) as z:
            s = z.read("word/settings.xml").decode("utf-8", errors="replace")
        m = re.search(r'<m:mathFont m:val="([^"]+)"', s)
        if not m or m.group(1) != harap_fon:
            masalah.append(f"(d) m:mathFont {m.group(1) if m else 'tidak ada'}, seharusnya {harap_fon} "
                           "(post-render _bersama/huruf.py --pasca-render di _quarto.yml)")
    print(f"    G-DOCX-RUMUS: {n} m:oMath di {Path(docx).name}; sumber {harap} rumus")
    catat("G-DOCX-RUMUS", not masalah, "\n".join(masalah[:40]))


# ---------------------------------------------------------------- G-DOCX
def _attr(tag, nama):
    m = re.search(rf'{nama}="(\d+)"', tag)
    return int(m.group(1)) if m else 0


def _teks_xml(par):
    return "".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", par))


SKEMA_CSL_CITATION = "https://github.com/citation-style-language/schema/raw/master/csl-citation.json"


def bidang_word(document_xml, statis=None):
    """Bidang kompleks Word (fldChar begin/separate/end, termasuk bersarang)
    sebagai daftar (kode, teks hasil). Bila `statis` berupa list, tautan
    sitasi (w:hyperlink ke bookmark ref-<kunci>) di luar bidang Zotero dicatat."""
    import xml.etree.ElementTree as ET
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    tumpukan, hasil_bidang = [], []
    for el in ET.fromstring(document_xml).iter():
        if el.tag == W + "hyperlink" and statis is not None \
                and (el.get(W + "anchor") or "").startswith("ref-") \
                and not any("ZOTERO_" in "".join(f["kode"]) for f in tumpukan):
            statis.append(el.get(W + "anchor"))
        if el.tag == W + "fldChar":
            jenis = el.get(W + "fldCharType")
            if jenis == "begin":
                tumpukan.append({"kode": [], "hasil": [], "tahap": "kode"})
            elif jenis == "separate" and tumpukan:
                tumpukan[-1]["tahap"] = "hasil"
            elif jenis == "end" and tumpukan:
                f = tumpukan.pop()
                teks = "".join(f["hasil"])
                hasil_bidang.append(("".join(f["kode"]), teks))
                if tumpukan and tumpukan[-1]["tahap"] == "hasil":
                    tumpukan[-1]["hasil"].append(teks)
        elif el.tag == W + "instrText" and tumpukan:
            tumpukan[-1]["kode"].append(el.text or "")
        elif el.tag in (W + "t", W + "tab") and tumpukan and tumpukan[-1]["tahap"] == "hasil":
            tumpukan[-1]["hasil"].append(el.text or "" if el.tag == W + "t" else "\t")
    return hasil_bidang


def masalah_zotero(docx):
    """Sitasi Zotero hidup (scripts/zotero-word.lua): setiap sitasi bidang
    ADDIN ZOTERO_ITEM CSL_CITATION dengan JSON sah (citationID, schema,
    plainCitation = teks hasil bidang, citationItems dengan uris dan itemData
    berjudul/berjenis/berpenulis/bertahun), tanpa tautan sitasi ref-<kunci>
    di luar bidang Zotero, tepat satu ZOTERO_BIBL, dan ZOTERO_PREF_1..n
    (<= 255 karakter) di docProps/custom.xml yang tersambung menjadi
    <data data-version="3"> dengan <style id=...>. Dokumen tanpa sitasi lulus."""
    import zipfile
    import xml.etree.ElementTree as ET
    with zipfile.ZipFile(docx) as z:
        statis = []
        semua = bidang_word(z.read("word/document.xml"), statis)
        custom = z.read("docProps/custom.xml").decode("utf-8") if "docProps/custom.xml" in z.namelist() else ""
    masalah, item, bibl = [], 0, 0
    if statis:
        masalah.append(f"{len(statis)} sitasi statis (tautan ke ref-… di luar bidang Zotero), mis. "
                       f"{', '.join(sorted(set(statis))[:5])}: pasang zotero-word.lua (at: post-render)")
    for kode, teks in semua:
        k = kode.strip()
        if k.startswith("ADDIN ZOTERO_ITEM"):
            item += 1
            try:
                d = json.loads(k[k.index("{"): k.rindex("}") + 1])
            except ValueError as e:
                masalah.append(f"JSON ZOTERO_ITEM tidak sah: {e}: {k[:70]}")
                continue
            p = d.get("properties", {})
            if not d.get("citationID") or d.get("schema") != SKEMA_CSL_CITATION:
                masalah.append(f"ZOTERO_ITEM tanpa citationID/schema: {k[:70]}")
            if p.get("plainCitation") != teks:
                masalah.append(f"plainCitation {p.get('plainCitation')!r} != hasil bidang {teks!r}")
            if not d.get("citationItems"):
                masalah.append("ZOTERO_ITEM tanpa citationItems")
            for b in d.get("citationItems", []):
                it = b.get("itemData", {})
                if not b.get("uris") or not it.get("title") or not it.get("type") \
                        or not (it.get("author") or it.get("editor")) or not it.get("issued"):
                    masalah.append(f"citationItem {b.get('id')} tanpa uris/title/type/author/issued")
        elif k.startswith("ADDIN ZOTERO_BIBL"):
            bibl += 1
            if not k.endswith("CSL_BIBLIOGRAPHY") or not teks.strip():
                masalah.append("ZOTERO_BIBL tanpa CSL_BIBLIOGRAPHY atau hasil kosong")
    if not item:
        return masalah
    if bibl != 1:
        masalah.append(f"{bibl} bidang ZOTERO_BIBL (seharusnya 1)")
    potong = {}
    if custom:
        for prop in ET.fromstring(custom):
            m = re.fullmatch(r"ZOTERO_PREF_(\d+)", prop.get("name", ""))
            if m:
                potong[int(m.group(1))] = "".join(prop.itertext())
    if not potong or sorted(potong) != list(range(1, len(potong) + 1)) \
            or any(len(v) > 255 for v in potong.values()):
        masalah.append("ZOTERO_PREF_1.. (maks. 255 karakter) tidak ada atau tidak berurutan di docProps/custom.xml")
    else:
        try:
            d = ET.fromstring("".join(potong[i] for i in sorted(potong)))
            if d.get("data-version") != "3" or d.find("style") is None or not d.find("style").get("id"):
                masalah.append("ZOTERO_PREF tanpa data-version 3 atau <style id>")
        except ET.ParseError as e:
            masalah.append(f"ZOTERO_PREF bukan XML: {e}")
    return masalah


def masalah_docx(docx, ukuran_mm=None, bernomor=False, margin_mm=None, otomatis=True, zotero=True):
    """Pemeriksaan otomatis keluaran Word (daftar periksa
    assets/templat-tinjauan-docx.md): ukuran halaman = ukuran buku, margin =
    margin ukuran di konfig.json, gambar tidak melebihi bidang teks dan
    berteks alternatif, tanpa ikon kotak (gambar <= 0,2 inci), tanpa "??" atau
    rujukan @fig-/@sec-/@tbl-/@eq- mentah, ada Heading1, dan judul bernomor
    bila number-sections. otomatis=True (word-otomatis.lua terpasang): jumlah
    bidang SEQ Gambar/Tabel/Persamaan = jumlah objek bernomor, setiap REF
    menunjuk bookmark yang ada, bidang TOC daftar isi/gambar/tabel ada, dan
    halaman hak cipta (gaya "Hak Cipta") sebelum daftar isi. zotero=True
    (zotero-word.lua terpasang): masalah_zotero."""
    import zipfile
    with zipfile.ZipFile(docx) as z:
        xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    masalah = []
    sect = re.findall(r"<w:sectPr[ >].*?</w:sectPr>", xml, flags=re.S)
    pgsz = re.search(r"<w:pgSz [^>]*>", sect[-1]).group(0) if sect else ""
    pgmar = re.search(r"<w:pgMar [^>]*>", sect[-1]).group(0) if sect else ""
    w, h = _attr(pgsz, "w:w"), _attr(pgsz, "w:h")
    mm = 25.4 / 1440
    if ukuran_mm:
        if abs(w * mm - ukuran_mm[0]) > 2 or abs(h * mm - ukuran_mm[1]) > 2:
            masalah.append(f"halaman {w * mm:.0f} × {h * mm:.0f} mm, seharusnya {ukuran_mm[0]} × {ukuran_mm[1]} mm "
                           "(reference-doc ukuran buku dari huruf.py)")
    if margin_mm:
        nyata = [_attr(pgmar, f"w:{k}") * mm for k in ("left", "right", "top", "bottom")]
        if any(abs(a - b) > 1 for a, b in zip(nyata, margin_mm)):
            masalah.append("margin kiri/kanan/atas/bawah " + "/".join(f"{a:.0f}" for a in nyata) +
                           " mm, seharusnya " + "/".join(f"{b:g}" for b in margin_mm) +
                           " mm seperti PDF (reference-doc dari huruf.py untuk ukuran di konfig.json)")
    bidang = (w - _attr(pgmar, "w:left") - _attr(pgmar, "w:right")) * 635  # EMU
    for tag in re.findall(r"<wp:extent [^>]*>", xml):
        cx = _attr(tag, "cx")
        if bidang and cx > bidang * 1.01:
            masalah.append(f"gambar {cx / 914400:.2f} in melebihi bidang teks {bidang / 914400:.2f} in")
        if cx <= 0.2 * 914400:
            masalah.append(f"gambar kecil {cx / 914400:.2f} in (ikon kotak? set callout-icon: false di format docx)")
    for tag in re.findall(r"<wp:docPr [^>]*>", xml):
        m = re.search(r'descr="([^"]*)"', tag)
        if not m or not m.group(1).strip():
            nama = re.search(r'name="([^"]*)"', tag)
            masalah.append(f"gambar tanpa teks alternatif ({nama.group(1) if nama else '?'}): "
                           "isi fig-alt atau keterangan (word-otomatis.lua)")
    teks = " ".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", xml))
    if "??" in teks:
        masalah.append("'??' di teks: rujukan silang atau sitasi tidak terselesaikan")
    for r in sorted(set(re.findall(r"@(?:fig|sec|tbl|eq|lst|thm)-[\w-]+", teks)))[:10]:
        masalah.append(f"rujukan mentah '{r}' di teks")
    judul = []
    paragraf = re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S)
    keterangan = {"Gambar": 0, "Tabel": 0}
    nomor_persamaan = 0
    for par in paragraf:
        st = re.search(r'<w:pStyle w:val="([^"]+)"', par)
        gaya = st.group(1) if st else ""
        if re.fullmatch(r"Heading\d", gaya):
            judul.append((gaya, _teks_xml(par).strip()))
        elif any("Caption" in g for g in re.findall(r'<w:pStyle w:val="([^"]+)"', par)):
            # Quarto: pPr kedua berisi ImageCaption sesudah pPr gaya paragraf
            m = re.match(r"\s*(Gambar|Tabel)[\s\u00a0]+[\dA-Z]+(?:\.\d+)?", _teks_xml(par))
            if m:
                keterangan[m.group(1)] += 1
        elif gaya == "NomorPersamaan":
            nomor_persamaan += 1
    if not any(g == "Heading1" for g, _ in judul):
        masalah.append("tidak ada judul bergaya Heading1")
    if bernomor and not any(g == "Heading1" and re.match(r"\d+\.?\s", s) for g, s in judul):
        masalah.append("judul bab tidak bernomor di Word (number-sections)")
    if zotero:
        masalah += masalah_zotero(docx)
    if not otomatis:
        return masalah
    # --- fitur otomatis Word (scripts/word-otomatis.lua)
    instr = re.findall(r"<w:instrText[^>]*>([^<]*)</w:instrText>", xml)
    seq = {n: sum(1 for i in instr if re.match(rf"\s*SEQ {n}\b", i)) for n in ("Gambar", "Tabel", "Persamaan")}
    statis = 0
    for om in re.findall(r"<m:oMath>.*?</m:oMath>", xml, flags=re.S):
        # "\qquad(1.1)" tanpa word-otomatis.lua: spasi lebar lalu nomor; kurungnya
        # bisa teks atau pembatas m:d
        if re.search(r"(?:\(|\s)\s*[\dA-Z]+\.\d+\s*\)?\s*$", "".join(re.findall(r"<m:t[^>]*>([^<]*)</m:t>", om))):
            statis += 1
    harap = {"Gambar": keterangan["Gambar"], "Tabel": keterangan["Tabel"], "Persamaan": nomor_persamaan + statis}
    for n in ("Gambar", "Tabel", "Persamaan"):
        if seq[n] != harap[n]:
            masalah.append(f"{seq[n]} bidang SEQ {n}, objek bernomor {harap[n]}"
                           + (f" ({statis} nomor persamaan statis di dalam rumus)" if n == "Persamaan" and statis else "")
                           + ": pasang word-otomatis.lua (at: post-render) di _quarto.yml")
    bookmark = set(re.findall(r'<w:bookmarkStart [^>]*w:name="([^"]+)"', xml))
    for r in sorted({m.group(1) for i in instr for m in [re.match(r"\s*REF\s+(\S+)", i)] if m} - bookmark)[:10]:
        masalah.append(f"REF {r} menunjuk bookmark yang tidak ada")
    toc = [(i, k) for k, i in enumerate(instr) if re.match(r"\s*TOC\b", i)]
    if not any(r"\o" in i for i, _ in toc):
        masalah.append("bidang TOC daftar isi tidak ada (toc: false di docx dan word-otomatis.lua)")
    for n, daftar in (("Gambar", "Daftar Gambar"), ("Tabel", "Daftar Tabel")):
        if harap[n] and not any(f'\\c "{n}"' in i for i, _ in toc):
            masalah.append(f"bidang TOC {daftar} (\\c \"{n}\") tidak ada")
    pos_hc = xml.find('<w:pStyle w:val="HakCipta"')
    pos_toc = xml.find("TOC \\o")
    if pos_hc < 0:
        masalah.append('halaman hak cipta (gaya "Hak Cipta") tidak ada di Word')
    elif pos_toc >= 0 and pos_hc > pos_toc:
        masalah.append("halaman hak cipta sesudah daftar isi; seharusnya sesudah halaman judul, sebelum daftar isi")
    return masalah


def gerbang_docx(buku, docx=None, ukuran_mm=None, bernomor=False, margin_mm=None, otomatis=True,
                 zotero=True):
    if docx is None:
        daftar = list((buku / "_book").glob("*.docx"))
        if not daftar:
            catat("G-DOCX", False, "DOCX tidak ditemukan di _book/")
            return
        docx = daftar[0]
        modul = _modul_huruf()
        if modul is not None:
            uk = modul.ukuran(KONFIG.get("ukuran", "b5"))
            ukuran_mm, margin_mm = uk["kertas"], uk["margin"]
        yml = (buku / "_quarto.yml").read_text(encoding="utf-8")
        bernomor = bool(re.search(r"^number-sections:\s*true", yml, flags=re.M))
        otomatis = "word-otomatis.lua" in yml
        zotero = "zotero-word.lua" in yml
    masalah = masalah_docx(docx, ukuran_mm, bernomor, margin_mm, otomatis, zotero)
    catat("G-DOCX", not masalah, "\n".join(sorted(set(masalah))[:40]))


# ---------------------------------------------------------------- G-HURUF
def _modul_huruf():
    import importlib.util
    for calon in (BERSAMA / "huruf.py", Path(__file__).resolve().parent / "huruf.py"):
        if calon.exists():
            spek = importlib.util.spec_from_file_location("huruf", calon)
            modul = importlib.util.module_from_spec(spek)
            spek.loader.exec_module(modul)
            return modul
    return None


def gerbang_huruf(buku, pdfs=None, nama=None):
    """Semua huruf tersemat (pdffonts) di PDF buku dan PDF gambar (matplotlib,
    TikZ) termasuk keluarga opsi "huruf" (teks, matematika, mono, dan pasangan
    TikZ-nya). Huruf asing (DejaVu, STIXGeneral, CMR pada opsi Times, dst.)
    berarti ada glif yang jatuh ke huruf cadangan lain."""
    modul = _modul_huruf()
    nama = nama or KONFIG.get("huruf", "libertinus")
    if modul is None or not shutil.which("pdffonts"):
        catat("G-HURUF", False, "_bersama/huruf.py atau pdffonts (poppler-utils) tidak ada")
        return
    if pdfs is None:
        pdfs = sorted((buku / "_book").glob("*.pdf"))
        for pola in ("*_files/figure-pdf/*.pdf", "gambar/*.pdf", "_book/*_files/figure-pdf/*.pdf"):
            pdfs += sorted(buku.glob(pola))
    if not pdfs:
        catat("G-HURUF", False, "PDF buku/gambar tidak ditemukan")
        return
    masalah = []
    if buku is not None:  # glif hilang: \tracinglostchars=2 di preamble.tex
        logs = sorted(buku.glob("*.log"), key=lambda p: p.stat().st_mtime)
        logs = [p for p in logs if not p.name.startswith("tikz")]
        if logs:
            hilang = sorted(set(re.findall(r"Missing character: There is no (.+?) in font ([^!\n]+)",
                                           logs[-1].read_text(encoding="utf-8", errors="replace"))))
            masalah += [f"{logs[-1].name}: glif {g} tidak ada di huruf {f.strip()}" for g, f in hilang[:20]]
    for pdf in pdfs:
        asing = modul.huruf_asing(pdf, nama)
        if asing:
            masalah.append(f"{pdf.name}: {', '.join(asing)} (opsi '{nama}' mengizinkan "
                           f"{', '.join(modul.opsi(nama)['izin'][:6])}...)")
    print(f"    G-HURUF: {len(pdfs)} PDF diperiksa (opsi {nama})")
    catat("G-HURUF", not masalah, "\n".join(masalah[:40]))


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
    try:
        import penggalan
    except ImportError as e:
        catat("G-PENGGALAN", False, f"pemenggal tidak dapat dimuat ({e}); pasang: pip install Sastrawi")
        return
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


# ---------------------------------------------------------------- G-RUMUS
def gerbang_rumus(qmd, peng):
    """Rumus dan simbol (references/rumus-dan-simbol.md). ERROR menggagalkan;
    WARNING ditulis di laporan untuk reviewer rumus (06) dan penyunting gaya (22)."""
    sys.path.insert(0, str(AKAR / "harness"))
    try:
        import cek_rumus
    except ImportError as e:
        catat("G-RUMUS", False, f"cek_rumus.py tidak dapat dimuat ({e}); salin dari skill ke harness/")
        return
    abaikan = [a["simbol"] for a in peng.get("rumus-abaikan", []) if "simbol" in a]
    temuan, _ = cek_rumus.periksa([qmd], "id", abaikan)
    err = [x for x in temuan if x["tingkat"] == "ERROR"]
    war = [x for x in temuan if x["tingkat"] != "ERROR"]
    fmt = lambda x: f"baris {x['baris']} {x['kode']} {x['tingkat']}: {x['temuan']} → {x['saran']}"
    catat("G-RUMUS", not err, "\n".join([fmt(x) for x in err] + [fmt(x) for x in war][:40]))


# ---------------------------------------------------------------- G-STRUKTUR dan G-GAYA-AJAR
def _bagian_bab(teks):
    """Pecah bab menjadi bagian (tingkat_judul, judul, baris_awal, daftar_baris_prosa_bersih)."""
    prosa, _ = pilah_qmd(teks)
    bagian = [(1, "(pembuka)", 1, [])]
    dalam_math = False
    for nomor, b in prosa:
        m = re.match(r"^(#{1,6})\s+(.*?)\s*(\{[^}]*\})?\s*$", b)
        if m and not dalam_math:
            bagian.append((len(m.group(1)), m.group(2).strip(), nomor, []))
            continue
        if b.strip().startswith("$$"):
            dalam_math = not (b.strip().count("$$") == 2) and not dalam_math
            continue
        if dalam_math:
            continue
        bagian[-1][3].append(bersihkan_baris_prosa(b))
    return bagian


def _kata(baris):
    teks = " ".join(baris)
    teks = re.sub(r"^:::.*$", " ", teks, flags=re.M)
    teks = re.sub(r":::\s*\{[^}]*\}|:::", " ", teks)
    return re.findall(r"[A-Za-zÀ-ÿ][\w'-]*", teks)


def peringatan_pertanyaan(teks):
    """G-PERTANYAAN (WARNING): subbab bernomor (## atau ### tanpa .unnumbered) yang paragraf prosa
    pertamanya tidak memuat kalimat tanya ('?' di luar kode dan rumus). Kembalikan daftar pesan."""
    kecuali = [k.lower() for k in KONFIG["pertanyaan_kecuali"]]
    prosa, _ = pilah_qmd(teks)
    # kelompokkan baris per judul subbab bernomor
    bagian, saat_ini, dalam_math = [], None, False
    for nomor, b in prosa:
        m = re.match(r"^(#{2,3})\s+(.*?)\s*(\{[^}]*\})?\s*$", b)
        if m and not dalam_math:
            atribut = m.group(3) or ""
            if ".unnumbered" in atribut or ".unlisted" in atribut:
                saat_ini = None
            else:
                saat_ini = (nomor, m.group(2).strip(), [])
                bagian.append(saat_ini)
            continue
        if re.match(r"^#{1}\s", b) and not dalam_math:
            saat_ini = None
            continue
        if saat_ini is None:
            continue
        if b.strip().startswith("$$"):
            dalam_math = not (b.strip().count("$$") == 2) and not dalam_math
            continue
        if dalam_math:
            continue
        saat_ini[2].append(b)
    pesan = []
    for nomor, judul, baris in bagian:
        if any(judul.lower().startswith(k) for k in kecuali):
            continue
        # paragraf prosa pertama: lewati baris kosong, pagar kotak, daftar, tabel, gambar, komentar
        paragraf, mulai = [], False
        for b in baris:
            t = b.strip()
            if not t:
                if mulai:
                    break
                continue
            if re.match(r"^(:::|\||!\[|<|[-*+]\s|\d+[.)]\s)", t) or re.fullmatch(r"\{#[^}]*\}", t):
                if mulai:
                    break
                continue
            mulai = True
            paragraf.append(bersihkan_baris_prosa(b))
        if not paragraf:
            continue  # subbab tanpa paragraf prosa (hanya daftar atau kode)
        if "?" not in " ".join(paragraf):
            pesan.append(f"baris {nomor}: subbab '{judul[:50]}' tidak dibuka pertanyaan wajar pembaca; "
                         "paragraf prosa pertamanya tanpa kalimat tanya (siklus subbab, SKILL.md)")
    return pesan


def gerbang_pertanyaan(qmd):
    """G-PERTANYAAN, tingkat WARNING: tidak masuk daftar gerbang (tidak menggagalkan status)."""
    pesan = peringatan_pertanyaan(qmd.read_text(encoding="utf-8"))
    if pesan:
        print(f"[PERINGATAN] G-PERTANYAAN: {len(pesan)} subbab")
        for p in pesan[:40]:
            print("    " + p)
    return pesan


def gerbang_struktur(qmd, buku):
    """Pengantar menarik, subbab ringkas, rangkuman di akhir bab (keputusan penulis 2026-11-10)."""
    if any(Path(buku).name.startswith(a) for a in KONFIG["struktur_abaikan_buku"]):
        return
    teks = qmd.read_text(encoding="utf-8")
    bagian = _bagian_bab(teks)
    masalah = []
    # pengantar: prosa antara judul bab (#) dan judul ## pertama, di luar kotak
    pengantar, i = [], 0
    while i < len(bagian) and bagian[i][0] <= 1:
        isi = "\n".join(bagian[i][3])
        isi = re.sub(r":::\s*\{\.callout[^}]*\}.*?:::", " ", isi, flags=re.S)
        pengantar += _kata([isi])
        i += 1
    if len(pengantar) < KONFIG["pengantar_min_kata"]:
        masalah.append(f"pengantar bab {len(pengantar)} kata (< {KONFIG['pengantar_min_kata']}); "
                       "buka dengan studi kasus nyata atau cerita pendek yang berakhir pada pertanyaan bab")
    awal = " ".join(pengantar[:6]).lower()
    if re.match(r"^(bab ini|pada bab ini|dalam bab ini|di bab ini)\b", awal):
        masalah.append("pengantar dibuka komentar meta ('Bab ini …'); mulai dari kasus atau cerita")
    # subbab ringkas
    for tingkat, judul, nomor, isi in bagian[i:]:
        n = len(_kata(isi))
        if n > KONFIG["subbab_maks_kata"] and not re.match(r"(?i)(latihan|bacaan lanjut|lampiran)", judul):
            masalah.append(f"baris {nomor}: bagian '{judul[:40]}' {n} kata (> {KONFIG['subbab_maks_kata']}); "
                           "pecah menjadi subbab per konsep")
    # rangkuman
    h2 = [(j, k, n, isi) for j, k, n, isi in bagian if j == 2]
    rang = [b for b in h2 if re.match(r"(?i)^(rangkuman|ringkasan)\b", b[1])]
    if not rang:
        masalah.append("tidak ada subbab 'Rangkuman' (atau 'Ringkasan') di akhir bab")
    else:
        posisi = h2.index(rang[-1])
        sesudah = [b[1] for b in h2[posisi + 1:]]
        if any(not re.match(r"(?i)(latihan|bacaan lanjut|catatan|soal|lampiran|daftar)", s) for s in sesudah):
            masalah.append("Rangkuman bukan bagian isi terakhir; letakkan sesudah semua subbab materi "
                           "(sebelum Bacaan lanjut dan Latihan)")
        n = len(_kata(rang[-1][3]))
        if not KONFIG["rangkuman_min_kata"] <= n <= KONFIG["rangkuman_maks_kata"]:
            masalah.append(f"Rangkuman {n} kata (harus {KONFIG['rangkuman_min_kata']}–{KONFIG['rangkuman_maks_kata']})")
        if re.search(r"\[@|(?<![\w`])@(?!fig-|tbl-|eq-|sec-|Fig-|Tbl-|Eq-|Sec-)\w", "\n".join(rang[-1][3])):
            masalah.append("Rangkuman memuat sitasi; tulis tanpa sitasi")
    catat("G-STRUKTUR", not masalah, "\n".join(masalah))


def gerbang_gaya_ajar(qmd):
    """Tahap gaya akhir (references/gaya-buku-ajar.md §6): sapaan, kalimat, kepadatan sitasi."""
    teks = qmd.read_text(encoding="utf-8")
    prosa, _ = pilah_qmd(teks)
    isi, sitasi, dalam_bacaan, dalam_kotak, dalam_math = [], 0, False, 0, False
    for _, b in prosa:
        m = re.match(r"^#{1,6}\s+(.*)$", b)
        if m:
            dalam_bacaan = bool(re.match(r"(?i)(bacaan lanjut|catatan bab|daftar pustaka|latihan)", m.group(1)))
            continue
        if b.strip().startswith("$$"):
            dalam_math = not (b.strip().count("$$") == 2) and not dalam_math
            continue
        if dalam_math:
            continue
        if b.lstrip().startswith(":::"):
            dalam_kotak += 1 if re.match(r"\s*:::\s*\{", b) else -1
            dalam_kotak = max(dalam_kotak, 0)
            continue
        if dalam_bacaan or dalam_kotak or re.match(r"\s*#\|", b):
            continue
        sitasi += len(re.findall(r"\[@[^\]]*\]", b)) + len(re.findall(r"(?<![\[\w`])@(?!fig-|tbl-|eq-|sec-|Fig-|Tbl-|Eq-|Sec-)\w[\w:-]*", b))
        isi.append(b)
    paragraf = re.split(r"\n\s*\n", "\n".join(isi))
    kata_total, kal_semua = 0, []
    for par in paragraf:
        bersih = bersihkan_baris_prosa(par)
        if not bersih.strip() or bersih.lstrip().startswith(("|", "-", "*", "1.")):
            kata_total += len(re.findall(r"\w+", bersih))
            continue
        for k in kalimat(" ".join(bersih.split())):
            n = len(re.findall(r"[A-Za-zÀ-ÿ0-9][\w'-]*", k))
            if n >= 3:
                kal_semua.append((n, k))
        kata_total += len(re.findall(r"\w+", bersih))
    masalah = []
    per1000 = lambda x: 1000 * x / max(kata_total, 1)
    plain = bersihkan_baris_prosa("\n".join(isi))
    mode = KONFIG.get("sapaan", "kita")
    pola_sapaan = {"kita": r"\b[Kk]ita\b", "Anda": r"\bAnda\b"}.get(mode, r"\bAnda\b|\b[Kk]ita\b")
    sapaan = len(re.findall(pola_sapaan, plain))
    if per1000(sapaan) < KONFIG["sapaan_per_1000_kata_min"]:
        masalah.append(f"sapaan {mode} {per1000(sapaan):.1f} per 1.000 kata (< {KONFIG['sapaan_per_1000_kata_min']}); "
                       "tulis seolah berdialog dengan pembaca")
    if mode == "kita":
        anda = [k for _, k in kal_semua if re.search(r"\bAnda\b", k)]
        if len(anda) > KONFIG.get("anda_maks", 0):
            masalah += [f"'Anda' di prosa (sapaan buku: kita): '{k[:70]}…'" for k in anda[:8]]
    pelaku = re.findall(r"\b[Pp]embaca (?:dapat|bisa|perlu|harus|diharapkan|akan|sudah|telah|mungkin|cukup)\b", plain)
    if len(pelaku) > KONFIG["pembaca_pelaku_maks"]:
        masalah.append(f"'pembaca' sebagai pelaku {len(pelaku)}× (> {KONFIG['pembaca_pelaku_maks']}); ganti dengan sapaan kita")
    if kal_semua:
        rerata = sum(n for n, _ in kal_semua) / len(kal_semua)
        if rerata > KONFIG["rerata_kata_kalimat_maks"]:
            masalah.append(f"rata-rata kalimat {rerata:.1f} kata (> {KONFIG['rerata_kata_kalimat_maks']}); pendekkan")
        panjang = [k for n, k in kal_semua if n > KONFIG["kalimat_maks_kata"]]
        for k in panjang[:10]:
            masalah.append(f"kalimat > {KONFIG['kalimat_maks_kata']} kata: '{k[:80]}…'")
    if per1000(sitasi) > KONFIG["sitasi_per_1000_kata_maks"]:
        masalah.append(f"{sitasi} sitasi = {per1000(sitasi):.1f} per 1.000 kata prosa isi "
                       f"(> {KONFIG['sitasi_per_1000_kata_maks']}); pindahkan sumber pengetahuan baku ke Bacaan lanjut "
                       "(gaya-buku-ajar.md §4)")
    catat("G-GAYA-AJAR", not masalah, "\n".join(masalah))


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
    ap.add_argument("--tahap", choices=["draf", "akhir"], default="draf",
                    help="akhir: sesudah tahap gaya (peran 22–23), tambah G-GAYA-AJAR")
    ap.add_argument("--tag-pdf", metavar="PDF",
                    help="hanya jalankan G-TAG pada PDF ini (uji fikstur, PDF hasil render)")
    ap.add_argument("--huruf-pdf", metavar="PDF", nargs="+",
                    help="hanya jalankan G-HURUF pada PDF ini (uji fikstur, PDF gambar)")
    ap.add_argument("--huruf", help="opsi huruf untuk --huruf-pdf (bawaan: konfig.json)")
    ap.add_argument("--docx-rumus", metavar="DOCX",
                    help="hanya jalankan G-DOCX-RUMUS pada DOCX ini (uji fikstur)")
    ap.add_argument("--sumber", nargs="*", default=[], help="berkas .qmd sumber untuk --docx-rumus")
    ap.add_argument("--docx-cek", metavar="DOCX", help="hanya jalankan G-DOCX pada DOCX ini (uji fikstur)")
    ap.add_argument("--ukuran", default="b5", help="ukuran buku untuk --docx-cek")
    a = ap.parse_args()
    if a.tag_pdf:
        gerbang_tag(None, pdf=Path(a.tag_pdf))
        sys.exit(0 if all(ok for _, ok, _ in hasil) else 1)
    if a.docx_cek:
        modul = _modul_huruf()
        uk = modul.ukuran(a.ukuran) if modul else {}
        gerbang_docx(None, docx=Path(a.docx_cek), ukuran_mm=uk.get("kertas"), margin_mm=uk.get("margin"))
        for g, ok, r in hasil:
            print(f"{g}: {'LULUS' if ok else 'GAGAL'}" + (f"\n{r}" if r else ""))
        sys.exit(0 if all(ok for _, ok, _ in hasil) else 1)
    if a.docx_rumus:
        gerbang_docx_rumus(None, docx=Path(a.docx_rumus), sumber=[Path(s) for s in a.sumber])
        for g, ok, r in hasil:
            print(f"{g}: {'LULUS' if ok else 'GAGAL'}" + (f"\n{r}" if r else ""))
        sys.exit(0 if all(ok for _, ok, _ in hasil) else 1)
    if a.huruf_pdf:
        gerbang_huruf(None, pdfs=[Path(p) for p in a.huruf_pdf], nama=a.huruf)
        for g, ok, r in hasil:
            print(f"{g}: {'LULUS' if ok else 'GAGAL'}" + (f"\n{r}" if r else ""))
        sys.exit(0 if all(ok for _, ok, _ in hasil) else 1)
    if not (a.buku and a.bab):
        ap.error("--buku dan --bab wajib (kecuali dengan --tag-pdf, --huruf-pdf, --docx-rumus, atau --docx-cek)")
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
    gerbang_rumus(qmd, peng)
    gerbang_struktur(qmd, buku)
    w_pertanyaan = gerbang_pertanyaan(qmd)
    if a.tahap == "akhir":
        gerbang_gaya_ajar(qmd)
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
    if w_pertanyaan:
        baris += ["", "## WARNING G-PERTANYAAN yang ditinjau manual", ""]
        baris += [f"- {t}" for t in w_pertanyaan]
    laporan.parent.mkdir(parents=True, exist_ok=True)
    laporan.write_text("\n".join(baris) + "\n", encoding="utf-8")
    print(f"\nStatus: {'LULUS' if lulus else 'GAGAL'} — laporan: {laporan}")
    if w_pertanyaan:
        print(f"Catatan: {len(w_pertanyaan)} WARNING G-PERTANYAAN perlu ditinjau manual (lihat laporan).")
    if warning:
        print(f"Catatan: {len(warning)} WARNING EYD perlu ditinjau manual (lihat laporan).")
    sys.exit(0 if lulus else 1)


if __name__ == "__main__":
    main()
