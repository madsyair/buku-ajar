#!/usr/bin/env python3
"""Pemenggalan kata bahasa Indonesia menurut EYD V (bab III.C).

Pola TeX hyph-id bekerja berbasis pola huruf sehingga tidak mengenal imbuhan
(menghasilkan "pe-ngang-gur" dan "di-ta-fsirk-an"). Modul ini menghitung
pemenggalan sesuai EYD V dengan bantuan kamus kata dasar Sastrawi, lalu
menulis daftar pengecualian \\babelhyphenation untuk semua kata dalam buku.

Kaidah yang diterapkan
  1a  vokal berurutan dipenggal di antaranya        (dibuat konservatif: lihat bawah)
  1b  monoftong eu dan 1c diftong ai, au, ei, oi tidak dipenggal
  1d  V-K-V  dipenggal sebelum konsonan (gabungan kh, ng, ny, sy = satu konsonan)
  1e  V-KK-V dipenggal di antara kedua konsonan
  1f  V-KKK-V dipenggal setelah konsonan pertama
  1g  gabungan konsonan satu bunyi tidak dipenggal
  2a  kata berimbuhan dipenggal di antara bentuk dasar dan imbuhan
  2b  bentuk dasar yang luluh dipenggal seperti kata dasar
  2d  tidak boleh menyisakan satu huruf di awal atau akhir baris
  3   unsur terikat (pasca-, antar-, multi-, ...) dipisah dari unsur lain

Prinsip konservatif: pemenggalan hanya ditawarkan bila pasti benar. Vokal
berurutan di dalam satu morfem tidak dipenggal karena tanpa kamus fonologis
"ma-in" dan "pan-dai" tidak dapat dibedakan. Pemenggalan yang hilang hanya
membuat baris sedikit kurang rapat; pemenggalan yang salah melanggar EYD.

Pemakaian
  python3 harness/penggalan.py --buku buku1         # tulis daftar pengecualian
  python3 harness/penggalan.py --uji                # uji terhadap contoh EYD V
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

AKAR = Path(__file__).resolve().parent.parent
import json  # noqa: E402
import Sastrawi  # noqa: E402


def _folder_bersama():
    """Folder bersama dari harness/konfig.json (kunci 'bersama'), bawaan _bersama."""
    k = AKAR / "harness" / "konfig.json"
    nama = json.loads(k.read_text(encoding="utf-8")).get("bersama", "_bersama") if k.exists() else "_bersama"
    return AKAR / nama

KAMUS = set(
    (Path(Sastrawi.__file__).parent / "Stemmer" / "data" / "kata-dasar.txt")
    .read_text(encoding="utf-8").split()
)
PEMOTONG = StemmerFactory().create_stemmer()

VOKAL = set("aiueo")
GABUNGAN = ("ng", "ny", "kh", "sy")
AWALAN = ["meng", "meny", "mem", "men", "me", "peng", "peny", "pem", "pen",
          "pe", "ber", "be", "bel", "ter", "te", "per", "di", "ke", "se"]
AKHIRAN = ["kan", "an", "nya", "lah", "kah", "tah", "pun", "mu", "ku"]
TERIKAT = ["antar", "pasca", "multi", "inter", "intra", "ekstra", "semi",
           "swa", "tuna", "mikro", "makro", "bio", "foto", "kilo", "hiper",
           "super", "trans", "ultra", "anti", "kontra", "supra", "mono",
           "poli", "tele", "sosio", "non", "sub", "pra"]

# Gabungan bentuk terikat dengan dasar bersuku satu yang tidak bisa dikenali
# aman secara umum (non+ton bukan gabungan), jadi didaftar satu per satu.
GABUNGAN_TERIKAT = {"subbab": [("sub", "dasar"), ("bab", "dasar")]}

# Vokal berurutan dalam satu morfem yang pemenggalannya sudah dicek di KBBI.
# Kaidah umum di sini konservatif (tidak memenggal vokal berurutan), jadi kata
# yang dipenggal TeX di antara dua vokal dan terbukti benar dicatat di sini.
PENGGALAN_KBBI = {"jauh": "ja-uh"}   # KBBI: ja·uh


# ------------------------------------------------------------------ kata dasar
def satuan(kata):
    """Pecah kata menjadi satuan bunyi: gabungan konsonan dan diftong utuh."""
    hasil, i = [], 0
    while i < len(kata):
        dua = kata[i:i + 2]
        if dua in GABUNGAN or dua == "eu":
            hasil.append(dua)
            i += 2
        else:
            hasil.append(kata[i])
            i += 1
    return hasil


def vokal(s):
    return s[0] in VOKAL


def suku_dasar(kata):
    """Penggal satu morfem menurut kaidah 1a–1g; kembalikan daftar potongan."""
    s = satuan(kata)
    inti = [i for i, x in enumerate(s) if vokal(x)]
    if len(inti) < 2:
        return [kata]
    titik = []  # indeks satuan tempat potongan baru dimulai
    for a, b in zip(inti, inti[1:]):
        jarak = b - a - 1  # banyaknya konsonan di antara dua vokal
        if jarak == 0:
            continue  # vokal berurutan: konservatif, tidak dipenggal
        if jarak == 1:
            titik.append(b - 1)  # 1d: sebelum konsonan
        else:
            titik.append(a + 2)  # 1e dan 1f: setelah konsonan pertama
    potong, mulai = [], 0
    for t in titik:
        potong.append("".join(s[mulai:t]))
        mulai = t
    potong.append("".join(s[mulai:]))
    return potong


# ------------------------------------------------------------------ morfologi
def pecah_awalan(teks):
    """Pecah rangkaian awalan (mis. 'memper') menjadi satuan awalan."""
    if not teks:
        return []
    for a in sorted(AWALAN, key=len, reverse=True):
        if teks.startswith(a):
            sisa = pecah_awalan(teks[len(a):])
            if sisa is not None:
                return [a] + sisa
    return None


def pecah_akhiran(teks):
    if not teks:
        return []
    for a in sorted(AKHIRAN + ["i"], key=len, reverse=True):
        if teks.startswith(a):
            sisa = pecah_akhiran(teks[len(a):])
            if sisa is not None:
                return [a] + sisa
    return None


def kata_indonesia(kata):
    return kata in KAMUS or PEMOTONG.stem(kata) in KAMUS


def morfem(kata):
    """Kembalikan daftar (morfem, jenis) dengan jenis 'imbuhan' atau 'dasar'.
    None jika kata tidak dikenal sebagai kata Indonesia."""
    if kata in GABUNGAN_TERIKAT:
        return GABUNGAN_TERIKAT[kata]
    dasar = PEMOTONG.stem(kata)
    if dasar not in KAMUS:
        return None
    if dasar == kata:
        for t in sorted(TERIKAT, key=len, reverse=True):
            sisa = kata[len(t):]
            if kata.startswith(t) and len(sisa) >= 4 and kata_indonesia(sisa):
                return [(t, "dasar"), (sisa, "dasar")]
        return [(kata, "dasar")]
    i = kata.find(dasar)
    if i >= 0:
        depan, belakang = kata[:i], kata[i + len(dasar):]
        # Peluluhan yang tertukar: peng+arang bisa berasal dari karang (2b)
        if dasar[0] in VOKAL and depan:
            for ujung, asal in (("ng", "k"), ("n", "t"), ("m", "p"), ("ny", "s")):
                if depan.endswith(ujung) and asal + dasar in KAMUS:
                    return gabung_luluh(kata, depan[:-len(ujung)], belakang)
    else:
        # Peluluhan: me+nutup dari tutup; cari bentuk dasar tanpa huruf awal
        j = kata.find(dasar[1:])
        if j < 0:
            return [(kata, "dasar")]
        depan, belakang = "", kata[j + len(dasar) - 1:]
        return gabung_luluh(kata, "", belakang)
    aw = pecah_awalan(depan)
    ak = pecah_akhiran(belakang)
    if aw is None or ak is None:
        return [(kata, "dasar")]
    hasil = [(a, "imbuhan") for a in aw]
    if ak and ak[0] == "i":  # akhiran -i menempel (2d: tak boleh satu huruf)
        hasil.append((dasar + "i", "dasar"))
        ak = ak[1:]
    else:
        hasil.append((dasar, "dasar"))
    hasil += [(a, "imbuhan") for a in ak]
    return hasil


def gabung_luluh(kata, _awal, belakang):
    """2b: bagian berimbuhan yang luluh dipenggal seperti kata dasar;
    akhiran tetap dipisah (2a)."""
    ak = pecah_akhiran(belakang) if belakang else []
    if ak is None:
        return [(kata, "dasar")]
    inti = kata[:len(kata) - len(belakang)] if belakang else kata
    hasil = []
    if ak and ak[0] == "i":
        inti += "i"
        ak = ak[1:]
    hasil.append((inti, "dasar"))
    return hasil + [(a, "imbuhan") for a in ak]


def penggal(kata):
    """Pemenggalan EYD V; None untuk kata yang bukan kata Indonesia."""
    k = kata.lower()
    if not re.fullmatch(r"[a-z]+", k) or len(k) < 4:
        return None
    if k in PENGGALAN_KBBI:
        return PENGGALAN_KBBI[k]
    m = morfem(k)
    if m is None:
        return None
    potong = []
    for teks, jenis in m:
        potong.extend([teks] if jenis == "imbuhan" else suku_dasar(teks))
    # 2d: tidak ada potongan satu huruf di awal atau akhir kata
    while len(potong) > 1 and len(potong[0]) < 2:
        potong[1] = potong[0] + potong[1]
        potong.pop(0)
    while len(potong) > 1 and len(potong[-1]) < 2:
        potong[-2] = potong[-2] + potong[-1]
        potong.pop()
    return "-".join(potong)


# ------------------------------------------------------------------ uji EYD V
# Contoh resmi EYD V bab III.C. Pemenggalan konservatif boleh lebih sedikit,
# tetapi setiap titik penggalan yang dihasilkan wajib ada pada kunci EYD.
CONTOH_EYD = {
    "jauh": "ja-uh",
    "subbab": "sub-bab",
    "bapak": "ba-pak", "dengan": "de-ngan", "kenyang": "ke-nyang",
    "lawan": "la-wan", "mutakhir": "mu-ta-khir", "musyawarah": "mu-sya-wa-rah",
    "bantu": "ban-tu", "mandi": "man-di", "sombong": "som-bong",
    "swasta": "swas-ta", "ambruk": "am-bruk", "bentrok": "ben-trok",
    "ultra": "ul-tra", "instrumen": "in-stru-men", "banyak": "ba-nyak",
    "kongres": "kong-res", "makhluk": "makh-luk", "masyhur": "masy-hur",
    "pandai": "pan-dai", "berjalan": "ber-ja-lan", "diambil": "di-am-bil",
    "kekasih": "ke-ka-sih", "membantu": "mem-ban-tu", "pengintai": "peng-in-tai",
    "perbuat": "per-bu-at", "sebuah": "se-bu-ah", "terbawa": "ter-ba-wa",
    "letakkan": "le-tak-kan", "makanan": "ma-kan-an", "kekuatan": "ke-ku-at-an",
    "merasakan": "me-ra-sa-kan", "perbuatan": "per-bu-at-an",
    "memakai": "me-ma-kai", "mengunci": "me-ngun-ci", "menutup": "me-nu-tup",
    "menyapu": "me-nya-pu", "pemikir": "pe-mi-kir", "pengarang": "pe-nga-rang",
    "penolong": "pe-no-long", "penyebut": "pe-nye-but", "nonaktif": "non-ak-tif",
    "pascapanen": "pas-ca-pa-nen", "kilometer": "ki-lo-me-ter",
    "penganggur": "peng-ang-gur", "ditafsirkan": "di-taf-sir-kan",
    "mengakhiri": "meng-a-khi-ri",
}
WAJIB_SAMA = {"bapak", "dengan", "bantu", "mandi", "ambruk", "instrumen",
              "kongres", "makhluk", "berjalan", "membantu", "makanan",
              "menutup", "pengarang", "penganggur", "ditafsirkan", "letakkan"}


def titik(p):
    out, n = set(), 0
    for bagian in p.split("-")[:-1]:
        n += len(bagian)
        out.add(n)
    return out


def uji():
    gagal = []
    for kata, kunci in CONTOH_EYD.items():
        hasil = penggal(kata)
        if hasil is None:
            gagal.append(f"{kata}: tidak dikenali sebagai kata Indonesia")
            continue
        if not titik(hasil) <= titik(kunci):
            gagal.append(f"{kata}: {hasil} memuat penggalan di luar EYD ({kunci})")
        elif kata in WAJIB_SAMA and hasil != kunci:
            gagal.append(f"{kata}: {hasil} seharusnya {kunci}")
    return gagal


def uji_tex():
    """Pastikan XeLaTeX benar-benar memakai pengecualian \\babelhyphenation."""
    kata = ["ditafsirkan", "penganggur", "pengangguran", "makanan"]
    harap = {"ditafsirkan": "di-taf-sir-kan", "penganggur": "peng-ang-gur",
             "pengangguran": "peng-ang-gur-an", "makanan": "ma-kan-an"}
    pengecualian = " ".join(penggal(k) for k in kata)
    with tempfile.TemporaryDirectory() as d:
        tex = Path(d) / "uji.tex"
        tex.write_text(
            "\\documentclass{article}\n\\usepackage[indonesian,provide=*]{babel}\n"
            f"\\babelhyphenation[indonesian]{{{pengecualian}}}\n\\begin{{document}}\n"
            + "".join(f"\\showhyphens{{{k}}}\n" for k in kata) + "\\end{document}\n",
            encoding="utf-8")
        subprocess.run(["xelatex", "-interaction=nonstopmode", "uji.tex"], cwd=d,
                       capture_output=True, text=True, timeout=120)
        log = (Path(d) / "uji.log").read_text(encoding="utf-8", errors="ignore")
    keluar = re.findall(r"\\TU/\S+ (\S+)", log)
    gagal = [f"TeX: {k} dipenggal '{k_tex}', seharusnya '{harap[k]}'"
             for k, k_tex in zip(kata, keluar) if k_tex != harap[k]]
    if len(keluar) != len(kata):
        gagal.append(f"TeX: keluaran \\showhyphens tidak terbaca ({keluar})")
    return gagal


# ------------------------------------------------------------------ kata dalam buku
def prosa_buku(buku):
    sys.path.insert(0, str(AKAR / "harness"))
    from harness import pilah_qmd  # noqa: E402
    teks, miring = [], []
    for qmd in sorted(buku.glob("*.qmd")):
        prosa, chunk = pilah_qmd(qmd.read_text(encoding="utf-8"))
        for _, b in prosa:
            b = re.sub(r"`[^`]*`|\$[^$]*\$|\{[^}]*\}|\[@[^\]]*\]|@\w[\w-]*|\]\([^)]*\)", " ", b)
            teks.append(b)
            miring += re.findall(r"(?<![*\w])\*([^*]+)\*(?!\*)", b)
        for _, isi, _ in chunk:
            teks += re.findall(r"[#%]\|\s*(?:fig|tbl)-cap:\s*\"([^\"]*)\"", isi)
    return " ".join(teks), miring


LATEX_AKSEN = {'"u': "ü", '"o': "ö", '"a': "ä", "'e": "é", "'a": "á", "`e": "è", "'i": "í",
               "vS": "Š", "vs": "š", "vc": "č", "^o": "ô", "~n": "ñ", "aa": "å"}


def _bersihkan_nama(teks):
    """Ubah aksen LaTeX (mis. {\\"u}, {\\v{S}}) menjadi huruf Unicode."""
    def ganti(m):
        kunci = m.group(1) + m.group(2)
        return LATEX_AKSEN.get(kunci, m.group(2))
    teks = re.sub(r"\\([\"'`^~]|v|aa)\s*\{?\s*([A-Za-z]?)\}?", ganti, teks)
    return re.sub(r"[{}\\]", "", teks)


def nama_diri(folder_buku, teks_prosa):
    """Nama orang dan nama diri yang tidak boleh dipenggal: semua unsur nama
    penulis/penyunting di pustaka.bib, ditambah kata berhuruf kapital di tengah
    kalimat yang tidak pernah muncul berhuruf kecil dan bukan kata dasar KBBI."""
    nama = set()
    kecil = set(re.findall(r"\b[a-zà-ž]+\b", teks_prosa))
    for fb in folder_buku:
        bib = fb / "pustaka.bib"
        if not bib.exists():
            continue
        for m in re.finditer(r"\b(?:author|editor)\s*=\s*\{(.*)\}\s*,?\s*$", bib.read_text(encoding="utf-8"), flags=re.M):
            nilai = m.group(1).strip()
            if nilai.startswith("{") and " and " not in nilai and "," not in nilai:
                continue  # penulis lembaga, mis. {Badan Pusat Statistik}
            for bagian in re.split(r"\s+and\s+", _bersihkan_nama(nilai)):
                for w in re.findall(r"[A-Za-zÀ-ž]+", bagian):
                    if len(w) >= 4 and w[0].isupper():
                        nama.add(w)
    for m in re.finditer(r"\b([A-ZÀ-Ž][a-zà-ž]{3,})\b", teks_prosa):
        w = m.group(1)
        if w.lower() not in kecil and w.lower() not in KAMUS and not kata_indonesia(w.lower()) \
                and penggal(w.lower()) is None and not re.search(r"(?:itas|isme|asi|anya)$", w.lower()):
            nama.add(w)
    nama |= {"Bayes", "Bayesian", "Gelman", "Poisson", "Bernoulli", "Laplace", "Metropolis", "Hastings",
             "Gibbs", "Jeffreys", "Hamiltonian", "Markov", "Dirichlet", "Gauss", "Gaussian", "Student",
             "Fisher", "Neyman", "Pearson", "Wishart", "Cholesky", "Jacobian", "Kolmogorov"}
    return sorted(nama)


def tulis(buku):
    # Daftar bersama dipakai semua buku, jadi dihimpun dari semua folder buku*;
    # bila hanya dari satu buku, menjalankan buku lain akan menghapus entrinya.
    # Semua folder buku di akar proyek (buku induk dan kunci jawaban)
    semua = sorted(p for p in AKAR.glob("*/_quarto.yml") if p.parent.name != "harness")
    folder_buku = [b.parent for b in semua] or [buku]
    teks, miring, prosa_saja = "", set(), ""
    for fb in folder_buku:
        t_b, m_b = prosa_buku(fb)
        teks += "\n" + t_b
        prosa_saja += "\n" + t_b
        miring |= set(m_b)
        # Label buatan Quarto (rujukan silang, judul callout) di _quarto.yml
        # serta teks daftar pustaka yang dicetak dari pustaka.bib
        for nama in ("_quarto.yml", "pustaka.bib"):
            berkas = fb / nama
            if berkas.exists():
                teks += "\n" + berkas.read_text(encoding="utf-8")
    kata = sorted({w.lower() for w in re.findall(r"[A-Za-z]+", teks)})
    entri, asing = [], set()
    for w in kata:
        p = penggal(w)
        # Kata tanpa titik penggal yang sah (mis. "naik", "diam" karena kaidah
        # deret vokal dibuat konservatif) juga ditulis, tanpa tanda hubung, agar
        # TeX tidak memenggalnya dengan pola hyph-id.
        if p and ("-" in p or len(w) >= 4):
            entri.append(p)
    for frasa in miring:
        kata_frasa = re.findall(r"[A-Za-z]+", frasa)
        if kata_frasa and not any(kata_indonesia(w.lower()) for w in kata_frasa):
            asing.add(frasa.strip())
    folder = _folder_bersama()
    folder.mkdir(exist_ok=True)
    baris = ["% Pengecualian pemenggalan EYD V — DIBANGKITKAN OTOMATIS oleh",
             "% harness/penggalan.py; jangan disunting tangan.",
             f"% {len(entri)} kata dari {', '.join(b.name for b in folder_buku)}.",
             "\\providehyphenmins{indonesian}{22}",
             "\\babelhyphenation[indonesian]{"]
    baris += ["  " + " ".join(entri[i:i + 8]) for i in range(0, len(entri), 8)]
    nama = nama_diri(folder_buku, prosa_saja)
    # Nama tidak boleh muncul di daftar Indonesia: entri berbahasa lebih
    # spesifik mengalahkan daftar global tanpa titik penggal.
    kecil_nama = {n.lower() for n in nama}
    kecil_nama |= {n + a for n in kecil_nama for a in ("nya", "lah", "kah")}
    baris = [b if not b.startswith("  ") else
             "  " + " ".join(e for e in b.split() if e.replace("-", "") not in kecil_nama)
             for b in baris]
    baris.append("}")
    nama = sorted(set(nama) | {n + "nya" for n in nama})
    baris += ["% Nama orang dan nama diri: tidak dipenggal (keputusan penulis 2026-11-06).",
              "\\babelhyphenation{"]
    baris += ["  " + " ".join(nama[i:i + 8]) for i in range(0, len(nama), 8)]
    baris.append("}")
    (folder / "nama-diri.txt").write_text("\n".join(nama) + "\n", encoding="utf-8")
    (folder / "penggalan-id.tex").write_text("\n".join(baris) + "\n", encoding="utf-8")
    (folder / "istilah-asing.txt").write_text(
        "# Frasa miring yang dikenali sebagai istilah asing (bahasa Inggris).\n"
        "# DIBANGKITKAN OTOMATIS oleh harness/penggalan.py.\n"
        + "\n".join(sorted(asing)) + "\n", encoding="utf-8")
    print(f"{len(entri)} kata Indonesia ditulis ke _bersama/penggalan-id.tex")
    print(f"{len(asing)} frasa asing ditulis ke _bersama/istilah-asing.txt")
    return entri, asing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--buku")
    ap.add_argument("--uji", action="store_true")
    a = ap.parse_args()
    if a.uji:
        gagal = uji() + uji_tex()
        for g in gagal:
            print("GAGAL", g)
        print("LULUS" if not gagal else f"{len(gagal)} kegagalan")
        sys.exit(1 if gagal else 0)
    if a.buku:
        tulis(AKAR / a.buku)


if __name__ == "__main__":
    main()
