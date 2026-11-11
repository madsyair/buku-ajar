#!/usr/bin/env python3
"""Keselarasan angka tabel–narasi (G-SELARAS, prototipe 2026-11-11).

Mencari pasangan angka yang merupakan NILAI SAMA tetapi ditulis dengan JUMLAH
DESIMAL BERBEDA di tabel dan di prosa yang merujuk tabel itu, misalnya tabel
0,254 dan narasi 0,25. Sumber angka:

- tabel: sel tabel pipa di <buku>/build/<bab>.knit.md (hasil kable); label
  tabel diambil dari urutan chunk `#| label: tbl-...` di .qmd (knitr membuang
  opsi #| dari keluaran, tetapi urutannya tetap). Tanpa knit.md, hanya tabel
  pipa yang ditulis langsung di .qmd yang dibaca;
- prosa: paragraf hasil rajut. Paragraf .qmd yang memuat R inline dicocokkan
  dengan paragraf rajutannya sehingga setiap angka hasil `r angka(x, d)` dikenali
  beserta ekspresi dan d-nya. Paragraf yang tidak cocok (naskah .qmd sudah
  disunting sesudah dirajut) tetap diperiksa, tetapi hanya angka berdesimal.

Heuristik pasangan: kedua angka sama setelah angka yang lebih rinci dibulatkan
ke jumlah desimal yang lebih sedikit (pembulatan setengah ke dua arah diterima),
angka yang lebih kasar bukan nol, dan paragrafnya merujuk @tbl-<label> tabel
itu atau berjarak paling jauh JENDELA blok dari tabelnya tanpa merujuk tabel
lain. Angka prosa yang sama persis dengan salah satu sel tabel (desimal sama)
dianggap sudah selaras dan tidak dipasangkan lagi.

Pemakaian:
  python3 harness/selaras_angka.py                       # semua buku
  python3 harness/selaras_angka.py --buku buku2-stan --bab bab05
  python3 harness/selaras_angka.py --md laporan.md --json laporan.json
  python3 harness/selaras_angka.py --qmd x.qmd --knit build/x.knit.md   # satu berkas
Keluaran berstatus 0 kecuali --ketat dan ada temuan.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
# Buku = folder proyek yang memuat _quarto.yml (seri ini: tiga buku dan tiga kunci).
BUKU = sorted(p.parent.name for p in AKAR.glob("*/_quarto.yml"))
JENDELA = 2  # blok prosa sebelum/sesudah tabel yang dianggap "berdekatan"

# ------------------------------------------------------------------ angka
# Prosa seri: koma desimal, titik pemisah ribuan, minus "−" (U+2212).
POLA_ID = re.compile(r"(?<![\w.,])([−-]?)(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d+))?(?![\w]|,\d|\.\d)(\s?%)?")
POLA_TITIK = re.compile(r"(?<![\w.,])([−-]?)(\d+)\.(\d+)(?![\w.])(\s?%)?")


class Angka:
    __slots__ = ("nilai", "desimal", "teks", "persen")

    def __init__(self, nilai, desimal, teks, persen):
        self.nilai, self.desimal, self.teks, self.persen = nilai, desimal, teks, persen

    def __repr__(self):
        return self.teks


def angka_dalam(teks, titik_desimal=False):
    """Daftar Angka di teks. titik_desimal=True untuk tabel kable tanpa
    decimal.mark = "," (0.254)."""
    keluar = []
    if titik_desimal:
        for m in POLA_TITIK.finditer(teks):
            s, bulat, frak, pc = m.groups()
            keluar.append(Angka(Decimal(("-" if s else "") + bulat + "." + frak), len(frak),
                                m.group(0).strip(), bool(pc)))
    for m in POLA_ID.finditer(teks):
        s, bulat, frak, pc = m.groups()
        if titik_desimal and frak is None and "." in bulat:
            continue  # sudah dibaca sebagai titik desimal
        v = bulat.replace(".", "") + ("." + frak if frak else "")
        keluar.append(Angka(Decimal(("-" if s else "") + v), len(frak or ""),
                            m.group(0).strip(), bool(pc)))
    return keluar


def bulat(x, d, arah):
    q = Decimal(1).scaleb(-d)
    return x.quantize(q, rounding=arah)


def sama_dibulatkan(halus, kasar):
    """halus (lebih banyak desimal) dibulatkan ke desimal kasar sama dengan kasar."""
    d = kasar.desimal
    return any(bulat(halus.nilai, d, a) == kasar.nilai for a in (ROUND_HALF_UP, ROUND_HALF_DOWN))


# ------------------------------------------------------------------ pemilahan
POLA_PAGAR = re.compile(r"^\s*(```|~~~)")
POLA_PEMISAH = re.compile(r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$")


def blok_md(teks):
    """Pecah markdown menjadi blok: ('tabel', baris, [baris...]) atau
    ('prosa', baris, teks). Kode berpagar, judul, dan YAML dilewati."""
    baris = teks.splitlines()
    i, n = 0, len(baris)
    if n and baris[0].strip() == "---":
        i = 1
        while i < n and baris[i].strip() != "---":
            i += 1
        i += 1
    blok, buf, awal = [], [], 0

    def tutup():
        nonlocal buf
        if buf:
            blok.append(("prosa", awal, " ".join(b.strip() for b in buf)))
        buf = []

    while i < n:
        b = baris[i]
        if POLA_PAGAR.match(b):
            tutup()
            pagar = POLA_PAGAR.match(b).group(1)
            i += 1
            while i < n and not baris[i].strip().startswith(pagar):
                i += 1
            i += 1
            continue
        if b.lstrip().startswith("|") and i + 1 < n and POLA_PEMISAH.match(baris[i + 1]) \
                and "-" in baris[i + 1]:
            tutup()
            j = i
            while j < n and baris[j].lstrip().startswith("|"):
                j += 1
            blok.append(("tabel", i + 1, baris[i:j]))
            i = j
            continue
        if not b.strip() or b.startswith("#") or b.strip().startswith(":::"):
            tutup()
            i += 1
            continue
        if not buf:
            awal = i + 1
        buf.append(b)
        i += 1
    tutup()
    return blok


def sel_tabel(baris):
    """(kepala, [[sel...]...]) dari baris tabel pipa."""
    pecah = lambda b: [s.strip() for s in b.strip().strip("|").split("|")]
    kepala = pecah(baris[0])
    isi = [pecah(b) for b in baris[2:]]
    return kepala, isi


def sel_data(sel):
    """Sel data: setelah angka dibuang, sisa teksnya pendek (satuan, %, Rp,
    kurung selang), bukan kalimat rubrik atau keterangan."""
    sisa = re.sub(r"[−-]?\d[\d.,]*", "", sel)
    sisa = re.sub(r"[\s%;()\[\]$*\\]", "", sisa)
    return len(sisa) <= 12


def label_tabel_qmd(qmd_teks):
    """Label tbl- chunk dalam urutan, dan baris kepala tabel pipa prosa di .qmd
    (tabel yang ditulis langsung, untuk dikenali di knit.md)."""
    label = re.findall(r"^#\|\s*label:\s*(tbl-[\w-]+)", qmd_teks, flags=re.M)
    tanpa_kode = re.sub(r"^```\{.*?^```", "", qmd_teks, flags=re.S | re.M)
    kepala = []
    for jenis, _, isi in blok_md(tanpa_kode):
        if jenis == "tabel":
            m = re.search(r"\{#(tbl-[\w-]+)\}", tanpa_kode)
            kepala.append(isi[0].strip())
    return label, kepala


# ------------------------------------------------------------------ R inline
POLA_INLINE = re.compile(r"`r\s+([^`]+)`")
BAWAAN_D = {"angka": 2, "persen": 1, "selang": 3, "ilmiah": 1}


def argumen(expr):
    """Pecah panggilan f(a, b, d = 3) → (f, [argumen tingkat atas])."""
    m = re.match(r"\s*([\w.]+)\((.*)\)\s*$", expr, flags=re.S)
    if not m:
        return None, []
    f, isi = m.groups()
    arg, kedalaman, cur = [], 0, ""
    for c in isi:
        if c in "([{":
            kedalaman += 1
        elif c in ")]}":
            kedalaman -= 1
        if c == "," and kedalaman == 0:
            arg.append(cur.strip())
            cur = ""
        else:
            cur += c
    if cur.strip():
        arg.append(cur.strip())
    return f, arg


def d_inline(expr):
    f, arg = argumen(expr)
    if f not in BAWAAN_D:
        return f, None
    d = BAWAAN_D[f]
    for a in arg[1:]:
        m = re.match(r"(?:d\s*=\s*)?(\d+)$", a)
        if m:
            d = int(m.group(1))
    return f, d


def paragraf_qmd(qmd_teks):
    tanpa_kode = re.sub(r"^```\{.*?^```", "", qmd_teks, flags=re.S | re.M)
    return [t for j, _, t in blok_md(tanpa_kode) if j == "prosa"]


def templat(par):
    """Regex paragraf rajutan dari paragraf .qmd: R inline → grup tangkap."""
    potong = POLA_INLINE.split(par)
    literal, expr = potong[0::2], potong[1::2]
    bagian = []
    for k, lit in enumerate(literal):
        bagian.append(r"\s*".join(re.escape(w) for w in lit.split()) if lit.strip() else "")
        if k < len(expr):
            sp_kiri = r"\s*" if lit.endswith(" ") else ""
            bagian.append(sp_kiri + "(.+?)" + (r"\s*" if literal[k + 1].startswith(" ") else ""))
    return re.compile("^" + "".join(bagian) + "$", flags=re.S), expr


# ------------------------------------------------------------------ jenis besaran
JENIS = [  # (jenis, pola konteks); urutan menentukan prioritas
    ("R-hat", r"r[-_ ]?hat|\\hat\s*\{?r\}?|r̂|\brhat\b"),
    ("ESS", r"\bess\b|ess_bulk|ess_tail|ukuran sampel efektif|ess-"),
    ("MCSE", r"mcse|galat baku monte carlo|galat monte carlo"),
    ("E-BFMI", r"bfmi"),
    ("Pareto k", r"pareto|khat|\\hat\s*\{?k\}?|k̂|pareto_k"),
    ("SE elpd", r"se_diff|se_elpd|se elpd|galat baku selisih|\bse\b.*elpd|elpd.*\bse\b"),
    ("elpd", r"elpd|looic|p_loo|waic"),
    ("rasio odds/laju", r"rasio odds|odds ratio|rasio laju|\bor\b|\birr\b|exp\(b|exp\(beta|exp\(koef"),
    ("statistik uji / nilai-p", r"nilai-p|p-value|p_value|\bp\s*=|statistik uji|\bchi|\bt\s*="),
    ("persen", r"persen\(|\bpersen\b|persentase"),
    ("simpangan baku", r"\bsd\b|simpangan baku|sd_|sigma|\bmad\b"),
    ("koefisien", r"koefisien|\bb_|\bbeta\b|intersep|kemiringan|logit"),
    ("peluang/proporsi", r"peluang|proporsi|\bpr\(|\bp\(|mean\(.*[<>]|prob"),
    ("rasio (lain)", r"\brasio\b|kali lipat"),
    ("rupiah/jam/orang", r"rupiah|\brp\b|ribu|juta|\bjam\b|detik|orang|penduduk|rumah tangga"),
    ("ringkasan posterior", r"mean|median|rata|q5|q95|q2\.5|q97\.5|batas|interval|selang\(|kuantil|hdi|eti"),
]


def kenali_jenis(konteks):
    k = konteks.lower()
    for nama, pola in JENIS:
        if re.search(pola, k):
            return nama
    return "lain"


# ------------------------------------------------------------------ inti
def baca_bab(qmd, knit=None):
    """Kembalikan dict: tabel (label, baris, kepala, sel-angka), prosa (blok,
    angka, inline?), inline (expr, d, jenis dari .qmd)."""
    qmd_teks = qmd.read_text(encoding="utf-8")
    label, kepala_prosa = label_tabel_qmd(qmd_teks)
    sumber = knit if knit and knit.exists() else qmd
    teks = sumber.read_text(encoding="utf-8")
    if sumber == qmd:
        teks = re.sub(r"^```\{.*?^```", "", teks, flags=re.S | re.M)
    blok = blok_md(teks)
    tabel, prosa = [], []
    antre = list(label)
    for idx, (jenis, baris, isi) in enumerate(blok):
        if jenis == "tabel":
            kepala, sel = sel_tabel(isi)
            if sumber == knit and isi[0].strip() not in kepala_prosa and antre:
                lab = antre.pop(0)
            else:
                m = None
                lab = None
            titik = not any(re.search(r"\d,\d", c) for r in sel for c in r) and \
                any(re.search(r"\d\.\d", c) for r in sel for c in r)
            angka_sel = []
            for r in sel:
                for k, c in enumerate(r):
                    kol = kepala[k] if k < len(kepala) else ""
                    if not sel_data(c):
                        continue  # sel teks (rubrik, keterangan): angkanya bukan data
                    for a in angka_dalam(c, titik):
                        angka_sel.append((a, kol, r[0] if r else "", k))
            tabel.append({"idx": idx, "baris": baris, "label": lab, "kepala": kepala,
                          "angka": angka_sel})
        else:
            prosa.append({"idx": idx, "baris": baris, "teks": isi,
                          "rujuk": set(re.findall(r"@(tbl-[\w-]+)", isi))})
    # Pencocokan paragraf .qmd ↔ rajutan untuk angka hasil R inline
    inline_semua = []
    templ = []
    for par in paragraf_qmd(qmd_teks):
        if "`r " not in par:
            continue
        try:
            rx, expr = templat(par)
        except re.error:
            continue
        templ.append((rx, expr, par))
        for e in expr:
            f, d = d_inline(e)
            if d is not None:
                kiri = par[:par.find(e)][-60:]
                inline_semua.append({"expr": e, "fungsi": f, "d": d,
                                     "jenis": "persen" if f == "persen" else kenali_jenis(e + " " + kiri)})
    cocok = 0
    for p in prosa:
        p["inline"] = None
        if sumber != knit:
            continue
        for rx, expr, par in templ:
            m = rx.match(p["teks"])
            if m:
                p["inline"] = list(zip(expr, m.groups()))
                cocok += 1
                break
    # Angka prosa
    for p in prosa:
        daftar = []
        if p["inline"]:
            for e, keluaran in p["inline"]:
                f, d = d_inline(e)
                if d is None:
                    continue
                for a in angka_dalam(keluaran):
                    daftar.append((a, e))
        elif sumber == knit:
            teks_bersih = re.sub(r"@\w[\w-]*|\[@[^\]]*\]", " ", p["teks"])
            for a in angka_dalam(teks_bersih):
                if a.desimal > 0:
                    daftar.append((a, None))
        p["angka"] = daftar
    return {"tabel": tabel, "prosa": prosa, "inline": inline_semua,
            "sumber": str(sumber.relative_to(AKAR)) if AKAR in sumber.parents else str(sumber),
            "par_inline": len(templ), "par_cocok": cocok}


def temuan_bab(data, jendela=JENDELA):
    hasil, sudah = [], set()
    for t in data["tabel"]:
        if not t["angka"]:
            continue
        sel_teks = {(a.nilai, a.desimal, a.persen) for a, *_ in t["angka"]}
        for p in data["prosa"]:
            rujuk_ini = t["label"] and t["label"] in p["rujuk"]
            dekat = abs(p["idx"] - t["idx"]) <= jendela and not (p["rujuk"] - {t["label"]})
            if not (rujuk_ini or dekat):
                continue
            for a, expr in p["angka"]:
                if (a.nilai, a.desimal, a.persen) in sel_teks:
                    continue  # angka itu sendiri ada persis di tabel
                calon = []
                for c, kol, baris_lab, k in t["angka"]:
                    if c.persen != a.persen or c.desimal == a.desimal:
                        continue
                    halus, kasar = (c, a) if c.desimal > a.desimal else (a, c)
                    if kasar.nilai == 0 or kasar is c and c.desimal == 0:
                        continue
                    if kasar is a and a.desimal == 0 and (expr is None or abs(a.nilai) < 10):
                        continue
                    if sama_dibulatkan(halus, kasar):
                        calon.append((c, kol, baris_lab))
                if not calon:
                    continue
                c, kol, baris_lab = calon[0]
                jenis = "persen" if a.persen else kenali_jenis(f"{kol} {baris_lab}")
                if jenis == "lain" and expr:
                    jenis = kenali_jenis(expr)
                halus = c if c.desimal > a.desimal else a
                nol = set(halus.teks.rstrip("%").strip().split(",")[-1][min(c.desimal, a.desimal):]) <= {"0"}
                kunci = (t["label"], p["baris"], c.teks, a.teks)
                if kunci in sudah:
                    continue
                sudah.add(kunci)
                yakin = "tinggi" if rujuk_ini and len(calon) == 1 else "sedang"
                hasil.append({"label": t["label"] or f"tabel@{t['baris']}", "baris_tabel": t["baris"],
                              "baris_prosa": p["baris"], "tabel": c.teks, "d_tabel": c.desimal,
                              "prosa": a.teks, "d_prosa": a.desimal, "kolom": kol,
                              "baris": baris_lab, "expr": expr, "jenis": jenis,
                              "yakin": yakin, "calon": len(calon), "nol_belakang": nol,
                              "rujuk": bool(rujuk_ini)})
    return hasil


def sebaran_tabel(data):
    s = defaultdict(Counter)
    for t in data["tabel"]:
        for a, kol, baris_lab, k in t["angka"]:
            j = "persen" if a.persen else kenali_jenis(f"{kol} {baris_lab}")
            if a.desimal == 0 and j not in ("ESS", "rupiah/jam/orang", "persen"):
                continue  # bilangan bulat: nomor baris, cacahan, label
            s[j][a.desimal] += 1
    return s


def bab_buku(buku):
    d = AKAR / buku
    return sorted(p.stem for p in d.glob("*.qmd")
                  if p.stem not in ("references", "riwayat-penulis"))


def periksa(qmd, knit=None):
    """Antarmuka untuk harness: daftar temuan satu bab."""
    return temuan_bab(baca_bab(Path(qmd), Path(knit) if knit else None))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--buku", nargs="*", default=BUKU)
    ap.add_argument("--bab", nargs="*")
    ap.add_argument("--qmd")
    ap.add_argument("--knit")
    ap.add_argument("--md", help="tulis laporan markdown ke berkas ini")
    ap.add_argument("--json", help="tulis temuan JSON ke berkas ini")
    ap.add_argument("--ketat", action="store_true", help="status 1 bila ada temuan")
    a = ap.parse_args()

    if a.qmd:
        sasaran = [("-", Path(a.qmd).stem, Path(a.qmd), Path(a.knit) if a.knit else None)]
    else:
        sasaran = []
        for b in a.buku:
            for bab in (a.bab or bab_buku(b)):
                sasaran.append((b, bab, AKAR / b / f"{bab}.qmd", AKAR / b / "build" / f"{bab}.knit.md"))

    semua, per_buku, per_bab = [], Counter(), {}
    seb_prosa, seb_tabel = defaultdict(Counter), defaultdict(Counter)
    stat = Counter()
    for b, bab, qmd, knit in sasaran:
        if not qmd.exists():
            continue
        data = baca_bab(qmd, knit)
        tm = temuan_bab(data)
        for x in tm:
            x["buku"], x["bab"] = b, bab
        semua += tm
        per_buku[b] += len(tm)
        per_bab[(b, bab)] = (len(tm), sum(1 for x in tm if x["yakin"] == "tinggi"),
                             len(data["tabel"]), data["sumber"])
        stat["tabel"] += len(data["tabel"])
        stat["par_inline"] += data["par_inline"]
        stat["par_cocok"] += data["par_cocok"]
        for i in data["inline"]:
            seb_prosa[i["jenis"]][i["d"]] += 1
        for j, c in sebaran_tabel(data).items():
            seb_tabel[j].update(c)

    for x in semua:
        print(f"{x['buku']}/{x['bab']}: {x['label']} [{x['yakin']}] tabel {x['tabel']} "
              f"(d={x['d_tabel']}) ↔ prosa {x['prosa']} (d={x['d_prosa']}) "
              f"baris {x['baris_prosa']}; {x['jenis']}; kolom '{x['kolom']}'")
    print(f"\nTemuan: {len(semua)} ({sum(1 for x in semua if x['yakin'] == 'tinggi')} keyakinan tinggi) "
          f"dari {stat['tabel']} tabel; paragraf ber-R-inline cocok dengan rajutan "
          f"{stat['par_cocok']}/{stat['par_inline']}")
    for b in per_buku:
        print(f"  {b}: {per_buku[b]}")

    if a.md:
        L = ["# Inventaris ketidakselarasan desimal tabel–narasi", "",
             "Dibangkitkan oleh `harness/selaras_angka.py` dari `build/*.knit.md` (tabel kable) dan "
             "paragraf hasil rajut. Heuristik dan batasannya dijelaskan di kepala skrip.", "",
             f"- Tabel terbaca: {stat['tabel']}",
             f"- Paragraf .qmd ber-R-inline yang cocok dengan rajutannya: {stat['par_cocok']} dari "
             f"{stat['par_inline']} (sisanya disunting sesudah dirajut atau tidak ada di rajutan; "
             "angka berdesimalnya tetap diperiksa tanpa info d)",
             f"- Temuan: {len(semua)}, keyakinan tinggi (paragraf merujuk @tbl tabel itu dan hanya satu sel cocok): "
             f"{sum(1 for x in semua if x['yakin'] == 'tinggi')}", "",
             "## Per buku", "", "| Buku | Temuan | Keyakinan tinggi |", "|---|---:|---:|"]
        for b in dict.fromkeys(x[0] for x in sasaran):
            tb = [x for x in semua if x["buku"] == b]
            L.append(f"| {b} | {len(tb)} | {sum(1 for x in tb if x['yakin'] == 'tinggi')} |")
        L += ["", "## Per bab (hanya bab bertemuan)", "",
              "| Buku | Bab | Temuan | Tinggi | Tabel |", "|---|---|---:|---:|---:|"]
        for (b, bab), (n, nt, ntab, _) in per_bab.items():
            if n:
                L.append(f"| {b} | {bab} | {n} | {nt} | {ntab} |")
        L += ["", "## Pola selisih desimal (d tabel → d prosa)", "",
              "| d tabel | d prosa | Temuan |", "|---:|---:|---:|"]
        for (dt, dp), n in Counter((x["d_tabel"], x["d_prosa"]) for x in semua).most_common():
            L.append(f"| {dt} | {dp} | {n} |")
        L += ["", "## Temuan per jenis besaran", "", "| Jenis | Temuan |", "|---|---:|"]
        for j, n in Counter(x["jenis"] for x in semua).most_common():
            L.append(f"| {j} | {n} |")
        L += ["", "## Sebaran d di prosa (R inline di .qmd) per jenis besaran", "",
              "Jenis dikenali dari ekspresi R dan ±60 karakter sebelum R inline.", "",
              "| Jenis | " + " | ".join(f"d={d}" for d in range(6)) + " | Modus |",
              "|---|" + "---:|" * 7]
        for j, c in sorted(seb_prosa.items(), key=lambda kv: -sum(kv[1].values())):
            L.append(f"| {j} | " + " | ".join(str(c.get(d, 0)) for d in range(6)) +
                     f" | {c.most_common(1)[0][0]} |")
        L += ["", "## Sebaran desimal sel tabel per jenis besaran", "",
              "Jenis dikenali dari nama kolom dan label baris. Sel bilangan bulat hanya dihitung untuk ESS, "
              "persen, dan besaran berskala; selebihnya umumnya nomor baris, cacahan, atau label.", "",
              "| Jenis | " + " | ".join(f"d={d}" for d in range(6)) + " | Modus |",
              "|---|" + "---:|" * 7]
        for j, c in sorted(seb_tabel.items(), key=lambda kv: -sum(kv[1].values())):
            L.append(f"| {j} | " + " | ".join(str(c.get(d, 0)) for d in range(6)) +
                     f" | {c.most_common(1)[0][0]} |")
        L += ["", "## Daftar temuan", "",
              "| Buku/bab | Tabel | Baris prosa | Tabel | Prosa | Jenis | Kolom/baris | Ekspresi R | Yakin |",
              "|---|---|---:|---|---|---|---|---|---|"]
        for x in semua:
            e = (x["expr"] or "").replace("|", "\\|")
            kb = f"{x['kolom']} / {x['baris']}".replace("|", "\\|")
            L.append(f"| {x['buku']}/{x['bab']} | {x['label']} | {x['baris_prosa']} | {x['tabel']} | "
                     f"{x['prosa']} | {x['jenis']} | {kb} | `{e}` | {x['yakin']} |" if e else
                     f"| {x['buku']}/{x['bab']} | {x['label']} | {x['baris_prosa']} | {x['tabel']} | "
                     f"{x['prosa']} | {x['jenis']} | {kb} | – | {x['yakin']} |")
        Path(a.md).write_text("\n".join(L) + "\n", encoding="utf-8")
    if a.json:
        Path(a.json).write_text(json.dumps(semua, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.exit(1 if a.ketat and semua else 0)


if __name__ == "__main__":
    main()
