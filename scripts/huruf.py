#!/usr/bin/env python3
"""Opsi keluarga huruf buku ajar (skill buku-ajar).

Satu kunci memilih keluarga huruf seluruh buku: "huruf" di harness/konfig.json
(bawaan "libertinus"); "profil" memilih ukuran huruf penerbit (seri, springer,
crc, wiley) dan "ukuran" memilih ukuran buku (b5, unesco, a5, a4, 6x9, 7x10).
Ukuran mono kode/keluaran dihitung agar "batas_kode" dan "batas_keluaran"
karakter muat di kolom. Modul ini disalin ke <proyek>/_bersama/huruf.py dan
dipakai oleh tiga pihak:

  - siapkan_proyek.py dan baris perintah di bawah menulis blok bertanda
    ">>> huruf" ... "<<< huruf" di _quarto.yml, _bersama/doc-class.tex,
    preamble.tex, tikz-preamble.tex, dan hak-cipta.tex, serta reference-doc Word;
  - gaya_gambar.py membaca OTF opsi untuk huruf gambar dan mathtext;
  - harness.py (G-HURUF) membaca daftar keluarga yang diizinkan di PDF.

Mengganti opsi di proyek yang sudah ada:
  1. ubah "huruf", "profil", "ukuran", "batas_kode", "batas_keluaran", dan bila perlu
     "docx_huruf": "windows" di harness/konfig.json (atau pakai opsi di bawah);
  2. python3 _bersama/huruf.py --proyek . --buku buku1 [--buku kunci-buku1]
  3. render ulang; G-HURUF memeriksa pdffonts buku dan gambar.

Sumber templat penerbit dan alasannya: references/aturan-gaya-dan-tampilan.md,
subbab "Huruf dan templat penerbit".
"""
import argparse
import json
import re
from pathlib import Path

# Setiap opsi: mainfont, sansfont, mathfont, monofont (+ skala agar 72 karakter
# kode muat di blok lebar 140 mm; lebar karakter efektif <= Libertinus Mono 0,8),
# huruf cadangan (glif yang tidak ada di huruf utama/mono diambil dari keluarga
# yang sama), OTF gambar, paket TikZ (pdfLaTeX), dan prefiks nama huruf yang
# boleh muncul di pdffonts.
OPSI = {
    "libertinus": {
        "nama": "Libertinus (bawaan; satu keluarga lengkap: teks, matematika, mono)",
        "main": "Libertinus Serif", "sans": "Libertinus Serif",
        "math": "Libertinus Math", "mono": "Libertinus Mono", "skala_mono": 0.8, "lebar_mono": 0.64,
        "cadangan_main": [], "cadangan_mono": ["LibertinusSerif-Regular.otf", "LibertinusMath-Regular.otf"],
        "mono_lua": "LibertinusMono",
        "otf": {"regular": "LibertinusSerif-Regular.otf", "italic": "LibertinusSerif-Italic.otf",
                "bold": "LibertinusSerif-Bold.otf", "bolditalic": "LibertinusSerif-BoldItalic.otf",
                "math": "LibertinusMath-Regular.otf"},
        "mathtext_cadangan": "stix",
        "tikz": ["\\usepackage[T1]{fontenc}", "\\usepackage{libertinus}", "\\usepackage{libertinust1math}"],
        "izin": ["Libertinus"],
        "fon_hakcipta": "satu keluarga Libertinus, yaitu Libertinus Serif (teks, judul, dan gambar), "
                        "Libertinus Math (matematika), dan Libertinus Mono (kode), dengan lisensi "
                        "SIL Open Font License 1.1",
        "docx": "reference-b5.docx",
    },
    "springer": {
        "nama": "Times (Springer Nature SNmono/svmono; pendekatan sementara untuk Wiley)",
        "main": "TeX Gyre Termes", "sans": "TeX Gyre Heros",
        "math": "TeX Gyre Termes Math", "mono": "TeX Gyre Cursor", "skala_mono": 0.85, "lebar_mono": 0.6,
        "cadangan_main": ["texgyretermes-math.otf"],
        "cadangan_mono": ["texgyretermes-regular.otf", "texgyretermes-math.otf"],
        "mono_lua": "TeXGyreCursor",
        "otf": {"regular": "texgyretermes-regular.otf", "italic": "texgyretermes-italic.otf",
                "bold": "texgyretermes-bold.otf", "bolditalic": "texgyretermes-bolditalic.otf",
                "math": "texgyretermes-math.otf"},
        "mathtext_cadangan": "stix",
        # Sama dengan templat resmi SNmono: newtxtext + newtxmath[varvw]
        "tikz": ["\\usepackage[T1]{fontenc}", "\\usepackage{newtxtext}", "\\usepackage[varvw]{newtxmath}"],
        "izin": ["TeXGyreTermes", "TeXGyreHeros", "TeXGyreCursor", "NewTX", "ntx", "txsy", "txex",
                 "txmi", "txr", "rtx", "zt"],
        "fon_hakcipta": "TeX Gyre Termes (teks, judul, dan gambar), TeX Gyre Termes Math (matematika), "
                        "TeX Gyre Heros (sans), dan TeX Gyre Cursor (kode), dengan lisensi "
                        "GUST Font License; diagram TikZ memakai newtx (LPPL)",
        "docx": "reference-b5-windows.docx",
    },
    "crc": {
        "nama": "Latin Modern / Computer Modern (Chapman & Hall/CRC krantz.cls) + Source Code Pro",
        "main": "Latin Modern Roman", "sans": "Latin Modern Sans",
        "math": "Latin Modern Math", "mono": "Source Code Pro", "skala_mono": 0.8, "lebar_mono": 0.6,
        "cadangan_main": ["latinmodern-math.otf"],
        "cadangan_mono": ["latinmodern-math.otf"],
        "mono_lua": "SourceCodePro",
        "otf": {"regular": "lmroman10-regular.otf", "italic": "lmroman10-italic.otf",
                "bold": "lmroman10-bold.otf", "bolditalic": "lmroman10-bolditalic.otf",
                "math": "latinmodern-math.otf"},
        "mathtext_cadangan": "cm",
        "tikz": ["\\usepackage[T1]{fontenc}", "\\usepackage{lmodern}"],
        # Cm*: Computer Modern BaKoMa matplotlib (mathtext cadangan "cm"), leluhur Latin Modern
        "izin": ["LMRoman", "LMSans", "LMMono", "LMMath", "LatinModern", "SourceCodePro",
                 "Cmr", "Cmmi", "Cmsy", "Cmex", "CMR", "CMMI", "CMSY", "CMEX"],
        "fon_hakcipta": "Latin Modern Roman (teks, judul, dan gambar) dan Latin Modern Math "
                        "(matematika) dengan lisensi GUST Font License, serta Source Code Pro (kode) "
                        "dengan lisensi SIL Open Font License 1.1",
        "docx": "reference-b5.docx",
    },
    "stix": {
        "nama": "STIX Two Text/Math + Source Code Pro",
        "main": "STIX Two Text", "sans": "STIX Two Text",
        "math": "STIX Two Math", "mono": "Source Code Pro", "skala_mono": 0.8, "lebar_mono": 0.6,
        "cadangan_main": ["STIXTwoMath-Regular.otf"],
        "cadangan_mono": ["STIXTwoText-Regular.otf", "STIXTwoMath-Regular.otf"],
        "mono_lua": "SourceCodePro",
        "otf": {"regular": "STIXTwoText-Regular.otf", "italic": "STIXTwoText-Italic.otf",
                "bold": "STIXTwoText-Bold.otf", "bolditalic": "STIXTwoText-BoldItalic.otf",
                "math": "STIXTwoMath-Regular.otf"},
        "mathtext_cadangan": "stix",
        "tikz": ["\\usepackage[T1]{fontenc}", "\\usepackage{stix2}"],
        "izin": ["STIXTwo", "SourceCodePro"],
        "fon_hakcipta": "STIX Two Text (teks, judul, dan gambar), STIX Two Math (matematika), dan "
                        "Source Code Pro (kode), dengan lisensi SIL Open Font License 1.1",
        "docx": "reference-b5.docx",
    },
}
BAWAAN = "libertinus"
DOCX_WINDOWS = "reference-b5-windows.docx"
CATATAN_OPSI = ("Wiley: huruf Wiley-AuthoringTemplate.sty tidak dapat dipastikan; pakai 'springer' "
                "(Times) sementara dan konfirmasikan ke editor Wiley.")

# Profil penerbit (kunci "profil" di konfig.json, bawaan "seri"): ukuran huruf
# dasar, spasi baris, dan blok teks penerbit bila terbaca dari berkas kelas.
# Angka yang tidak terbaca dari sumber ditandai belum terverifikasi
# (references/aturan-gaya-dan-tampilan.md, "Huruf dan templat penerbit").
PROFIL = {
    "seri": {"nama": "seri (12 pt, spasi 1,1; kolom dari ukuran buku)", "pt": 12, "linestretch": 1.1},
    # krantz.cls: \ExecuteOptions{letterpaper,10pt,...}; krantz1: \textwidth
    # 28pc + .5pt, \textheight 45pc + 3pt (\trimwidth 6in, \trimheight 9in).
    "crc": {"nama": "Chapman & Hall/CRC krantz1 (10 pt, blok teks 28pc × 45pc; pasangkan ukuran 6x9)",
            "pt": 10, "linestretch": 1.0, "blok_teks": ("336.5pt", "543pt")},
    # SNmono/svmono tidak ada di TeX Live; templat tidak memberi opsi ukuran:
    # 10 pt bawaan kelas belum terverifikasi; blok teks dari ukuran buku.
    "springer": {"nama": "Springer Nature SNmono (10 pt belum terverifikasi; blok teks dari ukuran buku)",
                 "pt": 10, "linestretch": 1.0},
    # Templat Overleaf Wiley: \documentclass[11pt]{book}; trim tidak diketahui.
    "wiley": {"nama": "Wiley (11 pt dari \\documentclass[11pt]{book}; trim belum diketahui)",
              "pt": 11, "linestretch": 1.0},
}
PROFIL_BAWAAN = "seri"

# Ukuran buku (kunci "ukuran"): kertas dan margin bawaan dalam mm
# (dalam/inner, luar/outer, atas, bawah). Sumber dan status: aturan-gaya.
UKURAN = {
    "b5": {"nama": "B5 176 × 250 mm (bawaan seri)", "kertas": (176, 250), "margin": (28, 28, 22, 24)},
    # Pedoman LPPM Unsoed: kiri 3 cm, kanan 2 cm, atas 3 cm, bawah 2 cm.
    "unesco": {"nama": "UNESCO 155 × 230 mm (LPPM Unsoed; Deepublish)", "kertas": (155, 230),
               "margin": (30, 20, 30, 20)},
    "a5": {"nama": "A5 148 × 210 mm (margin bawaan skill)", "kertas": (148, 210), "margin": (18, 15, 18, 20)},
    "a4": {"nama": "A4 210 × 297 mm (margin bawaan skill)", "kertas": (210, 297), "margin": (30, 30, 25, 25)},
    # 6 × 9 in: \trimwidth/\trimheight krantz.cls; margin = blok krantz1 di tengah.
    "6x9": {"nama": "6 × 9 in, 152,4 × 228,6 mm (krantz.cls)", "kertas": (152.4, 228.6),
            "margin": (17, 17, 19, 19)},
    # 7 × 10 in: belum terverifikasi (krantz.cls hanya menyatakan 6 × 9 in); blok
    # krantz2 33pc × 51pc di tengah.
    "7x10": {"nama": "7 × 10 in, 177,8 × 254 mm (krantz2; belum terverifikasi)", "kertas": (177.8, 254),
             "margin": (19, 19, 19, 19)},
}
UKURAN_BAWAAN = "b5"
MM = 72.27 / 25.4            # pt TeX per mm
BANTALAN_KODE = 8.2          # pt: garis kiri 2 pt + bantalan 1,4 mm + 0,6 mm + 0,5 pt
MONO_MIN = 6.8               # pt: di bawah ini tawarkan batas baris lebih kecil
BATAS_BAWAAN = {"batas_kode": 72, "batas_keluaran": 78}


def baca_konfig(akar):
    """Kunci huruf, profil, ukuran, docx_huruf, dan batas baris dari
    <akar>/harness/konfig.json."""
    berkas = Path(akar) / "harness" / "konfig.json"
    k = json.loads(berkas.read_text(encoding="utf-8")) if berkas.exists() else {}
    return {"huruf": k.get("huruf", BAWAAN), "profil": k.get("profil", PROFIL_BAWAAN),
            "ukuran": k.get("ukuran", UKURAN_BAWAAN), "docx_huruf": k.get("docx_huruf", ""),
            "batas_kode": int(k.get("batas_kode", 72)), "batas_keluaran": int(k.get("batas_keluaran", 78))}


def opsi(nama):
    if nama not in OPSI:
        raise SystemExit(f"opsi huruf '{nama}' tidak dikenal; pilih {', '.join(OPSI)}. {CATATAN_OPSI}")
    return OPSI[nama]


def profil(nama):
    if nama not in PROFIL:
        raise SystemExit(f"profil '{nama}' tidak dikenal; pilih {', '.join(PROFIL)}")
    return PROFIL[nama]


def ukuran(nama):
    if nama not in UKURAN:
        raise SystemExit(f"ukuran '{nama}' tidak dikenal; pilih {', '.join(UKURAN)}")
    return UKURAN[nama]


def _pt_dari(teks):
    m = re.match(r"([\d.]+)(pt|mm)", teks)
    return float(m.group(1)) * (MM if m.group(2) == "mm" else 1)


def tata_letak(nama, nama_profil=PROFIL_BAWAAN, nama_ukuran=UKURAN_BAWAAN, batas_kode=72, batas_keluaran=78):
    """Geometri, lebar kolom (pt), dan ukuran mono kode/keluaran (pt) yang
    membuat batas_kode karakter (dengan bantalan kotak) dan batas_keluaran
    karakter muat di kolom. Ukuran mono dibatasi 0,8 × huruf dasar."""
    o, pr, uk = opsi(nama), profil(nama_profil), ukuran(nama_ukuran)
    lebar, tinggi = uk["kertas"]
    geo = [f"paperwidth={lebar}mm", f"paperheight={tinggi}mm"]
    if "blok_teks" in pr:
        geo += [f"textwidth={pr['blok_teks'][0]}", f"textheight={pr['blok_teks'][1]}",
                "hcentering", "vcentering"]
        kolom = _pt_dari(pr["blok_teks"][0])
    else:
        dalam, luar, atas, bawah = uk["margin"]
        geo += [f"inner={dalam}mm", f"outer={luar}mm", f"top={atas}mm", f"bottom={bawah}mm"]
        kolom = (lebar - dalam - luar) * MM
    w = o["lebar_mono"]
    def turun(x):
        return int(x * 20) / 20
    batas_atas = 0.8 * pr["pt"]
    kode = min(turun((kolom - BANTALAN_KODE) / (batas_kode * w)), batas_atas)
    keluaran = min(turun((kolom - 0.5) / (batas_keluaran * w)), batas_atas)
    saran = []
    if min(kode, keluaran) < MONO_MIN:
        bk = min(batas_kode, int((kolom - BANTALAN_KODE) / (MONO_MIN * w)))
        bo = min(batas_keluaran, int((kolom - 0.5) / (MONO_MIN * w)))
        saran.append(f"mono kode {kode} pt / keluaran {keluaran} pt di bawah {MONO_MIN} pt; pilih: "
                     f"(a) batas_kode {bk} dan batas_keluaran {bo} di konfig.json (G-LEBAR-KODE, "
                     f"options(width = {bo - 3})), atau (b) terima mono kecil")
    return {"geometri": geo, "kolom_pt": kolom, "kolom_mm": kolom / MM, "kode_pt": kode,
            "keluaran_pt": keluaran, "saran": saran}


def dari_berkas(nama_otf):
    return f"file:{nama_otf}:mode=node;"


def nama_docx(nama, nama_profil, docx_huruf="", nama_ukuran=UKURAN_BAWAAN):
    """(nama berkas reference-doc, windows?, pt): reference-<ukuran>[-windows][-Npt].docx."""
    windows = docx_huruf == "windows" or opsi(nama)["docx"] == DOCX_WINDOWS
    pt = profil(nama_profil)["pt"]
    ukuran(nama_ukuran)
    dasar = f"reference-{nama_ukuran}" + ("-windows" if windows else "")
    return dasar + ("" if pt == 12 else f"-{pt}pt") + ".docx", windows, pt


def blok(nama, nama_profil=PROFIL_BAWAAN, docx_huruf="", nama_ukuran=UKURAN_BAWAAN,
         batas_kode=72, batas_keluaran=78):
    """Isi blok bertanda untuk setiap berkas (tanpa baris penanda)."""
    o, pr = opsi(nama), profil(nama_profil)
    tl = tata_letak(nama, nama_profil, nama_ukuran, batas_kode, batas_keluaran)
    yml = [f"mainfont: {o['main']}"]
    yml += [f"sansfont: {o['sans']}", f"mathfont: {o['math']}", f"monofont: {o['mono']}",
            f"monofontoptions: [Scale={o['skala_mono']}]"]
    yml_profil = [f"# kolom {tl['kolom_mm']:.1f} mm; mono kode {tl['kode_pt']} pt "
                  f"({batas_kode} karakter), keluaran {tl['keluaran_pt']} pt ({batas_keluaran} karakter)",
                  "geometry:"] + [f"  - {g}" for g in tl["geometri"]]
    yml_profil += [f"fontsize: {pr['pt']}pt", f"linestretch: {pr['linestretch']}"]
    lua = []
    if o["cadangan_main"]:
        lua.append('\\directlua{luaotfload.add_fallback("serimain", {'
                   + ", ".join(f'"{dari_berkas(f)}"' for f in o["cadangan_main"]) + "})}")
    lua.append('\\directlua{luaotfload.add_fallback("serimono", {'
               + ", ".join(f'"{dari_berkas(f)}"' for f in o["cadangan_mono"]) + "})}")
    # Cadangan huruf teks dipasang di preamble: Pandoc meloloskan kurung
    # kurawal mainfontoptions sehingga RawFeature={...} tidak sah di _quarto.yml.
    # Babel (lang: id-ID) memasang huruf teks lewat \\babelfont{rm} saat bahasa
    # dipilih, sehingga \\setmainfont saja ditimpa.
    pre = ([f"\\ifdefined\\directlua\\ifdefined\\babelfont"
            f"\\babelfont{{rm}}[RawFeature={{fallback=serimain}}]{{{o['main']}}}"
            f"\\else\\setmainfont{{{o['main']}}}[RawFeature={{fallback=serimain}}]\\fi\\fi"]
           if o["cadangan_main"] else [])
    pre += [f"\\ifdefined\\directlua\\setmonofont{{{o['mono']}}}[Scale={o['skala_mono']},"
           f"RawFeature={{fallback=serimono}}]\\fi",
           f"\\ifdefined\\directlua\\directlua{{seri_mono_nama = \"{o['mono_lua']}\"}}\\fi"]
    s = o["skala_mono"]
    k1, o1 = round(tl["kode_pt"] / s, 2), round(tl["keluaran_pt"] / s, 2)
    pre_profil = [f"% {nama_ukuran}, profil {nama_profil}: kolom {tl['kolom_mm']:.1f} mm; "
                  f"kode {tl['kode_pt']} pt, keluaran {tl['keluaran_pt']} pt (nominal x Scale {s})",
                  f"\\newcommand{{\\kodekecil}}{{\\fontsize{{{k1}pt}}{{{round(k1 * 1.2, 2)}pt}}\\selectfont}}",
                  f"\\newcommand{{\\keluarankecil}}{{\\fontsize{{{o1}pt}}{{{round(o1 * 1.2, 2)}pt}}\\selectfont}}"]
    hak = [f"\\providecommand{{\\serifon}}{{{o['fon_hakcipta']}}}"]
    return {"yml": yml, "yml_profil": yml_profil, "lua": lua, "pre": pre, "pre_profil": pre_profil,
            "tikz": o["tikz"], "hak": hak, "docx": nama_docx(nama, nama_profil, docx_huruf, nama_ukuran)[0],
            "tata_letak": tl}


def ganti_blok(teks, isi, komentar, indent="", tanda="huruf"):
    k = re.escape(komentar)
    pola = re.compile(rf"(^[ \t]*{k} >>> {tanda}\b[^\n]*\n).*?(^[ \t]*{k} <<< {tanda}\b)", re.S | re.M)
    if not pola.search(teks):
        return teks, False
    baru = "".join(indent + b + "\n" for b in isi)
    return pola.sub(lambda m: m.group(1) + baru + m.group(2), teks, count=1), True


# ---------------------------------------------------------------- gaya Word
def buat_docx(sumber, tujuan, windows=False, pt=12, nama_ukuran=UKURAN_BAWAAN):
    """Salin reference-b5.docx; windows=True: semua gaya Times New Roman (teks,
    judul), Courier New (kode), Cambria Math (rumus OMML); pt: ukuran dasar
    profil (semua w:sz diskalakan pt/12); ukuran selain b5: w:pgSz dan w:pgMar
    dari kertas dan margin ukuran itu. Menjorok, spasi, dan id-ID tetap."""
    import zipfile
    faktor = pt / 12
    uk = ukuran(nama_ukuran)
    twip = 1440 / 25.4

    def halaman(s):
        if nama_ukuran == "b5":
            return s
        (lebar, tinggi), (dalam, luar, atas, bawah) = uk["kertas"], uk["margin"]
        s = re.sub(r'<w:pgSz w:w="\d+" w:h="\d+"/>',
                   f'<w:pgSz w:w="{round(lebar * twip)}" w:h="{round(tinggi * twip)}"/>', s)
        return re.sub(r'<w:pgMar [^>]*/>',
                      f'<w:pgMar w:left="{round(dalam * twip)}" w:right="{round(luar * twip)}" '
                      f'w:top="{round(atas * twip)}" w:bottom="{round(bawah * twip)}"/>', s)

    def skala(m):
        return f'{m.group(1)}"{max(2, round(int(m.group(2)) * faktor))}"'

    def rfonts(m):
        nama = "Courier New" if "Mono" in m.group(0) else "Times New Roman"
        return (f'<w:rFonts w:ascii="{nama}" w:hAnsi="{nama}" w:cs="{nama}" '
                f'w:eastAsia="{nama}"/>')

    with zipfile.ZipFile(sumber) as zin, zipfile.ZipFile(tujuan, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith(".xml"):
                s = data.decode("utf-8")
                if item.filename == "word/document.xml":
                    s = halaman(s)
                if item.filename == "word/styles.xml" and faktor != 1:
                    s = re.sub(r'(<w:szC?s? w:val=)"(\d+)"', skala, s)
                if windows:
                    if item.filename == "word/styles.xml":
                        s = re.sub(r"<w:rFonts\b[^>]*/>", rfonts, s)
                    s = s.replace("Libertinus Serif", "Times New Roman")
                    s = s.replace("Libertinus Mono", "Courier New")
                    s = s.replace("Libertinus Math", "Cambria Math")
                data = s.encode("utf-8")
            zout.writestr(item, data)


# ---------------------------------------------------------------- terapkan
def terapkan(proyek, bukus, nama=None, nama_profil=None, docx_huruf=None, nama_ukuran=None):
    """Tulis ulang blok huruf/profil di proyek; kembalikan berkas yang diubah."""
    P = Path(proyek)
    k = baca_konfig(P)
    nama = nama or k["huruf"]
    nama_profil = nama_profil or k["profil"]
    nama_ukuran = nama_ukuran or k["ukuran"]
    docx_huruf = k["docx_huruf"] if docx_huruf is None else docx_huruf
    b = blok(nama, nama_profil, docx_huruf, nama_ukuran, k["batas_kode"], k["batas_keluaran"])
    tl = b["tata_letak"]
    print(f"  {nama}, profil {nama_profil}, ukuran {nama_ukuran}: kolom {tl['kolom_mm']:.1f} mm, "
          f"kode {tl['kode_pt']} pt ({k['batas_kode']} karakter), keluaran {tl['keluaran_pt']} pt "
          f"({k['batas_keluaran']} karakter)")
    for s in tl["saran"]:
        print(f"  saran: {s}")
    diubah = []
    rencana = [(P / "_bersama" / "doc-class.tex", [("lua", "$--", "", "huruf")]),
               (P / "_bersama" / "preamble.tex", [("pre", "%", "", "huruf"),
                                                  ("pre_profil", "%", "", "profil")]),
               (P / "_bersama" / "tikz-preamble.tex", [("tikz", "%", "", "huruf")]),
               (P / "_bersama" / "hak-cipta.tex", [("hak", "%", "", "huruf")])]
    for buku in bukus:
        rencana.append((P / buku / "_quarto.yml", [("yml", "#", "    ", "huruf"),
                                                   ("yml_profil", "#", "    ", "profil")]))
    for berkas, bloks in rencana:
        if not berkas.exists():
            print(f"  peringatan: {berkas} tidak ada")
            continue
        teks = berkas.read_text(encoding="utf-8")
        baru = teks
        for kunci, kom, ind, tanda in bloks:
            baru, ada = ganti_blok(baru, b[kunci], kom, ind, tanda)
            if not ada:
                print(f"  peringatan: penanda '>>> {tanda}' tidak ada di {berkas}")
        if berkas.name == "_quarto.yml":
            baru = re.sub(r"(reference-doc:\s*\S*?/)reference-b5[\w-]*\.docx", rf"\g<1>{b['docx']}", baru)
            baru = re.sub(r"(# >>> huruf)[^\n]*", rf"\1: {nama} (dibangkitkan _bersama/huruf.py dari "
                          r"harness/konfig.json)", baru, count=1)
            baru = re.sub(r"(# >>> profil)[^\n]*", rf"\1: {nama_profil}, ukuran {nama_ukuran} "
                          r"(dibangkitkan _bersama/huruf.py)", baru, count=1)
        if baru != teks:
            berkas.write_text(baru, encoding="utf-8")
            diubah.append(str(berkas))
    # Lebar keluaran R (knitr) = batas_keluaran - 3 (awalan "## "): .Rprofile buku
    for buku in bukus:
        rp = P / buku / ".Rprofile"
        lama = rp.read_text(encoding="utf-8") if rp.exists() else ""
        baris = f"options(width = {k['batas_keluaran'] - 3})  # huruf.py: batas_keluaran - 3"
        baru = re.sub(r"^options\(width = \d+\)  # huruf\.py[^\n]*$", baris, lama, flags=re.M)
        if baru == lama and baris not in lama:
            baru = lama + ("" if not lama or lama.endswith("\n") else "\n") + baris + "\n"
        if baru != lama:
            rp.write_text(baru, encoding="utf-8")
            diubah.append(str(rp))
    berkas_docx, windows, pt = nama_docx(nama, nama_profil, docx_huruf, nama_ukuran)
    tujuan = P / "_bersama" / berkas_docx
    sumber = P / "_bersama" / "reference-b5.docx"
    if sumber.exists() and tujuan != sumber and not tujuan.exists():
        buat_docx(sumber, tujuan, windows, pt, nama_ukuran)
        diubah.append(str(tujuan))
    return diubah


# ---------------------------------------------------------------- rumus Word
def fon_rumus_docx(nama, docx_huruf=""):
    """Fon rumus OMML di Word: Cambria Math untuk gaya Word Windows, selain itu
    huruf matematika opsi."""
    o = opsi(nama)
    return "Cambria Math" if docx_huruf == "windows" or o["docx"] == DOCX_WINDOWS else o["math"]


def pasang_fon_rumus(docx, fon):
    """Tulis <m:mathPr><m:mathFont m:val=fon/></m:mathPr> di word/settings.xml.
    Pandoc tidak menyalin m:mathPr dari reference-doc, jadi tanpa langkah ini
    Word memakai fon rumus bawaannya."""
    import shutil
    import tempfile
    import zipfile
    docx = Path(docx)
    with zipfile.ZipFile(docx) as zin:
        isi = {i.filename: (i, zin.read(i.filename)) for i in zin.infolist()}
    info, data = isi["word/settings.xml"]
    s = data.decode("utf-8")
    if 'xmlns:m="' not in re.search(r"<w:settings\b[^>]*>", s).group(0):
        s = re.sub(r"(<w:settings\b)", r'\1 xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"',
                   s, count=1)
    s = re.sub(r"<m:mathPr>.*?</m:mathPr>|<m:mathPr/>", "", s, flags=re.S)
    # urutan skema CT_Settings: m:mathPr sesudah w:rsids, sebelum w:themeFontLang dst.
    sisip = f'<m:mathPr><m:mathFont m:val="{fon}"/></m:mathPr>'
    m = re.search(r"<w:(?:attachedSchema|themeFontLang|clrSchemeMapping|doNotIncludeSubdocsInStats|"
                  r"doNotAutoCompressPictures|forceUpgrade|captions|readModeInkLockDown|smartTagType|"
                  r"shapeDefaults|doNotEmbedSmartTags|decimalSymbol|listSeparator)\b", s)
    s = s[:m.start()] + sisip + s[m.start():] if m else s.replace("</w:settings>", sisip + "</w:settings>")
    isi["word/settings.xml"] = (info, s.encode("utf-8"))
    sementara = Path(tempfile.mkstemp(suffix=".docx", dir=docx.parent)[1])
    with zipfile.ZipFile(sementara, "w", zipfile.ZIP_DEFLATED) as zout:
        for nama, (inf, dat) in isi.items():
            zout.writestr(inf, dat)
    shutil.move(sementara, docx)


def pasca_render(folder_buku="."):
    """Langkah post-render Quarto (_quarto.yml project.post-render): pasang fon
    rumus Word di setiap DOCX _book/ menurut konfig.json."""
    buku = Path(folder_buku).resolve()
    k = baca_konfig(buku.parent)
    fon = fon_rumus_docx(k["huruf"], k["docx_huruf"])
    for docx in sorted((buku / "_book").glob("*.docx")):
        pasang_fon_rumus(docx, fon)
        print(f"  huruf.py: m:mathFont {fon} -> {docx.name}")


# ---------------------------------------------------------------- G-HURUF
def nama_pdffonts(pdf):
    """Nama huruf tersemat (tanpa awalan subset ABCDEF+) dari pdffonts."""
    import subprocess
    keluar = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True,
                            errors="replace").stdout.splitlines()[2:]
    return {re.sub(r"^[A-Z]{6}\+", "", b.split()[0]) for b in keluar if b.strip()}


def huruf_asing(pdf, nama_opsi):
    izin = opsi(nama_opsi)["izin"]
    return sorted(n for n in nama_pdffonts(pdf) if not any(n.startswith(p) for p in izin))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--proyek", default=".")
    ap.add_argument("--buku", action="append", default=[], help="folder buku (boleh berulang)")
    ap.add_argument("--huruf", help=f"opsi huruf: {', '.join(OPSI)} (bawaan: konfig.json)")
    ap.add_argument("--profil", help=f"profil ukuran: {', '.join(PROFIL)} (bawaan: konfig.json)")
    ap.add_argument("--ukuran", help="ukuran buku: " + ", ".join(UKURAN) + " (bawaan: konfig.json)")
    ap.add_argument("--docx-huruf", choices=["", "windows"], help="gaya Word huruf Windows")
    ap.add_argument("--daftar", action="store_true", help="tampilkan opsi dan profil")
    ap.add_argument("--buat-docx", nargs=2, metavar=("SUMBER", "TUJUAN"),
                    help="bangkitkan gaya Word Windows (pakai --profil untuk ukuran)")
    ap.add_argument("--pasca-render", action="store_true",
                    help="post-render Quarto: pasang m:mathFont di DOCX _book/ (dijalankan dari folder buku)")
    a = ap.parse_args()
    if a.pasca_render:
        pasca_render(".")
        return
    if a.daftar:
        for n, o in OPSI.items():
            print(f"{n:11s} {o['nama']}\n            main {o['main']}, sans {o['sans']}, math {o['math']}, "
                  f"mono {o['mono']} (Scale={o['skala_mono']}), Word {o['docx']}")
        print(CATATAN_OPSI)
        for n, pr in PROFIL.items():
            print(f"profil {n:9s} {pr['nama']}")
        for n, uk in UKURAN.items():
            tl = tata_letak(BAWAAN, PROFIL_BAWAAN, n)
            print(f"ukuran {n:7s} {uk['nama']}; kolom {tl['kolom_mm']:.1f} mm, Libertinus Mono 12 pt: "
                  f"kode {tl['kode_pt']} pt, keluaran {tl['keluaran_pt']} pt")
        return
    if a.buat_docx:
        buat_docx(a.buat_docx[0], a.buat_docx[1], True, profil(a.profil or PROFIL_BAWAAN)["pt"],
                  a.ukuran or UKURAN_BAWAAN)
        return
    kb = Path(a.proyek) / "harness" / "konfig.json"
    ubah = {kunci: nilai for kunci, nilai in [("huruf", a.huruf), ("profil", a.profil),
                                               ("ukuran", a.ukuran), ("docx_huruf", a.docx_huruf)]
            if nilai is not None}
    if a.ukuran:
        ukuran(a.ukuran)
    if a.huruf:
        opsi(a.huruf)
    if a.profil:
        profil(a.profil)
    if ubah and kb.exists():
        k = json.loads(kb.read_text(encoding="utf-8"))
        k.update(ubah)
        kb.write_text(json.dumps(k, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"  konfig: {ubah} ({kb})")
    for f in terapkan(a.proyek, a.buku, a.huruf, a.profil, a.docx_huruf, a.ukuran):
        print(f"  diubah: {f}")


if __name__ == "__main__":
    main()
