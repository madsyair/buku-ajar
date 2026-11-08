# Harness dan gerbang mutu

*Harness engineering*: setiap aturan yang dapat diperiksa mesin dijadikan **gerbang yang dapat dieksekusi**, dijalankan di setiap putaran, dan diuji dengan fikstur gagal/lulus. Reviewer manusia dan agen hanya memeriksa yang tidak dapat diperiksa mesin. Skrip ada di `scripts/` skill; cara memasangnya di proyek di `scripts/README.md`.

## 1. Menjalankan

```bash
python3 harness/harness.py --buku <buku> --bab bab02            # tanpa render (agen bab)
python3 harness/harness.py --buku <buku> --bab bab02 --render   # dengan render (orkestrator, berurutan)
bash harness/uji_harness.sh                                     # uji regresi harness
python3 harness/harness.py --tag-pdf <buku>/_book/<buku>.pdf    # G-TAG saja pada PDF jadi
python3 harness/harness.py --huruf-pdf <pdf>... [--huruf springer]  # G-HURUF saja
```

Keluaran: `[LULUS]/[GAGAL] G-…` per gerbang, rincian temuan (baris qmd atau knit.md), dan laporan `harness/laporan/<buku>-<bab>.md` (tabel status, rincian, bukti referensi, WARNING EYD yang perlu ditinjau manual). Kode keluar 0 = semua gerbang lulus. Bab **tidak** dianggap selesai sebelum Status LULUS.

Variabel lingkungan: `JUDUL_GAMBAR`, `ATRIBUSI_MANUAL`, `KONJUNGSI`, `TEPI`, `TAG`, `LN`, `DRAF` (bawaan 1; set 0 hanya untuk masa transisi atau versi terbit, dan catat alasannya), `SKILL_EYD`, `SKILL_GAYA` (jalur skrip skill pendukung bila tidak ditemukan otomatis), `RETICULATE_PYTHON`.

## 2. Daftar gerbang

| Gerbang | Tahap | Memeriksa | Sumber aturan |
|---|---|---|---|
| G-KODE | rajut | semua chunk R/Python berjalan saat `knitr::knit` (menghasilkan `build/<bab>.knit.md`) | kode dijalankan |
| G-LAMPIRAN | rajut | `knitr::purl` → `lampiran-kode/<buku>/<bab>.R` berjalan mandiri dari foldernya; chunk Python → `<bab>_gambar.py` berjalan mandiri; setiap chunk TikZ → `.tex` mandiri terkompilasi | reproduksi pembaca |
| G-ANGKA | statis | angka desimal, persen, ribuan di prosa dan `fig/tbl-cap` teks diketik tangan; pengecualian `angka-tetap` per bab | angka inline |
| G-KELUARAN | statis | komentar kode yang menyerupai keluaran (`# 0.21`, `# [1]`) | keluaran asli |
| G-PYTHON | statis | chunk Python memakai objek `r.` atau menghitung (`numpy.random`, `scipy.stats`, `statsmodels`, `pymc`) | R menghitung, Python menggambar |
| G-LEBAR-KODE | statis | baris R > `batas_kode` (bawaan 72), Python > `batas_kode_python` (79) karakter; batas dibaca dari `konfig.json` | kode muat di kolom (ukuran mono dihitung `huruf.py`) |
| G-LEBAR-KELUARAN | rajut | keluaran `##` > `batas_keluaran` (bawaan 78) karakter (`TEPI=1`); `huruf.py` menulis `options(width = batas_keluaran − 3)` ke `<buku>/.Rprofile` | tanpa luapan tepi |
| G-BOCOR | rajut | peringatan, galat, repr objek, `fig-cap` yang tak dievaluasi, `Inf/NaN/NA` di prosa | tampilan bersih |
| G-RUJUKAN | statis | `@fig/@tbl/@eq/@sec` tanpa sasaran; label ganda di buku; label yang tidak pernah dirujuk; kunci sitasi tak ada di bib | rujukan |
| G-SITASI | statis | sitasi berlokasi (`[@k, hlm. 3]`); nama penulis manual di kalimat bersitasi kurung (nama diambil otomatis dari `pustaka.bib` + konfig `penulis`) | penulis–tahun tanpa lokasi |
| G-ATRIBUSI | statis | manual/lembaga/dokumentasi sebagai subjek ("Menurut Panduan…", "BPS menyatakan"); sitasi naratif untuk entri bib berpenulis lembaga | subjek hanya penulis orang |
| G-REFERENSI | statis + R | setiap sitasi punya klaim di `klaim.json` untuk kalimat itu; kutipan bukti benar-benar ada di sumber (berkas, Rd, DESCRIPTION, citation, hitung ulang); entri bib ber-DOI/ISBN/URL dan terverifikasi di `referensi.json`; penanda klaim usang | registri klaim |
| G-JUDUL | statis + rajut | judul tabel/gambar > 12 kata atau lebih dari satu frasa; frasa panel > 6 kata; multipanel tanpa `label_panel()` atau keterangan tanpa (a)(b); arah panel ("kiri", "panel kanan"); judul/subjudul berupa kalimat tanya | keputusan judul |
| G-PERSAMAAN | statis | "Persamaan" berkapital di tengah kalimat; `@eq-` di awal kalimat | "persamaan" huruf kecil |
| G-KONJUNGSI | statis | koma sebelum penghubung subordinatif di tengah kalimat; ", karena itu" di tengah kalimat; pengecualian per kalimat `konjungsi-abaikan` | kajian koma konjungsi |
| G-LARANGAN | statis | kata terlarang di prosa dan keterangan (bawaan: Sokratik/Socrates/Feynman); konfig `larangan` | nama teknik tidak ditulis |
| G-ISTILAH | statis | istilah yang sudah diganti keputusan penulis (konfig `istilah_terlarang`); pengecualian `istilah-abaikan` | keputusan istilah |
| G-LN | statis (`LN=1`) | `\log` tanpa subskrip basis di rumus prosa dan `fig/tbl-cap` (logaritma natural ditulis `\ln`); `\log_{10}`, `\log_2` lulus; blok kode, R inline, kode sebaris, dan berkas kode dilewati; pengecualian `ln-abaikan`. Fikstur: `uji-buku/babln.qmd` (GAGAL), `babbaik.qmd` memuat `\ln`, `\log_{10}`, `log()` (LULUS); fungsi `masalah_ln()` juga diuji langsung | ln di naskah, kode `log` |
| G-HALJUDUL | statis | `subtitle:` di `_quarto.yml`; `date` bukan ISO; `date-format` tanpa "[Draf revisi ke-N · ]" (`DRAF=1`) | halaman judul |
| G-EYD | rajut | `periksa.py` skill eyd pada prosa hasil rajut: 0 ERROR (WARNING ditinjau manual); pengecualian `eyd-abaikan` | EYD V |
| G-GAYA | rajut | pemeriksa gaya skill math-article bila ada, atau cadangan ("di mana", koma *tetapi/sedangkan/melainkan*, koma setelah penghubung antarkalimat) | gaya |
| G-PARAGRAF | rajut | paragraf isi < 2 atau > 6 kalimat | paragraf padu |
| G-SLOP | rajut | frasa basa-basi dan kosakata khas tulisan mesin (daftar `SLOP_ID`); pengecualian `gaya-abaikan` | humanizer-id |
| G-PENGGALAN | statis / render | `penggalan.py` memperbarui daftar pengecualian; pemenggal lulus contoh EYD V; setelah render: babel indonesian dan daftar dimuat, istilah asing bertanda Inggris, **nama tidak terpenggal** di PDF, setiap penggalan kata Indonesia di PDF sah menurut EYD V, Word: pemenggalan otomatis dan bahasa id-ID | pemenggalan |
| G-RENDER | `--render` | `quarto render` PDF + Word dalam satu proses tanpa galat; peringatan rujukan/sitasi | render |
| G-LOG | `--render` | log LaTeX akhir (bukan log TikZ) tanpa "Rerun to correct" (hook `lastpage`), "Label(s) may have changed", "Rerun to get cross-references/outlines right", atau label "multiply defined". Obat: `latex-min-runs: 4` di `_quarto.yml` dan `\endhead` longtable di `preamble.tex`. Perlu `latex-clean: false`. Fikstur `uji-buku/log/{rerun,ganda,bersih}.txt` (berakhiran .txt karena `kemas_sumber.py` membuang `*.log`) diuji lewat `masalah_log_latex()` | daftar isi dan rujukan stabil |
| G-TEPI | `--render` | Overfull hbox > 3 pt di log LaTeX (rumus, tabel, kode, teks), dilaporkan dengan judul bab dan baris .tex; log LuaLaTeX memakai format *Overfull* yang sama dengan XeLaTeX | tanpa luapan tepi |
| G-TAG | `--render` (`TAG=1`) atau `--tag-pdf` | PDF bertag: `pdfinfo` melaporkan `Tagged: yes`; pohon struktur (`pdfinfo -struct`) berakar Document dan memuat H1, P, dan Figure; `/Lang` = id-ID (pikepdf bila ada). Gagal bila `pdf-engine` bukan `lualatex` atau partial `doc-class.tex` (`\DocumentMetadata`) tidak dipasang. Fikstur: `uji-buku/tag-tanpa.pdf` (GAGAL) dan `tag-baik.pdf` (LULUS), sumbernya di `uji-buku/sumber-tag/`. `TAG=0` hanya untuk proyek lama yang belum pindah ke LuaLaTeX, dengan alasan tercatat | PDF bertag (butir 35) |
| G-HURUF | `--render` (`HURUF=1`) atau `--huruf-pdf` | Setiap huruf tersemat (`pdffonts`, awalan subset dibuang) di PDF buku dan PDF gambar (`*_files/figure-pdf/`, `gambar/`) diawali salah satu prefiks keluarga opsi `huruf` di `konfig.json` (`izin` di `_bersama/huruf.py`: teks, matematika, mono, dan pasangan TikZ-nya); log LaTeX tanpa "Missing character" (`\tracinglostchars=2` di `preamble.tex`). Huruf asing (DejaVu, Inter, STIXGeneral, CMR pada opsi Times) berarti glif jatuh ke huruf cadangan lain. Fikstur: `uji-buku/huruf/huruf-baik.pdf` (LULUS untuk libertinus, GAGAL untuk springer) dan `huruf-asing.pdf` (GAGAL) | satu keluarga huruf (butir 34) |

Pengecualian hanya lewat `harness/pengecualian.json` dan **wajib beralasan**:

```json
{
 "angka-tetap": {"buku3/bab04": [{"teks": "95%", "alasan": "tingkat interval yang dipilih penulis"}]},
 "eyd-abaikan": [{"temuan": "…", "kategori": "…", "alasan": "…"}],
 "gaya-abaikan": [{"pola": "…", "alasan": "…"}],
 "konjungsi-abaikan": ["potongan ±40 karakter unik dari kalimat yang komanya sah"],
 "larangan-abaikan": [],
 "istilah-abaikan": [],
 "ln-abaikan": ["potongan teks temuan G-LN yang sah, mis. kutipan rumus sumber"]
}
```

## 3. Konfigurasi proyek (`harness/konfig.json`)

Semua yang khusus proyek ada di sini, bukan di kode harness:

```json
{
 "bersama": "_bersama",
 "lampiran": "lampiran-kode",
 "id_bab_polos": [],
 "penulis": ["Bürkner", "Štrumbelj"],
 "larangan": [
  {"pola": "\\bsokrat\\w*|\\bsocrat\\w*", "saran": "nama teknik pengajaran tidak ditulis"},
  {"pola": "\\bfeynman\\b", "saran": "nama teknik pengajaran tidak ditulis"}
 ],
 "istilah_terlarang": [
  {"pola": "\\bderau\\b", "saran": "pakai *noise* (keputusan penulis 2026-11-06)"},
  {"pola": "\\btaksiran\\b|\\bpenaksir\\b|\\bditaksir\\b|\\bmenaksir\\b", "saran": "estimasi/estimator (keputusan penulis 2026-11-06)"},
  {"pola": "\\bkemungkinan maksimum\\b", "saran": "*maximum likelihood* (keputusan penulis 2026-11-06)"},
  {"pola": "\\bpendugaan area kecil\\b", "saran": "estimasi area kecil (keputusan penulis 2026-11-06)"},
  {"pola": "\\btarikan acak\\b|\\bditarik dari (?:distribusi|prior|posterior)\\b", "saran": "membangkitkan / nilai bangkitan (keputusan 2026-11-06)"}
 ],
 "kemasan": {"buku1": "R 4.6, R dasar saja"}
}
```

Kunci `larangan` menggantikan daftar bawaan; tulis ulang kedua pola bawaan bila menambah larangan. Pola `istilah_terlarang` harus cukup sempit agar arti umum tidak tertangkap ("kemungkinan besar" tetap sah, jadi jangan melarang "kemungkinan").

## 4. Menambah gerbang dari keputusan penulis

Setiap kali penulis membuat **keputusan gaya baru**, orkestrator menjalankan prosedur ini (lihat juga `loop-kerja.md`, loop D):

1. **Catat keputusan** bertanggal di `KEPUTUSAN-RANCANGAN.md`: isi, cakupan (semua buku/satu buku), berlaku surut atau tidak, nama gerbang yang menegakkannya.
2. **Klasifikasikan** apakah keputusan dapat diperiksa mesin:
   - **pola kata** (istilah, larangan kata) → tambah entri `istilah_terlarang` atau `larangan` di `konfig.json`; tidak perlu menyunting kode;
   - **struktur qmd** (judul, label, opsi chunk, kotak) → fungsi baru di `harness.py` dengan pola `gerbang_x(qmd, peng)` yang memanggil `catat("G-X", lulus, rincian)`, lalu dipanggil di `main()` (boleh di balik variabel lingkungan `X=1` selama masa transisi);
   - **hasil rajut** (keluaran, prosa terevaluasi) → fungsi yang menerima `md` (`build/<bab>.knit.md`);
   - **hasil render** (PDF, log LaTeX, Word) → fungsi di cabang `if a.render:`;
   - **tidak dapat diperiksa mesin** (kepaduan, kebenaran isi) → butir daftar periksa reviewer di berkas agen yang relevan.
3. **Pesan temuan** menyebut baris, potongan teks, dan perbaikan yang diharapkan ("tulis faktanya langsung dengan sitasi [@kunci]"), bukan sekadar "salah".
4. **Fikstur**: tambah satu bab gagal `harness/uji-buku/bab<nama>.qmd` yang hanya melanggar aturan baru, tambahkan namanya ke daftar `GAGAL` di `uji_harness.sh`, dan pastikan `babbaik.qmd` tetap LULUS. Untuk gerbang render, pisahkan pemeriksaan teks dari pencarian berkas (pola `masalah_log_latex(teks)` di G-LOG, `masalah_ln(teks)` di G-LN) dan uji fungsinya langsung pada fikstur teks di `uji_harness.sh`, tanpa render. Jalankan `bash harness/uji_harness.sh` sampai semua "benar".
5. **Audit semua buku**: jalankan gerbang baru pada semua bab semua buku (buku induk dan kunci) tanpa render; kumpulkan temuan per bab; jalankan putaran penyuntingan per kelompok bab (instruksi tertulis di `naskah-bersama/instruksi-<topik>-<tanggal>.md`); naikkan nomor "Draf revisi ke-N" buku yang berubah dan catat di `REVISI.md`.
6. **Komit** harness, fikstur, konfig, dan keputusan dalam satu titik simpan git ("Harness: G-X untuk keputusan …").

Kerangka fungsi baru:

```python
def gerbang_contoh(qmd, peng):
    """Keputusan penulis YYYY-MM-DD: <isi keputusan>."""
    prosa, chunk = pilah_qmd(qmd.read_text(encoding="utf-8"))
    abaikan = peng.get("contoh-abaikan", [])
    masalah = []
    for nomor, b in prosa:
        bersih = re.sub(r"`[^`]*`", " ", b)       # buang kode inline
        if POLA.search(bersih) and not any(a in bersih for a in abaikan):
            masalah.append(f"baris {nomor}: … — <perbaikan>")
    catat("G-CONTOH", not masalah, "\n".join(masalah[:40]))
```

Gerbang yang terlalu ketat (banyak positif palsu) lebih merugikan daripada tidak ada: setiap positif palsu harus dapat dikecualikan per kalimat dengan alasan, dan polanya diperbaiki bila pengecualian menumpuk.

## 5. Registri klaim dan penulisan aman

Lihat `data-dan-sumber.md` untuk format. Skrip tambah klaim (dijalankan di bawah `flock`):

```python
# tambah_klaim.py — flock <scratchpad>/klaim.lock python3 tambah_klaim.py
import json, pathlib
p = pathlib.Path("harness/klaim.json")
klaim = json.loads(p.read_text(encoding="utf-8"))
BAB = "buku3/bab05"
baru = [ {"bab": BAB, "kunci": "gelman2021", "penanda": "…",
          "bukti": [{"jenis": "berkas", "berkas": "ros.md", "lokasi": "bag. 15.6",
                     "kutipan": "…"}]} ]
klaim = [k for k in klaim if k["bab"] != BAB] + baru   # ganti entri bab sendiri saja
p.write_text(json.dumps(klaim, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
```

Sebelum mencatat, cek kutipan: `grep -F "potongan kutipan" harness/sumber/ros.md` (atau `tools::Rd2txt` untuk Rd).

## 6. Pemeriksaan render

Render dijalankan **orkestrator, berurutan** (satu buku sekali jalan, tidak paralel dengan agen lain yang merajut buku yang sama), setelah semua agen bab selesai:

```bash
python3 harness/harness.py --buku <buku> --bab <bab-terakhir-diubah> --render
```

Setelah render: G-RENDER, G-LOG (log LaTeX akhir stabil, tanpa label ganda), G-TAG (PDF bertag), G-HURUF (huruf tersemat hanya keluarga opsi), G-TEPI (daftar luapan per bab dengan lebar pt dan baris .tex), dan G-PENGGALAN (audit PDF). Sekali per buku editor mengukur panjang baris (median dan persentil-95 karakter per baris prosa dari `pdftotext -layout`, harus 40–70; `aturan-gaya-dan-tampilan.md` bagian 8) (G-HURUF memastikan `pdffonts` hanya memuat keluarga opsi huruf). Sesudah itu editor/pembaca memeriksa tampilan (lihat `agents/09-editor.md`): halaman bab, gambar dan catatan tidak terpisah, label tidak tertimpa, blok kode tidak terbelah, tidak ada "??" rujukan, tanda air dan "Draf revisi ke-N" tampil, paragraf menjorok di PDF dan Word.

## 7. Batas harness

Harness tidak memeriksa kebenaran isi, kecocokan narasi dengan gambar, ambang tipis, kepaduan antarparagraf, atau kesesuaian soal dengan bab. Semua itu tugas peninjau independen (`loop-kerja.md`). Lulus harness adalah **syarat perlu**, bukan bukti mutu.
