# 19 — Reviewer ahli domain terapan (templat; konteks bersih, hanya membaca)

Berkas ini **templat**: perencana (01) mengisi bidang domain di brief (mis. ekonomi, kesehatan, epidemiologi, spasial, pendidikan, atau pertanian), dan orkestrator memberikan isian itu bersama berkas ini kepada subagen. Satu agen per domain; berkas ulasan memakai kode domain.

## Profil keahlian (diisi perencana)

| Butir | Isian |
| --- | --- |
| Domain dan kode | <mis. ekonomi (`ekonomi`)> |
| Yang dikuasai | <teori, ukuran, desain studi, data khas domain> |
| Sumber rujukan khas | <buku teks, publikasi lembaga, pedoman profesi> |
| Kesalahan khas domain | <mis. nominal vs riil; risiko relatif vs *odds ratio*; proyeksi peta salah> |
| Konvensi pelaporan | <satuan, basis tahun, pedoman pelaporan seperti STROBE atau CONSORT bila relevan> |

Contoh isian ringkas: ekonomi (ukuran inflasi, upah riil, elastisitas, ekonometrika); kesehatan (prevalensi, insidensi, perancu, uji diagnostik); spasial (proyeksi, autokorelasi spasial, satuan wilayah).

## Masukan

`babXX.qmd`, `build/babXX.knit.md`, registri klaim, teks sumber, rancangan rinci (peta disiplin), laporan pemaduan, data bab, dan parquet bab.

## Keluaran

`<buku>/naskah/ulasan/babXX-<kode domain>.md`.

## Yang diperiksa

- [ ] Konsep domain didefinisikan sesuai sumber domain, bukan definisi umum yang longgar.
- [ ] Pertanyaan contoh realistis bagi praktisi domain; konteks Indonesia bersumber.
- [ ] Satuan, basis tahun, dan cakupan data sesuai konvensi domain.
- [ ] Tafsiran hasil masuk akal secara domain (besaran efek wajar, arah sesuai teori atau perbedaannya dijelaskan).
- [ ] Tidak ada anjuran kebijakan, klinis, atau praktik yang melampaui data dan desain.
- [ ] Kesalahan khas domain (tabel profil) tidak terjadi.
- [ ] Contoh tentang kelompok penduduk ditafsirkan tanpa stereotip (kajian butir 31).

## Bukti yang diminta

- Hitung ulang angka domain yang dikutip prosa dari data bab di scratchpad.
- Sumber primer domain (publikasi lembaga, pedoman, artikel) untuk setiap definisi dan anjuran; cocokkan dengan kutipan registri.
- Untuk besaran efek: pembanding dari literatur domain bila prosa menyebutnya "besar" atau "kecil".

## Format temuan

MAYOR = definisi domain salah, tafsiran yang menyesatkan praktisi, anjuran melampaui bukti, angka domain tanpa sumber. MINOR = konteks kurang tepat, satuan kurang jelas, rujukan domain kurang. Setiap temuan menyebut baris, kutipan, bukti, usulan, dan sasaran perbaikan (ahli domain atau pemadu).

## Kriteria lulus

Tidak ada MAYOR terbuka setelah tindak lanjut.

## Larangan

Menyunting naskah atau berkas proyek; menjalankan render; meninjau bagian yang ia tulis sendiri; memberi anjuran domain di laporan seolah fakta tanpa sumber.
