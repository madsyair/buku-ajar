#!/usr/bin/env python3
"""Uji berkas jenis agen Claude Code (claude-agents/).

Memeriksa: setiap berkas punya frontmatter sah (name, description, model dengan
nilai opus/sonnet/haiku/fable, tools bila ada), name = nama berkas, isi merujuk
ke agents/NN-*.md yang ada, dan setiap peran di agents/ (kecuali 00-orkestrator,
yang adalah sesi utama) punya tepat satu pasangan.
Pemakaian:
  python3 scripts/uji_agen.py                 # di skill: folder claude-agents/
  python3 harness/uji_agen.py                 # di proyek: .claude/agents/buku-ajar-*.md
                                              # (dilewati bila belum dipasang; pasangan
                                              # dicek bila skill ditemukan lewat BUKU_AJAR_SKILL
                                              # atau harness/skill-asal.txt)
"""
import os
import re
import sys
from pathlib import Path

MODEL = {"opus", "sonnet", "haiku", "fable"}


def frontmatter(teks):
    m = re.match(r"---\n(.*?)\n---\n", teks, re.S)
    if not m:
        return None
    d = {}
    for baris in m.group(1).splitlines():
        k, s, v = baris.partition(":")
        if not s or not k.strip() or k != k.strip():
            return None
        d[k.strip()] = v.strip()
    return d


def uji(skill, folder):
    """skill None: hanya frontmatter dan rujukan berbentuk sah (tanpa pasangan)."""
    salah = []
    peran = {p.stem: p for p in sorted((skill / "agents").glob("[0-9]*.md"))} if skill else {}
    berkas = sorted(folder.glob("buku-ajar-*.md"))
    dipasangkan = {}
    for b in berkas:
        t = b.read_text(encoding="utf-8")
        fm = frontmatter(t)
        if fm is None:
            salah.append(f"{b.name}: frontmatter tidak sah"); continue
        for k in ("name", "description", "model"):
            if not fm.get(k):
                salah.append(f"{b.name}: kunci {k} kosong/hilang")
        if fm.get("model") not in MODEL:
            salah.append(f"{b.name}: model {fm.get('model')!r} di luar {sorted(MODEL)}")
        if fm.get("name") != b.stem:
            salah.append(f"{b.name}: name harus sama dengan nama berkas")
        if not set(fm) <= {"name", "description", "model", "tools"}:
            salah.append(f"{b.name}: kunci tak dikenal {sorted(set(fm) - {'name', 'description', 'model', 'tools'})}")
        if "tools" in fm and not fm["tools"]:
            salah.append(f"{b.name}: tools kosong")
        m = re.search(r"agents/([0-9]+[a-z]?-[a-z0-9-]+)\.md", t.split("---\n", 2)[-1])
        if not m or (skill and m.group(1) not in peran):
            salah.append(f"{b.name}: isi tidak merujuk ke agents/NN-*.md yang ada")
        else:
            dipasangkan.setdefault(m.group(1), []).append(b.name)
        if not b.name.startswith("buku-ajar-" + (m.group(1).split("-")[0] if m else "?") + "-"):
            salah.append(f"{b.name}: nomor peran pada nama berkas tidak sama dengan peran yang dirujuk")
    for nama in peran:
        if nama.startswith("00-"):
            continue
        n = len(dipasangkan.get(nama, []))
        if n != 1:
            salah.append(f"agents/{nama}.md: {n} pasangan di {folder.name}/ (harus 1)")
    return salah, len(berkas)


def cari_skill(akar):
    for c in (os.environ.get("BUKU_AJAR_SKILL"),
              (akar / "harness" / "skill-asal.txt").read_text().strip()
              if (akar / "harness" / "skill-asal.txt").exists() else None,
              str(Path.home() / ".claude/skills/buku-ajar")):
        if c and (Path(c) / "agents").is_dir():
            return Path(c)
    return None


if __name__ == "__main__":
    ini = Path(__file__).resolve().parent
    if (ini.parent / "claude-agents").is_dir():      # di skill
        skill, folder = ini.parent, ini.parent / "claude-agents"
    else:                                            # di proyek
        akar = ini.parent
        folder = akar / ".claude" / "agents"
        if not list(folder.glob("buku-ajar-*.md")):
            print("dilewati: agen belum dipasang (siapkan_proyek.py --pasang-agen)")
            sys.exit(0)
        skill = cari_skill(akar)
        if skill is None:
            print("peringatan: skill tidak ditemukan; pasangan dengan agents/ tidak diperiksa")
    salah, n = uji(skill, folder)
    for s in salah:
        print("SALAH:", s)
    if salah:
        sys.exit(1)
    print(f"benar: {n} berkas agen sah" + (" dan berpasangan dengan peran di agents/" if skill else ""))
