#!/usr/bin/env python3
"""G-DAG-STAN: setiap DAG di bab punya padanan di program Stan bab yang sama.

Berkas ini identik di harness seri (harness/dag_stan.py) dan di skill buku-ajar
(scripts/dag_stan.py). harness.py memanggil periksa(); status WARNING pada tahap draf
dan GAGAL pada --tahap akhir, seperti G-SITASI-ULANG.

DAG dikenali dari chunk ```{tikz}``` berlabel fig-dag-* atau yang memuat bayesnet,
\\node[latent], \\node[obs], \\factor, atau \\plate (gaya turunan latent/obs/det/const
yang didefinisikan lewat \\tikzset juga dikenali). Program Stan bab dikumpulkan dari:
blok ```stan``` dan chunk ```{stan file=...}```; teks program di string R
(`kode <- "... model { ... }"`); berkas stan/<nama>.stan yang dirujuk chunk R
(file.path("stan", "x.stan"), basename = "x"); blok ```stan``` di build/<bab>.knit.md
(keluaran stancode() yang dicetak); dan arahan `dag-stan: program <jalur>`, dengan
jalur .stan atau fit/<nama>.rds (dibaca dengan stancode(readRDS(...)) lewat Rscript).

Pemeriksaan (minimum, statis):
  1. setiap simpul parameter (latent, termasuk gaya putus-putus/bertitik) dan data
     (obs, const) punya padanan nama di program yang paling cocok; simpul
     deterministik (det, belah ketupat) tidak diperiksa karena sering hanya ekspresi;
  2. setiap parameter yang dideklarasikan di blok `parameters` program itu tergambar
     sebagai simpul, kecuali pola di "parameter_tanpa_simpul" (mis. z_1, zb pada
     parameterisasi tak terpusat brms);
  3. batas plat simbolik (`j = 1, \\dots, J`) muncul sebagai nama di program.
Panah tidak diperiksa otomatis (ketergantungan brms tersembunyi di fungsi _glm); itu
tugas reviewer rumus dan kode.

Nama simpul dinormalkan: \\alpha → alpha, \\mu_0 → mu0/mu_0, \\sigma_\\alpha →
sigma_alpha, \\theta_j → theta (indeks satu huruf i, j, k, n, t dibuang), y^{rep}_j →
y_rep, \\tilde{y} → y_baru/y_tilde, \\mathbf{x}_n → x, R^2 → R2. Padanan lazim
(alpha ↔ Intercept/b_Intercept, beta ↔ b, sigma_alpha ↔ sd_1, ...) dibaca dari
dag-stan-padanan.json di folder yang sama. Arahan per bab, sebagai komentar HTML di
mana saja di bab atau komentar `%` di dalam chunk TikZ (berlaku untuk DAG itu saja):
  <!-- dag-stan: abaikan z karena dimarginalkan -->
  <!-- dag-stan: padanan b_alpha = laju_alpha -->
  % dag-stan: program fit/b3-02-r2d2.rds
"""
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

PADANAN_BAWAAN = {
    "padanan": {},
    "data_brms": ["X", "Xc", "offsets"],
    "parameter_tanpa_simpul": [],
    "dekorasi": {"tilde": ["baru", "tilde", "new"], "hat": ["hat"], "bar": ["bar"]},
}

JENIS_DASAR = {"latent": "parameter", "obs": "data", "const": "data", "det": "deterministik"}
INDEKS = set("ijknt")
TIPE_STAN = (r"(?:array\s*\[[^\]]*\]\s*)?(?:int|real|complex|vector|row_vector|matrix|simplex|"
             r"ordered|positive_ordered|unit_vector|sum_to_zero_vector|cholesky_factor_corr|"
             r"cholesky_factor_cov|corr_matrix|cov_matrix)\b")
YUNANI = ["alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta", "theta",
          "vartheta", "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma", "tau",
          "upsilon", "phi", "varphi", "chi", "psi", "omega", "Gamma", "Delta", "Theta", "Lambda",
          "Sigma", "Phi", "Psi", "Omega"]


def muat_padanan(berkas=None):
    p = json.loads(json.dumps(PADANAN_BAWAAN))
    berkas = Path(berkas) if berkas else Path(__file__).resolve().parent / "dag-stan-padanan.json"
    if berkas.exists():
        isi = json.loads(berkas.read_text(encoding="utf-8"))
        for k, v in isi.items():
            if not k.startswith("_"):
                p[k] = v
    return p


# ---------------------------------------------------------------- pengurai TikZ
def _seimbang(teks, i, buka, tutup):
    """Indeks sesudah pasangan kurung yang dibuka di teks[i]."""
    d = 0
    for j in range(i, len(teks)):
        if teks[j] == buka:
            d += 1
        elif teks[j] == tutup:
            d -= 1
            if d == 0:
                return j + 1
    return len(teks)


def _pisah_opsi(opsi):
    hasil, d, awal = [], 0, 0
    for i, c in enumerate(opsi):
        if c in "{[(":
            d += 1
        elif c in "}])":
            d -= 1
        elif c == "," and d == 0:
            hasil.append(opsi[awal:i].strip())
            awal = i + 1
    hasil.append(opsi[awal:].strip())
    return [h for h in hasil if h]


def gaya_turunan(tikz):
    """Gaya \\tikzset turunan latent/obs/det/const: {"par": "latent", ...}."""
    gaya = {}
    for m in re.finditer(r"([A-Za-z]+)/\.style\s*=\s*\{", tikz):
        isi = tikz[m.end() - 1:_seimbang(tikz, m.end() - 1, "{", "}")]
        for t in _pisah_opsi(isi[1:-1]):
            if t in JENIS_DASAR:
                gaya[m.group(1)] = t
                break
    return gaya


def simpul_tikz(tikz):
    """Daftar (nama, jenis_dasar, label, gaya_tambahan) untuk setiap \\node berjenis."""
    gaya = gaya_turunan(tikz)
    hasil = []
    for m in re.finditer(r"\\node\s*\[", tikz):
        i = m.end() - 1
        j = _seimbang(tikz, i, "[", "]")
        opsi = _pisah_opsi(tikz[i + 1:j - 1])
        jenis = next((JENIS_DASAR.get(gaya.get(t, t)) for t in opsi
                      if gaya.get(t, t) in JENIS_DASAR), None)
        if jenis is None:
            continue
        sisa = tikz[j:]
        mn = re.match(r"\s*\((\w+)\)", sisa)
        nama = mn.group(1) if mn else ""
        k = j + (mn.end() if mn else 0)
        ma = re.match(r"\s*at\s*", tikz[k:])
        if ma:
            k += ma.end()
            k = _seimbang(tikz, k, "(", ")") if tikz[k] == "(" else k
        kb = tikz.find("{", k)
        if kb < 0:
            continue
        label = tikz[kb + 1:_seimbang(tikz, kb, "{", "}") - 1]
        hasil.append((nama, jenis, label.strip(), opsi))
    return hasil


def plat_tikz(tikz):
    """Daftar (label, batas) untuk setiap \\plate; batas = simbol sesudah \\dots/\\ldots."""
    hasil = []
    for m in re.finditer(r"\\plate\s*(\[[^\]]*\])?\s*\{", tikz):
        k = m.end() - 1
        k = _seimbang(tikz, k, "{", "}")           # nama plat
        k = tikz.find("{", k)
        k = _seimbang(tikz, k, "{", "}")           # isi plat
        kb = tikz.find("{", k)
        label = tikz[kb + 1:_seimbang(tikz, kb, "{", "}") - 1]
        mb = re.search(r"\\[lc]?dots\s*,\s*([A-Za-z]\w*(?:_\{?\w+\}?)?)\s*\$", label)
        hasil.append((label, mb.group(1) if mb else None))
    return hasil


def adalah_dag(opsi_chunk, isi):
    if re.search(r"label:\s*fig-dag", opsi_chunk + "\n" + isi):
        return True
    return bool(re.search(r"bayesnet|\\factor\b|\\plate\b|\\node\s*\[\s*(latent|obs)\b", isi)) \
        or any(j in ("parameter", "data") for _, j, _, _ in simpul_tikz(isi))


# ---------------------------------------------------------------- normalisasi simbol
def _buang_pembungkus(s):
    for c in ["mathbf", "boldsymbol", "bm", "mathrm", "mathit", "mathcal", "text", "operatorname"]:
        s = re.sub(r"\\" + c + r"\s*\{([^{}]*)\}", r"\1", s)
        s = re.sub(r"\\" + c + r"\s*(\\?\w)", r"\1", s)
    return s


def simbol_label(label):
    """Simbol mentah dari label simpul: '$\\tilde s_n, u_n$' → ['\\tilde s_n', 'u_n']."""
    mat = re.findall(r"\$([^$]*)\$", label)
    if not mat:
        return []
    hasil = []
    for m in mat:
        hasil += [b.strip() for b in _pisah_opsi(m) if b.strip()]
    return hasil


def kandidat(simbol, padanan):
    """Nama-nama program yang dapat menjadi padanan satu simbol LaTeX."""
    s = _buang_pembungkus(simbol)
    dek = None
    md = re.match(r"\\(tilde|hat|bar|widetilde|widehat|overline)\s*\{?\s*(\\?[A-Za-z]+)\s*\}?(.*)$", s)
    if md:
        dek = {"widetilde": "tilde", "widehat": "hat", "overline": "bar"}.get(md.group(1), md.group(1))
        s = md.group(2) + md.group(3)
    m = re.match(r"\\?([A-Za-z]+)(.*)$", s)
    if not m:
        return set(), ""
    dasar, sisa = m.group(1), m.group(2)
    sup = sub = ""
    for jenis, isi in re.findall(r"([_^])\s*(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\\[A-Za-z]+|\w)", sisa):
        isi = _buang_pembungkus(isi.strip("{}")).replace("\\", "").replace(" ", "")
        if jenis == "^":
            sup = isi
        else:
            sub = isi
    if re.fullmatch(r"[A-Za-z](\[[A-Za-z]\])?([+-]\d+)?", sub) and (sub[0] in INDEKS or sub[0].isupper()):
        sub = ""                                     # indeks: theta_j, mu_{t-1}, mu_N → theta, mu
    elif re.fullmatch(r"\w+,\w+", sub):
        sub = ""
    nama = f"{dasar}_{sub}" if sub else dasar
    if sup == "2":
        nama += "2"                                   # R^2 → R2, tau^2 → tau2
    elif sup:
        nama = f"{nama}_{sup}"                        # y^{rep}_j → y_rep
    if dek:
        akhiran = padanan["dekorasi"].get(dek, [dek])
        calon = {f"{nama}_{a}" for a in akhiran} | {f"{nama}{a}" for a in akhiran}
        nama = f"{nama}_{dek}"
    else:
        calon = {nama, nama.replace("_", "")}
        if sub.isdigit():                             # gamma_0 → padanan gamma
            calon |= set(padanan["padanan"].get(dasar, []))
    for k in list(calon) + [nama]:
        calon |= set(padanan["padanan"].get(k, []))
    return {c for c in calon if c}, nama


# ---------------------------------------------------------------- program Stan
def tanpa_komentar(kode):
    kode = re.sub(r"/\*.*?\*/", " ", kode, flags=re.S)
    return "\n".join(re.sub(r"(//|#).*$", "", b) for b in kode.splitlines())


def blok_stan(kode, nama):
    m = re.search(r"(^|\n)\s*" + re.escape(nama) + r"\s*\{", kode)
    if not m:
        return ""
    i = kode.find("{", m.start() + len(m.group(1)))
    return kode[i + 1:_seimbang(kode, i, "{", "}") - 1]


def parameter_program(kode):
    blok = blok_stan(tanpa_komentar(kode), "parameters")
    nama = []
    for pernyataan in blok.split(";"):
        p = " ".join(pernyataan.split())
        if re.match(TIPE_STAN, p):
            m = re.search(r"(\w+)\s*$", p)
            if m:
                nama.append(m.group(1))
    return nama


def nama_program(kode):
    return set(re.findall(r"\b[A-Za-z_]\w*\b", tanpa_komentar(kode)))


def _baca(p):
    try:
        return Path(p).read_text(encoding="utf-8")
    except OSError:
        return None


_cache_rds = {}


def stancode_rds(rds):
    """stancode(readRDS(rds)) lewat Rscript; None bila R/brms tidak tersedia."""
    rds = Path(rds).resolve()
    if rds in _cache_rds:
        return _cache_rds[rds]
    kode = None
    if rds.exists() and shutil.which("Rscript"):
        r = ("suppressPackageStartupMessages(library(brms)); "
             "cat(as.character(stancode(readRDS(commandArgs(TRUE)[1]))))")
        try:
            h = subprocess.run(["Rscript", "-e", r, str(rds)], capture_output=True, text=True,
                               timeout=300)
            if h.returncode == 0 and "model" in h.stdout:
                kode = h.stdout
        except (OSError, subprocess.TimeoutExpired):
            pass
    _cache_rds[rds] = kode
    return kode


def program_bab(qmd, teks):
    """Daftar program (nama, posisi_baris, kode) di bab; posisi dipakai untuk memilih
    program terdekat bila skor kecocokan sama."""
    qmd = Path(qmd)
    dasar = qmd.parent
    hasil = []
    baris_ke = lambda i: teks.count("\n", 0, i) + 1  # noqa: E731

    def tambah(nama, pos, kode):
        if kode and re.search(r"\b(parameters|model)\s*\{", kode):
            hasil.append((nama, pos, kode))

    for m in re.finditer(r"^```+\s*\{?stan\b([^\n]*)\n(.*?)^```+\s*$", teks, flags=re.S | re.M):
        mf = re.search(r"file\s*=\s*[\"']([^\"']+)[\"']", m.group(1))
        if mf:
            tambah(mf.group(1), baris_ke(m.start()), _baca(dasar / mf.group(1)))
        tambah(f"blok stan b. {baris_ke(m.start())}", baris_ke(m.start()), m.group(2))
    for m in re.finditer(r"(\w+)\s*<-\s*\"((?:[^\"\\]|\\.)*)\"", teks, flags=re.S):
        if re.search(r"\bmodel\s*\{", m.group(2)):
            tambah(m.group(1), baris_ke(m.start()), m.group(2))
    rujukan = [(baris_ke(m.start()), m.group(1)) for m in
               re.finditer(r"file\.path\(\s*\"stan\"\s*,\s*\"([\w.-]+\.stan)\"", teks)]
    rujukan += [(baris_ke(m.start()), m.group(1)) for m in re.finditer(r"\bstan/([\w.-]+\.stan)\b", teks)]
    rujukan += [(baris_ke(m.start()), m.group(1) + ".stan") for m in
                re.finditer(r"dir\s*=\s*\"stan\"\s*,\s*basename\s*=\s*\"([\w.-]+)\"", teks)]
    for pos, f in rujukan:
        tambah(f"stan/{f}", pos, _baca(dasar / "stan" / f))
    md = dasar / "build" / f"{qmd.stem}.knit.md"
    if md.exists():
        for m in re.finditer(r"^```+\s*\{?\.?stan\b[^\n]*\n(.*?)^```+\s*$", _baca(md) or "",
                             flags=re.S | re.M):
            tambah(f"build/{md.name} (stancode)", 10 ** 9, m.group(1))
    # buang duplikat isi
    unik, lihat = [], set()
    for nama, pos, kode in hasil:
        h = hashlib.sha1(" ".join(tanpa_komentar(kode).split()).encode()).hexdigest()
        if h not in lihat:
            lihat.add(h)
            unik.append((nama, pos, kode))
    return unik


def arahan(teks):
    """Arahan dag-stan dari komentar HTML (<!-- ... -->) atau komentar TikZ (% ...)."""
    hasil = {"abaikan": set(), "padanan": {}, "program": []}
    for m in re.finditer(r"(?:<!--|%)\s*dag-stan:\s*(abaikan|padanan|program)\s+(.*?)\s*(?:-->|$)",
                         teks, flags=re.M):
        jenis, isi = m.group(1), m.group(2)
        if jenis == "abaikan":
            butir = re.split(r"\s+karena\s+", isi, maxsplit=1)[0]
            for b in re.split(r"[,\s]+", butir):
                b = b.strip("`$")
                if b:
                    hasil["abaikan"].add(b)
                    if "\\" in b or "_" in b or "{" in b:
                        hasil["abaikan"].add(kandidat(b, PADANAN_BAWAAN)[1])
        elif jenis == "padanan":
            ma = re.match(r"(.+?)\s*=\s*(.+)$", isi)
            if ma:
                kiri = ma.group(1).strip("`$ ")
                kiri = kandidat(kiri, PADANAN_BAWAAN)[1] if "\\" in kiri else kiri
                hasil["padanan"].setdefault(kiri, []).extend(
                    x.strip("` ") for x in re.split(r"[,/]", ma.group(2)) if x.strip("` "))
        else:
            hasil["program"].append(isi.split()[0])
    return hasil


# ---------------------------------------------------------------- pemeriksaan
def _cocok(calon, nama_prog):
    lower = {n.lower() for n in nama_prog}
    return any(c in nama_prog or c.lower() in lower for c in calon)


def _nilai(dag, prog, padanan, abaikan):
    """Kembalikan daftar masalah untuk satu pasangan DAG–program."""
    nama_prog = nama_program(prog)
    brms = "lprior" in nama_prog or "Xc" in nama_prog
    masalah, tertutup = [], set()
    for nama, jenis, label, _ in dag["simpul"]:
        if jenis == "deterministik":
            for s in simbol_label(label):
                tertutup |= kandidat(s, padanan)[0]
            continue
        for s in simbol_label(label):
            calon, norm = kandidat(s, padanan)
            if not norm or re.fullmatch(r"[\d.,{}\s]+", s):
                continue
            tertutup |= calon
            if norm in abaikan or s in abaikan or nama in abaikan or calon & abaikan:
                continue
            if jenis == "data" and brms and _cocok(padanan["data_brms"], nama_prog):
                continue
            if not _cocok(calon, nama_prog):
                masalah.append(f"simpul {jenis} ${s}$ ({norm}) tanpa padanan di program")
    pola_bebas = [re.compile(p + r"$") for p in padanan["parameter_tanpa_simpul"]]
    lower_tutup = {t.lower() for t in tertutup}
    for p in parameter_program(prog):
        if p in abaikan or p.lower() in lower_tutup or any(r.match(p) for r in pola_bebas):
            continue
        masalah.append(f"parameter program `{p}` tidak tergambar di DAG")
    for label, batas in dag["plat"]:
        if not batas:
            continue
        calon, norm = kandidat(batas, padanan)
        calon |= {batas.replace("{", "").replace("}", "")}
        if norm in abaikan or batas in abaikan:
            continue
        if not _cocok(calon, nama_prog) and not (brms and norm in ("N", "K")):
            masalah.append(f"batas plat `{batas}` ({label.strip()}) tidak ada di program")
    return masalah


def dag_bab(teks):
    """Daftar DAG: dict(label, baris, simpul, plat, arahan)."""
    hasil = []
    for m in re.finditer(r"^```+\s*\{tikz([^}\n]*)\}\s*\n(.*?)^```+\s*$", teks, flags=re.S | re.M):
        isi = m.group(2)
        if not adalah_dag(m.group(1), isi):
            continue
        ml = re.search(r"(?:label:\s*|label\s*=\s*[\"']?)(fig-[\w-]+)", m.group(1) + "\n" + isi)
        hasil.append({"label": ml.group(1) if ml else "(tanpa label)",
                      "baris": teks.count("\n", 0, m.start()) + 1,
                      "simpul": simpul_tikz(isi), "plat": plat_tikz(isi), "arahan": arahan(isi)})
    return hasil


def periksa(qmd, padanan=None):
    """Kembalikan (pesan, info). pesan: masalah per DAG; info: ringkasan pasangan."""
    qmd = Path(qmd)
    teks = qmd.read_text(encoding="utf-8")
    padanan = padanan or muat_padanan()
    dags = dag_bab(teks)
    if not dags:
        return [], []
    arah_bab = arahan(re.sub(r"^```+\s*\{tikz.*?^```+\s*$", "", teks, flags=re.S | re.M))
    programs = program_bab(qmd, teks)
    pesan, info = [], []
    for dag in dags:
        ar = {"abaikan": arah_bab["abaikan"] | dag["arahan"]["abaikan"],
              "padanan": {**arah_bab["padanan"], **dag["arahan"]["padanan"]},
              "program": dag["arahan"]["program"] or []}
        pad = json.loads(json.dumps(padanan))
        for k, v in ar["padanan"].items():
            pad["padanan"][k] = pad["padanan"].get(k, []) + v
        calon_prog = list(programs)
        for p in ar["program"]:
            jalur = (qmd.parent / p)
            kode = stancode_rds(jalur) if p.endswith(".rds") else _baca(jalur)
            if kode is None:
                pesan.append(f"baris {dag['baris']}: {dag['label']}: program `{p}` tidak dapat dibaca")
            else:
                calon_prog = [(p, dag["baris"], kode)]
        if not calon_prog:
            if re.search(r"\b(brm|cmdstan_model|stan_model|stan)\s*\(", teks):
                pesan.append(f"baris {dag['baris']}: {dag['label']}: tidak ada program Stan yang dapat "
                             "dibaca di bab ini; tambahkan `% dag-stan: program fit/<nama>.rds` "
                             "atau `stan/<nama>.stan` di chunk DAG")
            info.append(f"{dag['label']}: tanpa program Stan")
            continue
        nilai = []
        for nama, pos, kode in calon_prog:
            m = _nilai(dag, kode, pad, ar["abaikan"])
            jarak = (0 if pos >= dag["baris"] else 1, abs(pos - dag["baris"]))
            nilai.append((len(m), jarak, nama, m))
        nilai.sort(key=lambda x: (x[0], x[1]))
        _, _, nama, masalah = nilai[0]
        info.append(f"{dag['label']} ↔ {nama}: {'cocok' if not masalah else f'{len(masalah)} masalah'}")
        pesan += [f"baris {dag['baris']}: {dag['label']} ↔ {nama}: {x}" for x in masalah]
    return pesan, info


if __name__ == "__main__":
    import sys
    for f in sys.argv[1:]:
        p, i = periksa(f)
        print(f"== {f}")
        for x in i:
            print("  " + x)
        for x in p:
            print("  ! " + x)
