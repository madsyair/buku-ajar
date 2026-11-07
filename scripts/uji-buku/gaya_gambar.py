"""Gaya gambar bersama seri Statistika Bayesian.

Semua grafik data dibuat dengan matplotlib dan seaborn memakai modul ini agar
ketiga buku seragam. Angka yang digambar selalu dibaca dari berkas keluaran R
(folder data-gambar/); modul ini tidak menghitung apa pun.
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

# Ukuran mengikuti lebar blok teks B5 (sekitar 136 mm)
LEBAR = 5.2
TINGGI = 3.2

_FON = Path("/usr/share/texmf/fonts/opentype/public/tex-gyre")


def _daftarkan_fon():
    """Daftarkan TeX Gyre Pagella agar huruf gambar sama dengan teks buku."""
    keluarga = "serif"
    if _FON.exists():
        for berkas in _FON.glob("texgyrepagella-*.otf"):
            font_manager.fontManager.addfont(str(berkas))
        keluarga = "TeX Gyre Pagella"
    return keluarga


def gaya():
    """Terapkan tema seaborn dan rcParams seri."""
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore")
    keluarga = _daftarkan_fon()
    sns.set_theme(style="whitegrid", palette=PALET, font=keluarga)
    plt.rcParams.update({
        "figure.figsize": (LEBAR, TINGGI),
        "figure.dpi": 150,
        "axes.edgecolor": ABU,
        "axes.labelcolor": "#222222",
        "axes.titlesize": 10.5,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "legend.frameon": False,
        "grid.color": "#E5E7EB",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.cursive": [keluarga],
        "font.fantasy": [keluarga],
        "mathtext.fontset": "custom",
        "mathtext.rm": keluarga,
        "mathtext.it": keluarga + ":italic",
        "pdf.fonttype": 42,
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
