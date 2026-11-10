"""Gaya gambar bersama buku ajar (skill buku-ajar).

Digeneralisasi dari seri Statistika Bayesian. Semua grafik data dibuat dengan
matplotlib dan seaborn memakai modul ini agar semua buku seri seragam. Angka
yang digambar selalu dibaca dari berkas keluaran R (folder data-gambar/);
modul ini tidak menghitung apa pun.

Menyesuaikan untuk proyek baru:
  - Tambahkan satu palet per buku (warna sampul), mis. PALET_BUKU4 = [...],
    dan warna yang sama di tikz-preamble.tex (perintah definecolor seri...).
    Warna terang dipakai untuk isian/pita; untuk garis tipis dan titik pakai
    varian tua (lihat EMAS_TUA, MINT_TUA). Periksa kontras dengan skill dataviz.
  - LEBAR mengikuti lebar kolom teks dari "ukuran" dan "profil" di
    harness/konfig.json (B5 seri: 120 mm = 4,72 inci).
  - Huruf gambar mengikuti opsi "huruf" di harness/konfig.json (bawaan
    libertinus; juga springer, crc, stix; lihat _bersama/huruf.py): huruf teks
    opsi untuk label, angka, dan mathtext, huruf matematika opsi sebagai
    cadangan glif (≤, ≈). Berkas OTF dicari dengan kpsewhich lalu _FON_CALON.
    Variabel lingkungan BUKU_HURUF menimpa konfig (uji).

Pola pakai di chunk Python Quarto (echo: false):
    sys.path[:0] = ["../_bersama", "."]
    from gaya_gambar import gaya, tampil, label_panel, koma_desimal, LEBAR
    gaya(PALET_BUKU3); ...; label_panel(ax); tampil(fig, "buku3-bab02-garis")
"""
import logging
import os
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
import seaborn as sns

# Palet Buku 1 (sama dengan sampul)
TOSKA = "#0F3D3E"
SAWO = "#F2A541"
BATA = "#E4572E"
ABU = "#6B7280"
KREM = "#F7F3E3"
PALET = [TOSKA, SAWO, BATA, ABU, "#3D8B85", "#9C6644"]

# Palet Buku 2 (sama dengan sampul Buku 2): nila, biru langit, magenta
NILA = "#1B1B4B"
LANGIT = "#4CC9F0"
MAGENTA = "#F72585"
PALET_BUKU2 = [NILA, LANGIT, MAGENTA, ABU, "#7B6CF6", "#2A9D8F"]

# Palet Buku 3 (sama dengan sampul Buku 3): hijau hutan, kuning emas, hijau mint.
# EMAS dan MINT terang di atas putih: pakai untuk isian/pita; untuk garis tipis
# dan titik pakai EMAS_TUA dan MINT_TUA.
HUTAN = "#1E3B2F"
EMAS = "#FFC857"
MINT = "#7FD1AE"
EMAS_TUA = "#C98A0B"
MINT_TUA = "#2F8F6B"
PALET_BUKU3 = [HUTAN, EMAS_TUA, MINT_TUA, ABU, MINT, EMAS]

# Ukuran gambar: LEBAR = lebar kolom teks (B5 seri 120 mm = 4,72 inci; ukuran
# buku lain dari "ukuran"/"profil" di konfig.json), dihitung sesudah fungsi
# _lebar_kolom di bawah.
TINGGI = 3.2

# Huruf gambar = huruf teks opsi "huruf" (harness/konfig.json), sama dengan
# teks dan judul buku. Berkas OTF dibawa TeX Live.
_FON_CALON = [
    Path("/usr/share/texlive/texmf-dist/fonts/opentype/public/libertinus-fonts"),
    Path("/usr/share/fonts/opentype/libertinus"),
]


def _muat_huruf():
    """(modul _bersama/huruf.py atau None, isi harness/konfig.json)."""
    import importlib.util
    import json
    sini = Path(__file__).resolve().parent
    konfig = sini.parent / "harness" / "konfig.json"
    k = json.loads(konfig.read_text(encoding="utf-8")) if konfig.exists() else {}
    if not (sini / "huruf.py").exists():
        return None, k
    spek = importlib.util.spec_from_file_location("huruf", sini / "huruf.py")
    huruf = importlib.util.module_from_spec(spek)
    spek.loader.exec_module(huruf)
    return huruf, k


def _opsi_huruf():
    """Opsi huruf proyek dari _bersama/huruf.py dan harness/konfig.json."""
    huruf, k = _muat_huruf()
    if huruf is None:
        return "libertinus", None
    nama = os.environ.get("BUKU_HURUF") or k.get("huruf", "libertinus")
    return nama, huruf.opsi(nama)


def _lebar_kolom(bawaan=4.72):
    """Lebar kolom teks (inci) dari ukuran buku dan profil di konfig.json."""
    try:
        huruf, k = _muat_huruf()
        tl = huruf.tata_letak(k.get("huruf", "libertinus"), k.get("profil", "seri"),
                              k.get("ukuran", "b5"))
        return round(tl["kolom_mm"] / 25.4, 2)
    except Exception:  # konfig tidak ada atau tidak sah: lebar kolom B5 seri
        return bawaan


LEBAR = _lebar_kolom()


def _cari_otf(nama):
    try:
        import subprocess
        jalur = subprocess.run(["kpsewhich", nama], capture_output=True, text=True).stdout.strip()
        if jalur:
            return Path(jalur)
    except OSError:
        pass
    for p in _FON_CALON:
        if (p / nama).exists():
            return p / nama
    return None


def _daftarkan_fon():
    """Daftarkan OTF teks dan matematika opsi; kembalikan (keluarga teks,
    keluarga matematika, mathtext cadangan)."""
    _nama, o = _opsi_huruf()
    otf = o["otf"] if o else {"regular": "LibertinusSerif-Regular.otf",
                              "italic": "LibertinusSerif-Italic.otf",
                              "bold": "LibertinusSerif-Bold.otf",
                              "bolditalic": "LibertinusSerif-BoldItalic.otf",
                              "math": "LibertinusMath-Regular.otf"}
    keluarga, kel_math = "serif", None
    for peran, berkas in otf.items():
        jalur = _cari_otf(berkas)
        if jalur is None:
            continue
        font_manager.fontManager.addfont(str(jalur))
        nama = font_manager.FontProperties(fname=str(jalur)).get_name()
        if peran == "regular":
            keluarga = nama
        elif peran == "math":
            kel_math = nama
    # Hanya berkas opsi yang boleh dipilih untuk nama keluarga itu (Latin Modern
    # punya varian optis LMRoman5..17 bernama keluarga sama).
    kami = {str(_cari_otf(b)) for b in otf.values()}
    nama_kami = {keluarga, kel_math}
    font_manager.fontManager.ttflist = [
        f for f in font_manager.fontManager.ttflist
        if f.name not in nama_kami or f.fname in kami]
    font_manager.fontManager._findfont_cached.cache_clear() \
        if hasattr(font_manager.fontManager._findfont_cached, "cache_clear") else None
    return keluarga, kel_math, (o or {}).get("mathtext_cadangan", "stix")


def _ukuran_dari_huruf_opsi():
    """mathtext custom mengambil varian ukuran simbol (akar, kurung besar) dari
    huruf cadangan STIX meskipun huruf matematika opsi punya glifnya; akibatnya
    STIXGeneral ikut tersemat. Glif diambil dari huruf opsi satu ukuran saja
    (cukup untuk label gambar). API privat matplotlib: dilewati bila berubah."""
    try:
        from matplotlib import _mathtext
        _mathtext.UnicodeFonts.get_sized_alternatives_for_symbol = \
            lambda self, fontname, sym: [(fontname, sym)]
    except (ImportError, AttributeError):
        pass


def gaya(palet=None):
    """Terapkan tema seaborn dan rcParams seri (palet bawaan: Buku 1)."""
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore")
    keluarga, kel_math, cadangan = _daftarkan_fon()
    # Glif yang tidak ada di huruf teks (mis. ≤ dan θ pada Latin Modern Roman)
    # diambil dari huruf matematika opsi, bukan DejaVu bawaan matplotlib.
    daftar = [keluarga] + ([kel_math] if kel_math else [])
    if cadangan != "cm":
        _ukuran_dari_huruf_opsi()
    sns.set_theme(style="whitegrid", palette=palet or PALET, font=keluarga)
    plt.rcParams.update({
        "figure.figsize": (LEBAR, TINGGI),
        "figure.dpi": 150,
        "axes.edgecolor": ABU,
        "axes.labelcolor": "#222222",
        # Ukuran ditetapkan untuk Libertinus (lebih sempit dan x-height-nya
        # lebih kecil daripada Pagella; dinaikkan ±8%); opsi lain memakai
        # ukuran yang sama.
        "axes.titlesize": 11.5,
        "axes.labelsize": 11,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,
        "legend.frameon": False,
        "grid.color": "#E5E7EB",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.family": daftar,
        "font.serif": daftar,
        "font.cursive": daftar,
        "font.fantasy": daftar,
        "mathtext.fontset": "custom",
        "mathtext.rm": kel_math or keluarga,
        "mathtext.it": keluarga + ":italic",
        "mathtext.bf": keluarga + ":bold",
        "mathtext.sf": keluarga,
        "mathtext.tt": keluarga,
        "mathtext.cal": keluarga + ":italic",
        # Cadangan mathtext untuk simbol yang tidak ada di huruf teks: "cm"
        # (Computer Modern) untuk opsi crc, "stix" untuk opsi lain; G-HURUF
        # menandai bila cadangan di luar keluarga opsi ikut tersemat.
        "mathtext.fallback": cadangan,
        # Huruf OTF-CFF (Libertinus, TeX Gyre, Latin Modern, STIX Two) salah
        # disematkan mode Type 42 (TrueType), jadi huruf gambar disematkan Type 3.
        "pdf.fonttype": 3,
    })


def _koma(x, _pos=None):
    teks = f"{x:g}"
    return teks.replace("-", "−").replace(".", ",")


def koma_desimal(ax, sumbu="xy"):
    """Tampilkan desimal dengan koma (EYD V) pada sumbu yang dipilih."""
    if "x" in sumbu:
        ax.xaxis.set_major_formatter(FuncFormatter(_koma))
    if "y" in sumbu:
        ax.yaxis.set_major_formatter(FuncFormatter(_koma))


def tampil(fig, nama, folder="gambar"):
    """Simpan gambar (PDF dan PNG) lalu tampilkan.

    Di dalam Quarto, plt.show() ditangkap knitr sebagai gambar bab.
    Dijalankan mandiri (skrip lampiran), gambar tersimpan di folder `gambar/`.
    """
    os.makedirs(folder, exist_ok=True)
    fig.tight_layout()
    fig.savefig(os.path.join(folder, f"{nama}.pdf"))
    fig.savefig(os.path.join(folder, f"{nama}.png"), dpi=300)
    plt.show()
    plt.close(fig)


def label_panel(axes, mulai=0, x=-0.02, y=1.02):
    """Beri label (a), (b), (c), ... di pojok kiri atas setiap panel.

    Gaya seri: gambar berpanel banyak selalu berlabel huruf, dan keterangan
    gambar menyebut isi setiap huruf. Label diletakkan sedikit di luar
    pojok kiri atas sumbu sehingga tidak bertabrakan dengan judul panel.
    Posisi (x, y) dalam koordinat sumbu dapat digeser bila label menimpa
    angka sumbu atau isi panel.
    """
    import numpy as _np
    for i, ax in enumerate(_np.ravel(axes)):
        ax.text(x, y, f"({chr(97 + mulai + i)})", transform=ax.transAxes,
                ha="right", va="bottom", fontsize=11.5, fontweight="bold",
                color="#222222")
