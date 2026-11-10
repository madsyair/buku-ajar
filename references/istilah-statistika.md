# Istilah statistika dan komputasi

Berkas ini memuat keputusan istilah bawaan skill, disarikan dari keputusan penulis seri statistika Bayesian (2026-11-02 s.d. 2026-11-07) dan berkas `keputusan-istilah.md` ketiga bukunya. Setiap buku tetap punya `naskah/keputusan-istilah.md` sendiri (tabel di bawah menjadi titik awal); butir yang belum diputuskan ditandai **[RAGU n]** dan diajukan kepada penulis.

## Kebijakan umum

1. Istilah yang padanannya **sudah lazim** di statistika Indonesia memakai bahasa Indonesia (regresi, intersep, kemiringan, ragam, galat baku, derajat bebas, validasi silang, imputasi).
2. Istilah yang dalam praktik lebih dikenal dalam bahasa Inggris dan padanannya **belum lazim** ditulis dalam bahasa Inggris **bercetak miring** dan dijelaskan dengan kata sehari-hari pada kemunculan pertama di setiap bab (*likelihood*, *shrinkage*, *draws*, *noise*, *overfitting*, *offset*).
3. Kelas istilah mengikuti skill eyd (`references/istilah-dan-kbbi.md`): A = padanan baku dipakai; B = serapan; C = tetap asing, miring.
4. Kata sifat Inggris yang menerangkan kata Indonesia mengikuti urutan Indonesia: prior *weakly informative*, posterior *improper*.
5. Verba tetap Indonesia: dicocokkan (bukan di-*fit*), disusutkan, diimputasi. Rincian *fit* di bagian "Istilah *fit*".
6. Akhiran pada istilah asing: *likelihood*-nya, *shrinkage*-nya.
7. Nama fungsi, argumen, keluarga distribusi paket ditulis sebagai kode dan tidak dimiringkan atau diterjemahkan (`pp_check()`, `family`, `zi`).
8. Singkatan (GLM, LOO, ESS, DAG, MRP) ditulis tegak; kepanjangannya disebut sekali.
9. Satu istilah dipakai konsisten di seluruh seri. Perubahan istilah adalah keputusan penulis yang dicatat bertanggal di `KEPUTUSAN-RANCANGAN.md` dan berlaku surut ke bab yang sudah selesai (dijalankan sebagai putaran penyuntingan).
10. Istilah yang sudah diganti dimasukkan ke `harness/konfig.json` kunci `istilah_terlarang` agar gerbang G-ISTILAH mencegahnya muncul lagi.

## Keputusan bawaan

| Konsep | Bentuk dipakai | Bentuk ditolak | Catatan |
|---|---|---|---|
| *likelihood* | *likelihood* (miring di prosa, judul, keterangan, sel tabel, kotak, latihan, label TikZ); *likelihood*-nya; fungsi *likelihood*; *likelihood* marginal | "kemungkinan", "fungsi kemungkinan" | "kemungkinan" dalam arti umum ("kemungkinan besar") tetap. Di rumus, kode, argumen, label `{#…}`, kunci sitasi tidak berubah. |
| *maximum likelihood*, REML | estimasi *maximum likelihood*; *restricted maximum likelihood* (REML) | "kemungkinan maksimum" | |
| *estimate*, *estimator*, *to estimate* | estimasi, estimator, mengestimasi, diestimasi; estimasi langsung (*direct estimate*) | taksiran, penaksir, menaksir, ditaksir, pendugaan, dugaan (arti estimasi) | "diduga/dugaan" dalam arti menyangka tetap. Nama objek kode boleh tetap. **Pengecualian istilah tetap**: *pendugaan area kecil* (*small area estimation*, SAE), bukan "estimasi area kecil", karena itulah padanan yang paling umum di literatur Indonesia (IPB, STIS, ITS, Undip, Unud), sedangkan BPS memakai istilah Inggrisnya (keputusan penulis 2026-11-10). |
| *draw* (satu nilai dari distribusi, simulasi) | membangkitkan, dibangkitkan, nilai bangkitan, nilai acak | menarik, ditarik, tarikan (dari distribusi) | "Tarikan" hanya arti gaya: tarikan ke rata-rata, ditarik ke prior. |
| keluaran MCMC | *draws* (tunggal *draw*), dijelaskan sekali: "nilai-nilai parameter yang dihasilkan *sampler*" | tarikan, sampel MCMC | Lihat jembatan istilah di bawah. |
| memilih unit dari populasi/data (survei, *bootstrap*) | penarikan sampel, menarik sampel, sampel acak; *bootstrap*: menarik sampel ulang dengan pengembalian; "variasi penarikan sampel" | membangkitkan sampel; "mengambil sampel" sebagai istilah | "Mengambil sampel" boleh sesekali sebagai parafrase umum, bukan istilah. |
| proses/fase MCMC | *sampling* (miring; pasangan *warmup*); *Gibbs sampling*, *importance sampling* | | Momentum HMC: "momentum baru dibangkitkan". |
| *noise* | *noise* (miring): *noise* pengamatan, *noise* proses, *noise* estimasi; rasio *signal-to-noise* | derau, rasio sinyal-derau | Dijelaskan sekali per bab. |
| *shrinkage* | *shrinkage* (glosa: penyusutan estimasi ke arah rata-rata kelompok); verba menyusutkan, tersusutkan; judul bab boleh "Prior Penyusutan …" | | Di judul memakai kata Indonesia; di isi *shrinkage* boleh disebut sekali. |
| *posterior predictive check* | *posterior predictive check* (PPC); nilai-*p* prediktif posterior | | Pasangannya untuk prior: "cek prediktif prior", "simulasi prediktif prior". |
| *weakly informative*, *improper*, *proper* | prior *weakly informative*, prior *improper* | "prior lemah informatif" | |
| *burn-in* vs *warmup* | *burn-in* hanya untuk rantai Metropolis/Gibbs bersetelan tetap; *warmup* untuk fase yang juga menyetel *sampler* (Stan/HMC/NUTS) | | Jelaskan bedanya sekali. |
| *overdispersion* | overdispersi (serapan, tegak); pertama: overdispersi (*overdispersion*, dispersi berlebih) | | |
| *complete/no/partial pooling* | sama (miring) | | |
| Bayesian workflow | alur kerja Bayesian (*Bayesian workflow* sekali dalam kurung) | | |
| residual | residu [RAGU: residu/sisaan] | | Pilih satu per seri. |
| random/fixed effect | efek acak, efek tetap; pertama: efek tingkat kelompok (efek acak) | | brms menyebut *group-level*/*population-level*. |
| *robust regression* | regresi *robust* [RAGU] | regresi kekar | |
| *spline* | *spline* | splin | |
| *overfitting* | *overfitting* (miring; glosa: terlalu pas dengan data yang dipakai mencocokkan) | | |
| *fit* (verba), *model fitting* | mencocokkan (model dengan data); pencocokan (model); pertama per buku: "mencocokkan model dengan data (*fit*; prosesnya *model fitting*)" | mengestimasi model, penyesuaian/pengepasan model, di-*fit*, *fit* sebagai kata benda | Lihat bagian "Istilah *fit*". |
| objek hasil *fit* | di prosa "objek hasil pencocokan"; nama objek kode tetap (`fit`, `fit_m1`) | "*fit* yang diagnostiknya gagal" | |
| *fitted values* | nilai prediksi | nilai dugaan, nilai taksiran | Sumbu plot residu. |
| *goodness of fit* | kecocokan model | | |
| logaritma natural | **ln** di naskah (prosa, rumus, tabel, gambar, glosarium); kode R/Stan tetap `log()` | `\log` tanpa basis di rumus; "log" untuk logaritma natural di prosa | Lihat bagian "Logaritma natural". Gerbang G-LN. |
| fake data | data palsu (data yang disimulasikan dari model dengan parameter yang ditetapkan sendiri) | | |
| effective sample size | ukuran sampel efektif (ESS) *bulk*/*tail* | | Glosa sekali per bab bila dilaporkan. |
| *divergent transition* | *divergent transition* (tanda bahwa *sampler* gagal menjelajahi bagian posterior yang melengkung tajam) | | |

## Istilah *fit* (keputusan seri, 2026-11-07)

Dasar: kajian pemakaian di seri (tiga bentuk bersaing: "mencocokkan", *fit* miring sebagai kata benda, "mengestimasi model"; "mencocokkan" juga dipakai dalam arti membandingkan).

- Kata kerja **mencocokkan** (model dengan data); kata benda proses **pencocokan** (model). "Model dicocokkan ulang", "LOO memerlukan $n$ kali pencocokan".
- Objek hasil: nama kode tetap; di prosa "**objek hasil pencocokan**".
- *fitted values* → **nilai prediksi**; *goodness of fit* → **kecocokan model**; *overfitting* tetap Inggris, **miring**, dengan glosa "terlalu pas dengan data yang dipakai mencocokkan".
- Dihindari: "mengestimasi model" (yang diestimasi parameter), "penyesuaian/pengepasan model", "nilai dugaan/taksiran", "di-*fit*". Masukkan ke `istilah_terlarang` di `konfig.json` bila buku sudah selesai disunting.
- "Mencocokkan" yang **berarti membandingkan** (hasil dengan grid, kunci dengan keluaran) diganti "membandingkan" agar kata itu hanya punya satu arti teknis.
- **Kemunculan pertama di setiap buku** menyebut istilah Inggrisnya: "mencocokkan model dengan data (*fit*; prosesnya *model fitting*)"; entri ditambahkan ke glosarium dan `keputusan-istilah.md`.

## Logaritma natural (keputusan seri, 2026-11-07)

- Logaritma natural ditulis **ln** di prosa, rumus (`\ln`), keterangan, tabel, gambar, dan glosarium: "ln *likelihood*", "ln *odds*", "skala ln", $\ln p(y \mid \theta)$. Istilah Inggris asalnya boleh disebut dalam kurung: "ln *likelihood* (*log-likelihood*)".
- **Kode tetap `log`**: R (`log()`), Stan (`log`, `log_lik`, `log_sum_exp`, `lp__`), nama objek, argumen, keluaran tercetak, dan R inline tidak diubah.
- Basis lain tetap `\log_{10}`, `\log_2`, `\log_b`. Sumbu grafik berskala logaritma basis 10 ditulis "skala logaritma".
- **Paragraf penjelas pada kemunculan pertama di setiap buku induk** (buku kunci merujuknya dalam satu kalimat), misalnya "Di naskah buku ini logaritma natural ditulis ln. Di R dan Stan, fungsi `log()` sudah berarti logaritma natural; basis lain ditulis `log10()`, `log2()`, atau `log(x, base = b)`. Jadi, `log(x)` di kode sama dengan $\ln x$ di naskah."
- **Tabel** memakai ln pada judul, judul kolom, dan isi. Nama kolom tampilan tabel dari objek R diganti lewat `col.names` (`knitr::kable(d, col.names = c("Model", "ln *likelihood*"))`); nama variabel kode tetap.
- Label gambar (sumbu, legenda, anotasi; mathtext `\log` → `\ln`) diganti ln; nama kolom data tidak.
- Kata yang **bukan logaritma** tidak diubah: logit, logistik, katalog, "log keputusan", "log LaTeX". Periksa makna setiap kemunculan; jangan mengganti otomatis buta.
- Kutipan verbatim di `harness/klaim.json` tidak diubah; bila kalimat penanda berubah, perbarui penandanya saja.
- Gerbang **G-LN** gagal bila `\log` tanpa subskrip basis muncul di rumus prosa atau keterangan (di luar blok kode, R inline, kode sebaris, dan berkas kode). Pengecualian beralasan: `ln-abaikan` di `pengecualian.json`.

## Notasi: periksa bentrok sebelum memilih

Simbol baru dipilih setelah memeriksa pemakaiannya di semua bab dan buku seri (rumus, kode, latihan, kunci) dan tabel notasi rancangan rinci. Contoh seri: π untuk distribusi stasioner diganti **ω** karena π dipakai sebagai konstanta (densitas normal); estimasi (tindakan) ditulis **$\hat\theta$**, bukan $a$ (bentrok dengan Beta($a$, $b$)) dan bukan $d$ (bentrok dengan $d\theta$). Simbol yang sama tidak berganti arti dalam satu bab ($\sigma$, $e$). Penggantian simbol adalah keputusan penulis dan diterapkan ke buku induk beserta kuncinya.

## Jembatan istilah antarbab dan antarbuku

Istilah yang berganti antara buku atau tahap belajar diberi **jembatan** pada kemunculan pertama istilah baru: satu atau dua kalimat yang mengaitkannya dengan istilah lama dan menyebut bedanya.

Contoh dari seri: Buku 1 (tanpa MCMC) memakai "sampel posterior", "membangkitkan sampel", "sampel Monte Carlo". Mulai Buku 2 Bab 4 dan Buku 3 Bab 1, keluaran MCMC disebut *draws*, dengan jembatan: isinya setara dengan sampel posterior Buku 1, tetapi *draws* berurutan saling berkorelasi sehingga tidak setara dengan sampel bebas (ukuran sampel efektif, Buku 2 Bab 7).

Aturan:

- Jembatan ditulis **sekali** di bab tempat istilah baru pertama muncul di buku itu, dan diulang singkat (satu klausa) di bab pertama buku berikutnya bila pembaca boleh melompat buku.
- Rancangan rinci mencatat setiap jembatan: istilah lama, istilah baru, bab, bunyi ringkasnya.
- Pembaca pemula dan editor memeriksa bahwa istilah buku lain yang dipakai tanpa glosa tidak ada (pembaca boleh melompat dari Buku 1 ke Buku 3).

## Penjelasan istilah pada kemunculan pertama

Pola: *istilah* (padanan atau kepanjangan bila ada) + arti sehari-hari + mengapa dibutuhkan + contoh angka. Contoh:

> *Draws*, yaitu nilai-nilai parameter yang dihasilkan *sampler* satu per satu, berperan seperti sampel posterior di Buku 1; bedanya, *draws* yang berurutan saling berkorelasi.

Jangan menulis tiga istilah baru dalam satu kalimat. Kotak "Ingat" tidak dipakai untuk menitipkan istilah baru.

## Format `keputusan-istilah.md` per buku

```
| Istilah Inggris | Bentuk di buku | Keputusan | Alasan | Bab |
```

Nilai kolom Keputusan: `TETAP-INDONESIA`, `TETAP (serapan)`, `PAKAI-INGGRIS`, `singkatan tegak`, `nama diri`, `Keputusan penulis YYYY-MM-DD`, `[RAGU n]`. Agen penulis menambah baris di bagian "Tambahan Bab N". Status "diputuskan saat perancangan, dapat diubah penulis" dibedakan dari "keputusan penulis"; jangan menyebut usulan agen sebagai keputusan penulis.
