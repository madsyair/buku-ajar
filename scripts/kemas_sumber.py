#!/usr/bin/env python3
"""Kemas kode sumber Quarto per buku (buku induk + kunci jawaban + folder bersama).

Digeneralisasi dari alat seri Statistika Bayesian. Buku dikenali otomatis:
setiap folder di akar proyek yang memuat _quarto.yml dan tidak berawalan
"kunci-" adalah buku induk; "kunci-<nama>" (bila ada) adalah pasangannya.
Judul dibaca dari _quarto.yml. Keterangan perangkat per buku dapat ditulis di
harness/konfig.json, kunci "kemasan": {"<buku>": "R 4.x, brms ..."}.

Pemakaian:  python3 scripts/kemas_sumber.py [folder_keluaran] [--proyek NAMA]
Keluaran:   <proyek>-<buku>-sumber.zip, masing-masing dengan BANGUN.md.
"""
import json
import pathlib
import re
import sys
import zipfile
from datetime import date

AKAR = pathlib.Path(__file__).resolve().parent.parent
argv = [a for a in sys.argv[1:] if not a.startswith("--")]
KELUAR = pathlib.Path(argv[0]) if argv else AKAR.parent / "kemasan-sumber"
PROYEK = sys.argv[sys.argv.index("--proyek") + 1] if "--proyek" in sys.argv else AKAR.name
KONFIG = AKAR / "harness" / "konfig.json"
KONF = json.loads(KONFIG.read_text(encoding="utf-8")) if KONFIG.exists() else {}
BUANG_DIR = {"build", "_book", ".quarto", "fit", "__pycache__", "gdb", ".git"}
BUANG_EXT = {".pdf", ".png", ".pyc", ".rds", ".log", ".aux", ".zip", ".gz", ".docx"}
# Berkas/folder bersama yang ikut setiap kemasan (yang tidak ada dilewati)
BERSAMA = [KONF.get("bersama", "_bersama"), "sampul", "harness", "naskah-bersama", "alat",
           "KEPUTUSAN-RANCANGAN.md", "README.md"] + KONF.get("kemasan_tambahan", [])


def daftar_buku():
    hasil = {}
    for q in sorted(AKAR.glob("*/_quarto.yml")):
        b = q.parent.name
        if b.startswith("kunci-") or b == "harness":
            continue
        m = re.search(r"^\s*title:\s*\"?([^\"\n]+)", q.read_text(encoding="utf-8"), flags=re.M)
        judul = m.group(1).strip() if m else b
        k = f"kunci-{b}" if (AKAR / f"kunci-{b}").exists() else None
        hasil[b] = (k, judul, KONF.get("kemasan", {}).get(b, "lihat prakata buku"))
    return hasil


def ikut(p):
    if any(x in BUANG_DIR or x.endswith("_files") for x in p.parts):
        return False
    if p.suffix in BUANG_EXT and not p.name.startswith("sampul"):
        return False
    if p.parent.name == "stan" and p.suffix == "":        # biner Stan hasil kompilasi
        return False
    if p.suffix == ".tex" and len(p.parts) == 2 and not p.stem.startswith("preamble"):
        return False                                       # .tex hasil render
    s = str(p)
    return "harness/sumber" not in s and "harness/laporan" not in s   # sumber berhak cipta


def bangun_md(b, k, judul, perangkat, bab):
    kunci = f" dan `{k}/` (kunci jawaban untuk pengajar)" if k else ""
    render_k = f"\ncd ../{k}\nquarto render            # kunci jawaban ke {k}/_book/" if k else ""
    return f"""# Cara membangun *{judul}*

Dikemas {date.today():%d-%m-%Y}. Isi: `{b}/` ({bab}){kunci}, ditambah folder bersama
(preamble LaTeX, filter Lua, gaya gambar, pemenggalan), `harness/` (pemeriksa mutu, tanpa
`sumber/` yang berhak cipta), `lampiran-kode/` (skrip per bab), dan dokumen keputusan.

## Perangkat

- R 4.x, Quarto >= 1.6, TeX Live dengan XeLaTeX.
- Python 3 dengan pandas, pyarrow, matplotlib, seaborn (gambar dibuat dari parquet yang ditulis R).
- {perangkat}

## Membangun

```bash
cd {PROYEK}/{b}
quarto render            # PDF dan Word ke {b}/_book/{render_k}
```

Cache model (`fit/`) dibuat saat pertama dirajut, jadi render pertama lama. Hasil dapat
sedikit berbeda antarversi perangkat karena galat Monte Carlo.

## Pemeriksaan mutu (opsional)

```bash
cd {PROYEK}
python3 harness/harness.py --buku {b} --bab bab01
```

G-REFERENSI memerlukan teks sumber di `harness/sumber/` (tidak disertakan karena hak cipta).
Tidak disertakan: PDF/Word jadi, gambar hasil render, cache model, biner Stan, berkas antara.
"""


def main():
    KELUAR.mkdir(parents=True, exist_ok=True)
    lampiran = KONF.get("lampiran", "lampiran-kode")
    for b, (k, judul, perangkat) in daftar_buku().items():
        n_bab = len(list((AKAR / b).glob("bab*.qmd")))
        bab = f"{n_bab} bab" + (" + lampiran" if list((AKAR / b).glob("lampiran-*.qmd")) else "")
        z = KELUAR / f"{PROYEK}-{b}-sumber.zip"
        n = 0
        bagian = BERSAMA + [b, f"{lampiran}/{b}"] + ([k, f"{lampiran}/{k}"] if k else [])
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for top in bagian:
                p = AKAR / top
                if not p.exists():
                    continue
                for f in ([p] if p.is_file() else sorted(q for q in p.rglob("*") if q.is_file())):
                    rel = f.relative_to(AKAR)
                    if ikut(rel):
                        zf.write(f, f"{PROYEK}/{rel}")
                        n += 1
            zf.writestr(f"{PROYEK}/BANGUN.md", bangun_md(b, k, judul, perangkat, bab))
        print(f"{z.name}: {n} berkas, {z.stat().st_size / 1e6:.1f} MB, {bab}")


if __name__ == "__main__":
    main()
