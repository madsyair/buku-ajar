# Rancangan rinci <Buku N> — <Judul> (<tanggal>)

Status: **diputuskan saat perancangan rinci <tanggal>, dapat diubah penulis** (kecuali butir bertanda "keputusan penulis <tanggal>").

- Judul: **<Judul>** (tanpa subjudul).
- Mesin dan versi: <…>.
- Anggaran isi: <…> halaman; dengan bagian depan ±<…>.

## Struktur bab

Kolom "Disiplin": kode disiplin yang menulis bab (lebih dari satu untuk bab multidisiplin; rinci di "Penugasan bagian"). Kolom "Ingat": kotak rujukan (maks. satu paragraf, ≤ 2 per bab) dengan nomor dan judul **final** bab sumber. Kolom "Sumber utama": kunci dan bab/bagian sumber untuk `lokasi` registri klaim (tidak dicetak).

| Bagian | Bab | Judul | Isi pokok | Disiplin | Data (paket::nama atau simulasi; status) | Contoh utama | Ingat | Sumber utama | Hlm. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I | 1 | … | … | … | … | … | … | … | … |
| | | **Jumlah** | | | | | | | **…** |

## Peta disiplin (buku multidisiplin)

Isi bila brief menyatakan buku multidisiplin; buku satu disiplin cukup menulis "satu disiplin: <nama>".

| Disiplin (kode) | Bab yang memuatnya | Penulis ahli (04a) | Reviewer ahli | Catatan |
| --- | --- | --- | --- | --- |

### Penugasan bagian

Satu baris per subbab. "Jembatan pemadu" untuk paragraf penghubung yang ditulis 04b. Berkas bagian `babXX-<kode>.qmd`.

| Bab | Subbab | Disiplin | Penulis ahli | Berkas bagian | Reviewer ahli | Reviewer lintas bagian |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 5.1 | pemodelan statistik | 04a `model` | `bab05-model.qmd` | 16 | 05, 07, 09 |
| 5 | 5.1 → 5.2 | jembatan pemadu | 04b | `bab05.qmd` | 16, 17, 20 | 07, 09 |

### Notasi dan istilah lintas disiplin

| Konsep | Simbol/istilah di buku | Kebiasaan disiplin lain | Bunyi padanan (disebut sekali) |
| --- | --- | --- | --- |
| koefisien | $\beta_j$ | $w_j$ (*machine learning*) | "di *machine learning* koefisien ini disebut bobot" |

### Bab sumber kotak Ingat (judul final)

| Buku lain | Bab | Judul |
| --- | --- | --- |

### Label bab dan label tetap lintas bab

`sec-…` per bab; label yang dirujuk lintas bab: `fig-…`, `sec-…`.

## Kepemilikan topik (satu topik, satu pemilik)

| Topik | Pemilik | Di buku lain | Di buku ini |
| --- | --- | --- | --- |

## Enam pertanyaan perencanaan per metode

| Bab | Metode | Apa masalahnya | Mengapa bukan cara naif | Kapan dipakai / asumsi | Bagaimana menghitung | Bagaimana menafsirkan | Kapan gagal |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Jembatan istilah

| Istilah lama | Istilah baru | Bab | Bunyi jembatan |
| --- | --- | --- | --- |

## Data yang sudah diperiksa (Rscript, <tanggal>)

| Paket (versi) | Dataset | Dimensi | Peubah kunci, NA | Status (kutipan Rd) | Bab | Sitasi |
| --- | --- | --- | --- | --- | --- | --- |

### Dataset yang diperiksa dan tidak dipakai

| Paket (versi) | Dataset | Alasan |
| --- | --- | --- |

## Halaman sebenarnya (diisi setelah render)

| Bab | Anggaran | Sebenarnya | Catatan |
| --- | --- | --- | --- |
