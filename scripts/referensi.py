"""Gerbang G-REFERENSI: setiap sitasi harus terverifikasi dan setiap klaim yang
dikutip harus benar-benar ada di sumbernya.

Dua registri:
  harness/referensi.json  kunci bib -> identitas (DOI/ISBN/URL) dan catatan verifikasi
  harness/klaim.json      daftar klaim: bab, kunci, penanda kalimat, bukti; opsional
                          "sitasi_di" bila kalimat klaim tanpa @kunci karena sumbernya sudah
                          disitasi di kalimat lebih awal pada paragraf yang sama (2026-11-12)

Jenis bukti dan cara pemeriksaannya:
  berkas     kutipan dicari otomatis di teks sumber lokal harness/sumber/<berkas>
             (salinan buku dari Project; tidak ikut didistribusikan). Bila tidak
             ditemukan di sumber utama itu, dicari di versi kedua
             harness/sumber/versi2/<berkas> (konversi lain dari buku yang sama;
             keputusan 2026-11-12); laporan menyebut versi yang cocok. Fikstur uji
             yang punya folder sumber/ sendiri memakai folder itu.
  rd         kutipan dicari otomatis di dokumentasi R (tools::Rd2txt)
  deskripsi  kutipan dicari otomatis di DESCRIPTION paket R
  citation   kutipan dicari otomatis di keluaran citation()
  hitung     ekspresi R dijalankan; hasilnya harus sama dengan nilai sumber
  web        diverifikasi saat menulis dengan membuka URL; dicatat URL, tanggal
             akses, dan kutipan apa adanya (tidak dapat diulang luring)
"""
import json
import re
import subprocess
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
SUMBER = AKAR / "harness" / "sumber"
VERSI_KEDUA = "versi2"   # subfolder sumber kedua: <sumber>/versi2/<berkas> (2026-11-12)

LIGATUR = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl",
           "‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-"}


def normal(teks):
    for a, b in LIGATUR.items():
        teks = teks.replace(a, b)
    teks = re.sub(r"<!-- Page \d+ -->", " ", teks)
    teks = re.sub(r"\u00ad\s*", "", teks)          # tanda hubung lunak (soft hyphen)
    teks = re.sub(r"-\s*\n\s*", "", teks)        # pemenggalan akhir baris
    return re.sub(r"\s+", " ", teks).strip().lower()


def halaman(mentah, kutipan):
    """Nomor halaman PDF (penanda <!-- Page N -->) tempat kutipan berada.
    Dicari per halaman lebih dahulu; bila kutipan melintasi batas halaman,
    dilaporkan halaman tempat kutipan dimulai."""
    norm_kutip = normal(kutipan)
    halaman_teks, nomor = [], None
    for b in re.split(r"(<!-- Page \d+ -->)", mentah):
        m = re.match(r"<!-- Page (\d+) -->", b)
        if m:
            nomor = m.group(1)
        else:
            halaman_teks.append((nomor, b))
    for nomor, b in halaman_teks:
        if norm_kutip in normal(b):
            return nomor
    for (nomor, b), (_, lanjut) in zip(halaman_teks, halaman_teks[1:]):
        if norm_kutip in normal(b + " " + lanjut):
            return nomor
    return None


_cache_sumber = {}


def _baca_sumber(f):
    """(teks mentah, teks normal) berkas sumber; disimpan agar tiap berkas dinormalkan sekali."""
    kunci = (f, f.stat().st_mtime_ns)
    if kunci not in _cache_sumber:
        mentah = f.read_text(encoding="utf-8")
        _cache_sumber[kunci] = (mentah, normal(mentah))
    return _cache_sumber[kunci]


def cari_bukti(akar, berkas, kutipan):
    """Cari kutipan di sumber utama <akar>/<berkas>, lalu di versi kedua
    <akar>/versi2/<berkas>. Kembalikan (versi, berkas_relatif, mentah):
    versi "utama" atau "versi kedua" bila cocok; None bila berkas ada tetapi
    kutipan tidak ditemukan; "tanpa berkas" bila kedua berkas tidak ada."""
    kandidat = [("utama", Path(berkas)), ("versi kedua", Path(VERSI_KEDUA) / berkas)]
    ada = [(v, rel) for v, rel in kandidat if (akar / rel).exists()]
    if not ada:
        return "tanpa berkas", None, None
    nk = normal(kutipan)
    for versi, rel in ada:
        mentah, norm = _baca_sumber(akar / rel)
        if nk in norm:
            return versi, rel, mentah
    return None, [str(rel) for _, rel in ada], None


def _r(ekspresi):
    p = subprocess.run(["Rscript", "-e", ekspresi], capture_output=True, text=True, timeout=300)
    return p.stdout + p.stderr


def teks_rd(paket, topik):
    return _r(f'db <- tools::Rd_db("{paket}"); '
              f'tools::Rd2txt(db[["{topik}.Rd"]], options = list(underline_titles = FALSE))')


def kunci_sitasi(baris):
    """Kunci bib yang disitasi pada satu baris prosa (bukan rujukan silang)."""
    keluar = []
    for k in re.findall(r"(?<![\w.])@([A-Za-z][\w:.-]*[\w])", baris):
        if not re.match(r"(fig|tbl|eq|sec|Fig|Tbl|Eq|Sec)-", k):
            keluar.append(k)
    return keluar


def paragraf_baris(prosa_baris):
    """Peta nomor baris -> teks paragrafnya (baris prosa berurutan yang tidak kosong,
    dipisah baris kosong, judul, atau pagar :::). Dipakai agar klaim dapat tertaut ke
    sitasi di kalimat pertama paragraf (sitasi sekali per paragraf, 2026-11-12)."""
    peta, kelompok, sebelum = {}, [], None

    def tutup():
        teks = "\n".join(b for _, b in kelompok)
        for n, _ in kelompok:
            peta[n] = teks

    for nomor, b in prosa_baris:
        t = b.strip()
        putus = not t or re.match(r"^#{1,6}\s", t) or t.startswith(":::") or (sebelum is not None and nomor != sebelum + 1)
        if putus and kelompok:
            tutup()
            kelompok = []
        if t and not re.match(r"^#{1,6}\s", t) and not t.startswith(":::"):
            kelompok.append((nomor, b))
        sebelum = nomor
    if kelompok:
        tutup()
    return peta

def periksa(qmd, bab, prosa_baris, bib_teks):
    """Kembalikan (daftar_masalah, ringkasan). Fikstur uji memakai registri di foldernya sendiri."""
    folder = qmd.parent if (qmd.parent / "klaim.json").exists() else AKAR / "harness"
    ref = json.loads((folder / "referensi.json").read_text(encoding="utf-8"))
    klaim = json.loads((folder / "klaim.json").read_text(encoding="utf-8"))
    # Fikstur uji dengan folder sumber/ sendiri memakai folder itu; selain itu harness/sumber/
    akar_sumber = folder / "sumber" if folder != AKAR / "harness" and (folder / "sumber").is_dir() else SUMBER
    klaim_bab = [k for k in klaim if k["bab"] == bab]
    masalah, ringkas = [], []

    # 1. Setiap sitasi punya klaim terverifikasi untuk kalimat itu, atau (sitasi sekali per
    #    paragraf, 2026-11-12) untuk kalimat lain di paragraf yang sama
    dipakai = set()
    par_baris = paragraf_baris(prosa_baris)
    for nomor, b in prosa_baris:
        for kunci in kunci_sitasi(b):
            dipakai.add(kunci)
            cocok = [k for k in klaim_bab if k["kunci"] == kunci
                     and (k["penanda"] in b or k["penanda"] in par_baris.get(nomor, ""))]
            if not cocok:
                masalah.append(f"baris {nomor}: sitasi @{kunci} tanpa klaim terverifikasi di klaim.json "
                               f"(kalimat: {b.strip()[:80]}…)")

    # 2. Setiap pustaka yang disitasi terdaftar, terverifikasi, dan beridentitas
    entri_bib = dict(re.findall(r"@\w+\{([^,]+),(.*?)\n\}", bib_teks, flags=re.S))
    for kunci in sorted(dipakai):
        if kunci not in entri_bib:
            masalah.append(f"@{kunci} tidak ada di pustaka.bib")
            continue
        r = ref.get(kunci)
        if not re.search(r"\b(doi|isbn|url)\s*=", entri_bib[kunci]):
            # Pengecualian beralasan (keputusan penulis 2026-11-14): dokumen tanpa alamat daring
            # (mis. salindia lembaga) boleh tanpa DOI/ISBN/URL bila referensi.json mencatat
            # "tanpa_id" berisi alasan dan salinan lokal yang benar-benar ada di harness/sumber/.
            tid = (r or {}).get("tanpa_id") or {}
            salinan = tid.get("salinan_lokal", "")
            if not (tid.get("alasan") and salinan and (akar_sumber / salinan).exists()):
                masalah.append(f"@{kunci} tidak punya DOI, ISBN, atau URL di pustaka.bib "
                               "(atau catat \"tanpa_id\" {alasan, salinan_lokal} di referensi.json)")
        if not r or not r.get("verifikasi"):
            masalah.append(f"@{kunci} belum diverifikasi di referensi.json")

    # 3. Setiap klaim bab ini: penandanya masih ada, buktinya terbukti
    teks_qmd = qmd.read_text(encoding="utf-8")
    rd_cache, otomatis, manual, kedua = {}, 0, 0, 0
    for k in klaim_bab:
        if k["penanda"] not in teks_qmd:
            masalah.append(f"klaim usang: penanda '{k['penanda'][:60]}' tidak ada lagi di {qmd.name}")
            continue
        if k.get("sitasi_di"):
            # Kalimat klaim tanpa @kunci karena sumbernya sudah disitasi lebih awal di paragraf
            # yang sama (keputusan 2026-11-12). Klaim tetap diperiksa terhadap sumbernya (di bawah)
            # dan harus tertaut: paragrafnya menyitasi @kunci sebelum penanda.
            tertaut = False
            for par in set(par_baris.values()):
                i = par.find(k["penanda"])
                if i >= 0 and k["kunci"] in kunci_sitasi(par[:i]):
                    tertaut = True
            if not tertaut:
                masalah.append(f"klaim @{k['kunci']} bertanda sitasi_di ('{k['sitasi_di'][:40]}'), tetapi paragraf "
                               f"penanda '{k['penanda'][:50]}' tidak menyitasi @{k['kunci']} sebelumnya; "
                               "sitasi sumber itu pada kemunculan pertama di paragraf")
        for bukti in k["bukti"]:
            jenis, kutip = bukti["jenis"], bukti.get("kutipan", "")
            label = f"@{k['kunci']} ({jenis})"
            if jenis == "berkas":
                versi, rel, mentah = cari_bukti(akar_sumber, bukti["berkas"], kutip)
                if versi == "tanpa berkas":
                    masalah.append(f"{label}: sumber lokal {bukti['berkas']} tidak tersedia "
                                   f"(sumber utama maupun {VERSI_KEDUA}/)")
                    continue
                if versi is None:
                    masalah.append(f"{label}: kutipan tidak ditemukan di {' maupun '.join(rel)}: '{kutip}'")
                    continue
                hlm = halaman(mentah, kutip)
                letak = f"hlm. PDF {hlm}" if hlm else "tanpa penanda halaman"
                ringkas.append(f"{label} {rel} [{versi}] {letak}, {bukti.get('lokasi', '')}: terbukti")
                otomatis += 1
                if versi != "utama":
                    kedua += 1
            elif jenis in ("rd", "deskripsi", "citation"):
                if jenis == "rd":
                    kunci_cache = (bukti["paket"], bukti["topik"])
                    if kunci_cache not in rd_cache:
                        rd_cache[kunci_cache] = teks_rd(*kunci_cache)
                    sumber = rd_cache[kunci_cache]
                elif jenis == "deskripsi":
                    sumber = _r(f'cat(unlist(packageDescription("{bukti["paket"]}")), sep = "\\n")')
                else:
                    sumber = _r('print(citation(), style = "text")')
                if normal(kutip) not in normal(sumber):
                    masalah.append(f"{label}: kutipan tidak ditemukan: '{kutip}'")
                    continue
                ringkas.append(f"{label} {bukti.get('paket', 'R')} {bukti.get('topik', '')}: terbukti")
                otomatis += 1
            elif jenis == "hitung":
                keluar = _r(f"cat(format({bukti['kode']}, digits = 15))").strip().splitlines()[-1]
                try:
                    nilai = float(keluar)
                except ValueError:
                    masalah.append(f"{label}: kode tidak menghasilkan bilangan: {keluar}")
                    continue
                harap = float(bukti["nilai_sumber"])
                if abs(nilai - harap) > float(bukti["toleransi"]) * abs(harap):
                    masalah.append(f"{label}: hitungan {nilai:g} ≠ nilai sumber {harap:g}")
                    continue
                ringkas.append(f"{label}: hitung ulang {nilai:.4g} cocok dengan sumber {harap:g}")
                otomatis += 1
            elif jenis == "web":
                kurang = [f for f in ("url", "diakses", "kutipan") if not bukti.get(f)]
                if kurang:
                    masalah.append(f"{label}: bukti web tanpa {', '.join(kurang)}")
                    continue
                ringkas.append(f"{label} {bukti['url']} (diakses {bukti['diakses']}): diverifikasi saat menulis")
                manual += 1
            else:
                masalah.append(f"{label}: jenis bukti tidak dikenal")
    ringkas.insert(0, f"{len(dipakai)} pustaka disitasi; {otomatis} bukti diperiksa ulang otomatis, "
                      f"{manual} bukti web tercatat"
                      + (f"; {kedua} bukti hanya cocok di sumber versi kedua ({VERSI_KEDUA}/)" if kedua else ""))
    return masalah, ringkas
