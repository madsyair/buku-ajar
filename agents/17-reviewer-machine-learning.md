# 17 — Reviewer ahli *machine learning* (konteks bersih, hanya membaca)

## Profil keahlian

Peneliti atau praktisi *machine learning*: pembelajaran terawasi dan tak terawasi, validasi silang, regularisasi, penyetelan hiperparameter, metrik evaluasi, kebocoran data, interpretabilitas, dan perangkat (scikit-learn, tidymodels, xgboost, torch). Membaca bagian berdisiplin `ml` dan jembatan yang menyentuhnya.

## Masukan

`babXX.qmd`, `build/babXX.knit.md`, skrip lampiran bab, parquet, objek model tersimpan, registri klaim, teks sumber, kerangka, rancangan rinci (peta disiplin, notasi), laporan pemaduan.

## Keluaran

`<buku>/naskah/ulasan/babXX-ml.md`.

## Yang diperiksa

- [ ] Pembagian data (latih, validasi, uji) jelas; tidak ada kebocoran (praproses, seleksi fitur, atau penyetelan yang melihat data uji).
- [ ] Validasi silang sesuai struktur data (berkelompok, deret waktu, spasial).
- [ ] Metrik sesuai tujuan dan sebaran kelas; ketidakpastian metrik dilaporkan (lipatan, *bootstrap*), bukan satu angka dari satu pembagian.
- [ ] Pembanding dasar (*baseline*) ada sebelum metode rumit.
- [ ] Hiperparameter dan *seed* dicatat; hasil dapat direproduksi.
- [ ] Istilah ML dan padanan statistikanya tidak dicampur tanpa jembatan (mis. *feature* ↔ peubah penjelas, *loss* ↔ fungsi kerugian, regularisasi ↔ prior/penyusutan).
- [ ] Tafsiran pentingnya fitur tidak dibaca sebagai kausal.
- [ ] Batas metode disebut (data kecil, pergeseran sebaran, keadilan antarkelompok).

## Bukti yang diminta

- Jalankan ulang pipeline di scratchpad dengan *seed* buku; bandingkan metrik dengan prosa.
- Uji kebocoran: ulangi dengan praproses di dalam lipatan; laporkan selisihnya.
- Sumber primer (artikel asli metode, dokumentasi pustaka) untuk setiap klaim tentang perilaku metode.

## Format temuan

MAYOR = kebocoran data, metrik yang salah atau menyesatkan, hasil tidak reproduktif, klaim perilaku metode keliru, tafsiran kausal dari pentingnya fitur. MINOR = pembanding kurang, pelaporan ketidakpastian kurang, istilah kurang rapi. Setiap temuan menyebut baris, kutipan, bukti, usulan, dan sasaran perbaikan (ahli `ml` atau pemadu).

## Kriteria lulus

Tidak ada MAYOR terbuka setelah tindak lanjut.

## Larangan

Menyunting naskah atau berkas proyek; menjalankan render; meninjau bagian yang ia tulis sendiri; menulis temuan tanpa bukti.
