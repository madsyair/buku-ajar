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
  - LEBAR mengikuti lebar blok teks (B5: 5,2 inci). Ubah bila ukuran kertas lain.
  - Huruf gambar Libertinus Serif, satu keluarga dengan teks, judul, kode, dan
    rumus buku (references/aturan-gaya-dan-tampilan.md, "Tipografi"). Berkas
    OTF dicari di _FON_CALON (TeX Live Debian dan TeX Live resmi) lalu kpsewhich.

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

# Ukuran mengikuti lebar blok teks B5 (sekitar 136 mm)
LEBAR = 5.2
TINGGI = 3.2

# Satu keluarga huruf: Libertinus Serif, sama dengan teks dan judul buku.
# Berkas OTF dibawa TeX Live (paket fonts-libertinus/texlive-fonts-extra).
_FON_CALON = [
    Path("/usr/share/texlive/texmf-dist/fonts/opentype/public/libertinus-fonts"),
    Path("/usr/share/fonts/opentype/libertinus"),
]


def _folder_fon():
    for p in _FON_CALON:
        if p.exists():
            return p
    try:
        import subprocess
        jalur = subprocess.run(["kpsewhich", "LibertinusSerif-Regular.otf"],
                               capture_output=True, text=True).stdout.strip()
        if jalur:
            return Path(jalur).parent
    except OSError:
        pass
    return None


def _daftarkan_fon():
    """Daftarkan Libertinus Serif agar huruf gambar sama dengan teks buku."""
    keluarga = "serif"
    folder = _folder_fon()
    berkas = sorted(folder.glob("LibertinusSerif-*.otf")) if folder else []
    for b in berkas:
        font_manager.fontManager.addfont(str(b))
    if berkas:
        keluarga = "Libertinus Serif"
    return keluarga


def gaya(palet=None):
    """Terapkan tema seaborn dan rcParams seri (palet bawaan: Buku 1)."""
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore")
    keluarga = _daftarkan_fon()
    sns.set_theme(style="whitegrid", palette=palet or PALET, font=keluarga)
    plt.rcParams.update({
        "figure.figsize": (LEBAR, TINGGI),
        "figure.dpi": 150,
        "axes.edgecolor": ABU,
        "axes.labelcolor": "#222222",
        # Libertinus lebih sempit dan x-height-nya lebih kecil daripada
        # Pagella; ukuran dinaikkan ±8% agar lebar teks gambar tetap sama.
        "axes.titlesize": 11.5,
        "axes.labelsize": 11,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,
        "legend.frameon": False,
        "grid.color": "#E5E7EB",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.serif": [keluarga],
        "font.cursive": [keluarga],
        "font.fantasy": [keluarga],
        "mathtext.fontset": "custom",
        "mathtext.rm": keluarga,
        "mathtext.it": keluarga + ":italic",
        "mathtext.bf": keluarga + ":bold",
        "mathtext.sf": keluarga,
        "mathtext.tt": keluarga,
        "mathtext.cal": keluarga + ":italic",
        "mathtext.fallback": "stix",
        # Libertinus berupa OTF-CFF; Type 42 (TrueType) menyematkannya dengan tipe
        # yang salah, jadi huruf gambar disematkan sebagai Type 3.
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
