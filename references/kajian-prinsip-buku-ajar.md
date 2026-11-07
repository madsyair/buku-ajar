<!--
Salinan kajian dari proyek seri statistika Bayesian
(naskah-bersama/kajian-prinsip-buku-ajar.md, 7 November 2026), disertakan apa adanya
sebagai dasar references/prinsip-buku-ajar.md.

STATUS VERIFIKASI SUMBER: kajian ini disusun dari abstrak, laman penerbit, katalog,
dan cuplikan mesin pencari; teks lengkap sumber TIDAK dibaca. Tanda di daftar pustaka:
[A] = metadata dan temuan inti terkonfirmasi dari abstrak/laman penerbit;
[S] = dikenal dari ringkasan sekunder, wajib dicek ke teks asli sebelum dikutip;
[A, terverifikasi] = dicocokkan dengan teks asli. Permendikbudristek 22/2022 (bagian
1.11, 1.12, butir 30-35) sudah diverifikasi terhadap teks peraturan di proyek seri:
naskah-bersama/sumber/permendikbudristek-22-2022.{pdf,md} (halaman = halaman PDF).
Kutipan langsung hanya dari Permendikbudristek 22/2022. Jangan menyitasi isi kajian ini di naskah buku tanpa
membuka sumber aslinya dan mencatat kutipan verbatimnya di harness/klaim.json.
Lihat juga "Lampiran: Butir yang Perlu Diverifikasi" di akhir berkas.

Bila kajian bertentangan dengan keputusan penulis (references/aturan-gaya-dan-tampilan.md,
KEPUTUSAN-RANCANGAN.md proyek), keputusan penulis yang berlaku. Contoh: butir 23
("judul gambar menyatakan temuan") diganti keputusan "judul gambar singkat, temuan
ke Div catatan".
-->


# Kajian Prinsip Penulisan Buku Ajar Statistika, Sains Data, dan Matematika Terapan

Rujukan untuk skill penulisan buku ajar bagi dosen Politeknik Statistika STIS

Disusun 7 November 2026

## Ruang Lingkup dan Cara Membaca Kajian

Kajian ini menjawab delapan pertanyaan tentang cara menulis buku ajar yang baik, dengan fokus pada statistika, sains data, dan matematika terapan. Pembacanya adalah dosen yang menulis buku dan reviewer yang menilainya. Setiap klaim diberi rujukan penulis–tahun. Daftar pustaka di bagian akhir memuat DOI atau URL.

**Catatan metode dan kejujuran sumber.** Penelusuran dilakukan lewat mesin pencari web. Dari lingkungan kerja penyusun, pengambilan teks lengkap (laman jurnal, peraturan.go.id, JDIH, situs penerbit) tidak dapat dilakukan karena pembatasan jaringan. Akibatnya, yang benar-benar terbaca adalah abstrak, katalog perpustakaan, laman penerbit, dan cuplikan yang ditampilkan mesin pencari. Karena itu:

1. Kajian ini **tidak memuat kutipan langsung** dari sumber, kecuali satu anekdot yang secara eksplisit ditandai sebagai kutipan sekunder dan kutipan dari Permendikbudristek Nomor 22 Tahun 2022 (lihat butir 4).
2. Semua isi disajikan sebagai parafrase temuan inti yang konsisten di beberapa sumber (abstrak dan ulasan).
3. Daftar pustaka memberi tanda status: **[A]** berarti metadata dan temuan inti terkonfirmasi dari abstrak atau laman penerbit; **[S]** berarti isi dikenal dari ringkasan sekunder sehingga perlu dicek ke teks asli sebelum dikutip di naskah buku.
4. **Pembaruan 7 November 2026.** Penulis mengunggah salinan resmi Permendikbudristek Nomor 22 Tahun 2022 (PDF JDIH Kemendikbudristek, 87 halaman). Teksnya disimpan di `sumber/permendikbudristek-22-2022.md` (dengan penanda `<!-- Halaman N -->`) beserta PDF-nya. Semua pernyataan tentang peraturan itu di bagian 1.11 dan 1.12 sudah dicocokkan dengan teks lengkap dan diberi tanda **[A, terverifikasi]**. Kutipan verbatim pendek di kedua bagian itu menyebut pasal atau lampiran serta halaman PDF ("hlm. N" = halaman ke-N berkas PDF, bukan nomor cetak lampiran).

Penulis buku yang ingin mengutip kalimat dari sumber-sumber ini tetap wajib membaca teks aslinya.

---

## 1. Prinsip Umum Buku Ajar Menurut Literatur

### 1.1 Tujuan belajar eksplisit dan keselarasan konstruktif

Biggs (1996) memadukan dua gagasan. Gagasan pertama berasal dari teori belajar konstruktivis: makna dibangun oleh pemelajar melalui aktivitasnya. Gagasan kedua berasal dari desain instruksional: tujuan, kegiatan belajar, dan asesmen harus selaras. Hasilnya adalah *constructive alignment* (keselarasan konstruktif). Bagi buku ajar, prinsip ini berarti tiga hal harus saling mengunci:

- tujuan bab yang dinyatakan dengan kata kerja yang dapat diamati (menghitung, menafsirkan, membandingkan, memeriksa asumsi);
- isi dan contoh yang melatih tepat kata kerja itu;
- latihan dan kunci jawaban yang menguji kata kerja yang sama.

Bab yang tujuannya "menafsirkan selang kredibel", tetapi latihannya hanya meminta menghitung batas selang, tidak selaras.

Tradisi Mager (*Preparing Instructional Objectives*, 1962; edisi ketiga 1997) merumuskan tujuan dari tiga unsur: unjuk kerja (*performance*), kondisi (*condition*), dan kriteria (*criterion*). Format ABCD menambahkan sasaran (*audience*), sehingga unsurnya menjadi *Audience, Behavior, Condition, Degree*. Atribusi ABCD kepada penulis tertentu berbeda-beda antarsumber, tetapi strukturnya sama (Mager, 1997).

Di lingkungan pendidikan tinggi Indonesia, tujuan bab dalam buku ajar sebaiknya diturunkan dari capaian pembelajaran mata kuliah (CPMK), yang diturunkan dari capaian pembelajaran lulusan (CPL) dalam Standar Nasional Pendidikan Tinggi. SN-Dikti diatur oleh Permendikbudristek Nomor 53 Tahun 2023, yang menurut materi sosialisasi LLDIKTI telah disesuaikan melalui Permendiktisaintek Nomor 39 Tahun 2025. Penulis perlu memeriksa ketentuan yang berlaku saat naskah disusun.

### 1.2 Beban kognitif: contoh terselesaikan, perhatian terbagi, redundansi

Teori beban kognitif berangkat dari temuan Sweller (1988): pemecahan masalah dengan analisis sarana–tujuan (*means–ends analysis*) menyita kapasitas memori kerja yang semestinya dipakai untuk membangun skema. Sweller dkk. (2019) meninjau dua puluh tahun perkembangan teori ini. Efek-efek yang paling relevan bagi penulis buku adalah sebagai berikut.

| Efek | Inti temuan | Terjemahan untuk buku ajar |
|---|---|---|
| *Worked example* | Pemula belajar lebih baik dari contoh yang langkahnya lengkap daripada dari soal yang langsung dikerjakan (Atkinson dkk., 2000; Sweller dkk., 2019) | Setiap prosedur baru diperkenalkan dengan satu contoh terselesaikan lengkap sebelum latihan mandiri |
| *Split-attention* | Teks dan diagram yang harus dipadukan secara mental membebani; mengintegrasikannya membantu (Chandler & Sweller, 1991) | Label diletakkan di dalam gambar, bukan di keterangan terpisah; penjelasan kode diletakkan dekat baris yang dijelaskan |
| Redundansi | Informasi yang sama dalam dua bentuk yang masing-masing sudah cukup justru menambah beban (Chandler & Sweller, 1991) | Jangan mengulang isi tabel dalam paragraf kalimat demi kalimat; prosa menafsirkan, tabel menyajikan |
| *Expertise reversal* | Bantuan yang menolong pemula dapat menjadi beban bagi pemelajar mahir (Kalyuga dkk., 2003) | Lihat Bagian 6 |

Atkinson dkk. (2000) menurunkan prinsip desain contoh terselesaikan, antara lain bahwa komponen contoh (teks, rumus, diagram) harus terintegrasi. Mereka juga menempatkan contoh terselesaikan terutama pada tahap awal penguasaan keterampilan.

### 1.3 Pembelajaran multimedia

Mayer (2020) dalam edisi ketiga *Multimedia Learning* merangkum 15 prinsip yang dikelompokkan menjadi tiga: mengurangi pemrosesan yang tidak relevan (*extraneous*), mengelola pemrosesan esensial, dan mendorong pemrosesan generatif. Untuk buku cetak atau PDF, prinsip yang relevan adalah:

- **Koherensi**: buang materi yang menarik tetapi tidak perlu, misalnya anekdot sejarah yang panjang, gambar dekoratif, atau rumus yang tidak dipakai lagi.
- **Penanda (*signaling*)**: tampakkan struktur dengan judul, kalimat pengantar yang menyebut urutan langkah, dan penebalan istilah kunci saat pertama muncul.
- **Kedekatan spasial**: teks dan gambar yang saling merujuk diletakkan berdekatan.
- **Kedekatan temporal**: dalam buku, ini berarti penjelasan dan representasi yang berpasangan disajikan bersamaan, misalnya rumus bersama keluaran kode yang menghitungnya, bukan dipisah beberapa halaman.
- **Segmentasi**: pecah penurunan panjang menjadi langkah bernomor yang dapat dibaca sesuai tempo pembaca.
- **Pralatih (*pre-training*)**: perkenalkan istilah dan notasi kunci sebelum konsep utama, misalnya kotak notasi di awal bab.

### 1.4 Latihan mengingat kembali dan latihan berjarak

Dunlosky dkk. (2013) menilai sepuluh teknik belajar. Latihan uji (*practice testing*) dan latihan berjarak (*distributed practice*) mendapat utilitas tinggi. Interogasi elaboratif, penjelasan diri, dan latihan berselang (*interleaved practice*) mendapat utilitas sedang. Meringkas, menandai teks, dan membaca ulang mendapat utilitas rendah.

Roediger dan Karpicke (2006) menunjukkan bahwa membaca ulang unggul pada tes lima menit kemudian, tetapi pola itu berbalik pada tes dua hari dan satu minggu kemudian: kelompok yang diuji mengingat lebih baik. Cepeda dkk. (2006) mensintesis 839 pengukuran dari 317 eksperimen dan mendapati bahwa jeda antarsesi belajar yang optimal makin panjang seiring makin panjangnya selang retensi. Mereka juga mencatat bahwa manfaat latihan berjarak lebih konsisten pada tugas verbal daripada pada keterampilan intelektual seperti matematika. Ini batasan yang perlu diingat penulis buku statistika.

Implikasinya bagi buku:

- tiap subbab ditutup dengan pertanyaan cek pemahaman, bukan ringkasan saja;
- latihan akhir bab memuat soal dari bab-bab sebelumnya (pengulangan berjarak);
- soal dengan jenis berbeda dicampur, sehingga pembaca harus memilih metode, bukan hanya menerapkannya.

### 1.5 Interogasi elaboratif dan penjelasan diri

Interogasi elaboratif meminta pemelajar menjawab "mengapa fakta ini benar?". Pressley dkk. (1987) menjadi salah satu rujukan awal. Penjelasan diri (*self-explanation*) meminta pemelajar menjelaskan langkah atau mengaitkannya dengan pengetahuan lama. Chi dkk. (1989) menemukan bahwa mahasiswa yang baik dalam mempelajari contoh mekanika menghasilkan lebih banyak penjelasan diri. Dunlosky dkk. (2013) memberi keduanya utilitas sedang karena bukti di kelas nyata masih terbatas. Dalam buku, keduanya dapat diwujudkan dengan pertanyaan sisipan (Bagian 3).

### 1.6 Dari konkret ke abstrak

*Concreteness fading* (pemudaran kekonkretan) dimulai dari representasi konkret, lalu secara eksplisit dan bertahap bergeser ke representasi abstrak. Fyfe dkk. (2014) meninjau studi-studi tentang teknik ini dalam pembelajaran matematika dan sains. Pashler dkk. (2007), dalam panduan praktik IES, juga merekomendasikan pemaduan representasi abstrak dan konkret serta penggunaan pertanyaan mendalam yang menuntut penjelasan.

Urutan yang lazim dalam statistika: contoh data nyata (konkret) → gambar atau simulasi (ikonik) → notasi dan rumus (abstrak) → kembali ke data untuk penafsiran.

### 1.7 Perancah dan pemudarannya

Istilah *scaffolding* (perancah) berasal dari Wood dkk. (1976): bantuan tutor yang memungkinkan pemula menyelesaikan tugas yang belum bisa ia selesaikan sendiri, lalu disesuaikan dengan unjuk kerja pemelajar. Renkl dan Atkinson (2003) mengusulkan prosedur pemudaran (*fading*): langkah-langkah pemecahan masalah dimasukkan satu per satu ke dalam contoh, sampai pemelajar menyelesaikan soal sendiri. Atkinson dkk. (2003) melaporkan bahwa pemudaran membantu transfer dekat secara andal, tetapi tidak andal untuk transfer jauh.

Pola buku: contoh 1 lengkap → contoh 2 dengan langkah terakhir dikosongkan → contoh 3 dengan dua langkah dikosongkan → soal mandiri.

### 1.8 Mengaktifkan pengetahuan awal

Ausubel (1960) memperkenalkan *advance organizer* (pengatur awal): materi pengantar yang tingkat abstraksinya lebih tinggi daripada materi pelajaran dan berfungsi sebagai jembatan ke struktur kognitif yang sudah ada. Pengatur awal berbeda dari ringkasan, yang tingkat abstraksinya sama dengan isi. Ringkasan sekunder menyebut manfaatnya terbesar pada pemelajar berpengetahuan awal rendah.

Untuk buku statistika: buka bab dengan menghubungkan konsep baru ke konsep lama. Contohnya, posterior dikaitkan dengan "memperbarui dugaan setelah melihat data", lalu dengan rata-rata tertimbang yang sudah dikenal.

### 1.9 Miskonsepsi dan teks sanggahan

Teks sanggahan (*refutation text*) menyebut miskonsepsi yang umum, menyanggahnya, lalu menjelaskan konsepsi yang benar. Tippett (2010) meninjau dua dekade penelitian tentang teks sanggahan dalam pendidikan sains. Meta-analisis yang lebih baru melaporkan efek positif sedang, walaupun temuan ini juga mendapat sikap skeptis dari sebagian peneliti.

Statistika kaya miskonsepsi: nilai-p sebagai peluang hipotesis nol benar, selang kepercayaan sebagai peluang parameter berada di dalam selang, korelasi sebagai kausalitas, dan "tidak signifikan berarti tidak ada efek". Setiap bab sebaiknya menyanggah secara eksplisit satu atau dua miskonsepsi yang paling relevan.

### 1.10 Umpan balik dalam latihan

Hattie dan Timperley (2007) membingkai umpan balik sebagai jawaban atas tiga pertanyaan: ke mana saya menuju, bagaimana kemajuan saya, dan apa langkah berikutnya. Shute (2008) mendefinisikan umpan balik formatif sebagai informasi yang dimaksudkan untuk mengubah pemikiran atau perilaku pemelajar. Ia menekankan bahwa manfaatnya bergantung pada cara penyampaiannya: spesifik, tidak menghakimi, dan tepat waktu.

Dalam buku, umpan balik berwujud kunci jawaban yang menjelaskan alasan, bukan hanya angka akhir. Kunci yang baik juga menyebut kesalahan yang lazim beserta cara mendeteksinya.

### 1.11 Pedoman resmi Indonesia

| Regulasi atau pedoman | Isi yang relevan | Catatan cakupan |
|---|---|---|
| UU Nomor 3 Tahun 2017 tentang Sistem Perbukuan dan PP Nomor 75 Tahun 2019 | Kerangka hukum perbukuan nasional | Berlaku umum |
| Permendikbudristek Nomor 22 Tahun 2022 tentang Standar Mutu Buku, Standar Proses dan Kaidah Pemerolehan Naskah, serta Standar Proses dan Kaidah Penerbitan Buku (ditetapkan 10 Mei 2022, diundangkan 25 Mei 2022, BN 2022 No. 527) **[A, terverifikasi]** | Tiga kelompok aturan: standar mutu Buku (Bab II, Lampiran I), standar proses dan kaidah pemerolehan naskah, yaitu penulisan, penerjemahan, dan penyaduran (Bab III, Lampiran II), serta standar proses dan kaidah penerbitan, yaitu pengeditan, pengilustrasian, dan pendesainan (Bab IV, Lampiran III). Pasal 8 (hlm. 5–6): standar mutu Buku Pendidikan terdiri atas standar materi, penyajian, desain, dan grafika. Pasal 10 ayat (1) (hlm. 8): standar penyajian mencakup "kelayakan penyampaian isi Buku sesuai dengan tingkat perkembangan peserta didik" dan "kelayakan penggunaan bahasa yang tepat dan komunikatif". Rincian lihat 1.12 | Berlaku untuk **semua Buku**: Buku Pendidikan dan Buku Umum, cetak dan elektronik (Pasal 2–3, hlm. 3–4). Buku Pendidikan didefinisikan mencakup "pendidikan akademik, pendidikan profesi, pendidikan vokasi" (Pasal 1 angka 3, hlm. 3). Istilah "buku ajar" dan "perguruan tinggi" tidak muncul; rincian kelayakan isi Buku Teks berorientasi pada satuan pendidikan dasar–menengah (lihat 1.12) |
| Permendikbudristek Nomor 25 Tahun 2022 tentang Penilaian Buku Pendidikan dan Peraturan Kepala BSKAP Nomor 039/H/P/2022 | Prosedur dan pedoman penilaian; instrumen penilaian ada di lampiran | Belum diverifikasi ke teks asli |
| Tradisi instrumen BSNP | Empat aspek kelayakan: isi, penyajian, kebahasaan, kegrafikan (dirujuk ke PP 19/2005 Pasal 43 ayat 5 oleh berbagai penelitian) | Banyak dipakai sebagai kerangka analisis buku. Permendikbudristek 22/2022 **tidak** memakai empat istilah ini: ia memakai materi, penyajian, desain, dan grafika; kebahasaan masuk ke standar penyajian |
| PO PAK Dosen 2019 (Ditjen Sumber Daya Iptek dan Dikti) | Buku ajar adalah buku pegangan satu mata kuliah yang ditulis pakar bidangnya, mengikuti kaidah tulisan ilmiah, dan disebarluaskan kepada peserta kuliah; ber-ISBN, berbeda dari diktat | Ketentuan angka kredit telah berubah sejak 2023; periksa aturan yang berlaku |

Simpulan untuk penulis STIS (direvisi setelah verifikasi teks Permendikbudristek 22/2022): pernyataan sebelumnya bahwa peraturan ini "bukan untuk buku ajar perguruan tinggi" **tidak tepat**. Peraturan ini berlaku untuk semua Buku, dan definisi Buku Pendidikan secara eksplisit mencakup pendidikan akademik dan vokasi. Yang benar: peraturan ini tidak memuat ketentuan **khusus** buku ajar perguruan tinggi. Rincian kelayakan isi Buku Teks bertumpu pada "standar nasional pendidikan dan kurikulum yang berlaku", "buku siswa dan buku panduan guru", serta "tingkat kelas" (Lampiran I, hlm. 36), sehingga sulit diterapkan langsung pada buku ajar satu mata kuliah. Namun, syarat isi (Pasal 9 ayat 2 dan Pasal 14 ayat 2), standar penyajian, desain, dan grafika, standar dan kaidah penulisan (Lampiran II), serta anatomi buku dan kaidah penerbitan (Lampiran III) berlaku bagi buku ajar STIS, baik ia digolongkan Buku Pendidikan (Buku Teks atau nonteks) maupun Buku Umum. Kerangka penilaian internal sebaiknya memakai istilah peraturan (materi, penyajian, desain, grafika), dengan kebahasaan diacu ke EYD Edisi V. Butir yang dapat diperiksa ada di 1.12.

### 1.12 Kriteria dari Permendikbudristek 22/2022 yang relevan untuk buku ajar

Semua butir di bawah ini **[A, terverifikasi]** terhadap `sumber/permendikbudristek-22-2022.md`. Halaman adalah halaman PDF. Kolom terakhir memetakan butir ke daftar periksa di bagian 8; butir 31–35 adalah tambahan baru.

| Kriteria peraturan | Bunyi atau isi (kutipan pendek) | Lokasi | Butir daftar periksa |
|---|---|---|---|
| Syarat isi (wajib) | Buku wajib "tidak bertentangan dengan nilai-nilai Pancasila", "tidak diskriminatif berdasarkan suku, agama, ras, dan/atau antargolongan", serta tidak mengandung unsur pornografi, kekerasan, dan ujaran kebencian | Pasal 9 ayat (2), hlm. 6; Pasal 14 ayat (2), hlm. 9–10 | **31 (baru)** |
| Kepatutan gambar | Pelanggaran norma pada gambar "di antaranya mengandung penistaan SARA, bias gender, pornografi, perundungan, dan kekerasan" | Lampiran III, hlm. 82 | 31 |
| Kebenaran keilmuan | Teori, konsep, dalil, atau aksioma "tidak menimbulkan bias dan multitafsir serta sesuai dengan definisi yang berlaku dalam bidang ilmu"; prosedur atau metode "bersifat runtut dan logis" | Pasal 9 ayat (5) huruf a, hlm. 6; Lampiran I, hlm. 36 | 8, 29 |
| Ketelitian data dan fakta | Data khusus mencakup "ketepatan dan kebenaran penggunaan hukum, dalil, aksioma, rumus atau postulat" serta terminologi dan definisi; perbaikan data dan fakta "berdasarkan sumber yang sahih dan mutakhir" | Lampiran II, hlm. 57; Pasal 24 ayat (4), hlm. 15 | 18, 21, 29 |
| Kesesuaian dengan perkembangan iptek | Materi "mengakomodasi perkembangan keilmuan dan teknologi terkini"; uraian dan latihan mendorong pembaca mencari informasi "dari berbagai sumber yang valid" | Pasal 9 ayat (5) huruf c, hlm. 6; Lampiran I, hlm. 36 | 20, 25 |
| Kesesuaian dengan konteks dan lingkungan | Materi "berkesesuaian dengan keseharian peserta didik, kearifan lokal, dan konteks kehidupan secara luas" | Lampiran I, hlm. 36 | 4, 18 |
| Kesatupaduan antarbagian | Bagian buku "saling mengait, saling melengkapi, dan saling berkesinambungan" | Lampiran I, hlm. 36 | 3, 26 |
| Kelayakan isi Buku Umum | Ketepatan, keterpaduan, kejelasan, dan kelegalan; kelegalan berarti "keabsahan hak cipta Naskah Buku" | Pasal 14 ayat (3)–(8), hlm. 10 | 29, 32 |
| Penyajian | Pola hierarkis, prosedural, atau klaster; "Setiap bab disajikan secara runtut dan berkesinambungan"; tingkat kerumitan bahasa sesuai kemampuan pembaca sasaran | Pasal 10, hlm. 8; Lampiran I, hlm. 40 | 7, 24 |
| Syarat penyajian dalam kaidah penulisan | "kejelasan", "keringkasan", dan "keterpautan"; keringkasan menghindari penyampaian ambigu, berulang, dan bertele-tele | Pasal 35 ayat (3), hlm. 19; Lampiran II, hlm. 57 | 12, 30 |
| Kebahasaan | Berpedoman pada KBBI, Pedoman Umum Ejaan Bahasa Indonesia, Tata Bahasa Baku Bahasa Indonesia, Pedoman Umum Pembentukan Istilah, dan pedoman lain dari lembaga kebahasaan. Catatan: peraturan terbit sebelum EYD Edisi V (Agustus 2022), jadi kini acuannya EYD V | Lampiran II, hlm. 58; Lampiran III, hlm. 81 | 30 |
| Tahapan penulisan | Prapenulisan (tema, tujuan, "pembaca sasaran", sumber, kerangka), penulisan draf, perevisian, dan penyuntingan mandiri (tipografi, bahasa, data dan fakta, legalitas dan norma) | Pasal 20–24, hlm. 13–15 | 1, 28 |
| Pengutipan dan hak cipta | Swasunting memperbaiki kutipan dan rujukan teks serta gambar "untuk menghindari pelanggaran hak cipta"; pengutipan "mengikuti rujukan primer (gaya selingkung)"; kutipan terhubung ke daftar pustaka | Pasal 24 ayat (5), hlm. 15; Lampiran I, hlm. 44; Lampiran II, hlm. 56 dan 58 | 19, **32 (baru)** |
| Gambar dan infografik | Perbaikan meliputi "ketepatan judul gambar", "ketepatan keterangan gambar", "kelegalan sumber gambar", "kebenaran data pada grafik", dan "kejelasan legenda pada gambar" | Pasal 50, hlm. 24 | 23, 32 |
| Ilustrasi buku teks | Ilustrasi untuk buku teks atau buku teknik "harus mengutamakan keakuratan yang bertanggung jawab"; karakter visual seluruh ilustrasi dalam satu buku selaras | Lampiran III, hlm. 75 | 23, 34 |
| Anatomi buku (bagian awal) | Wajib: halaman judul penuh; halaman hak cipta (memuat antara lain ISBN dan "nama/tipe fon yang digunakan di dalam buku"); daftar isi dan prakata wajib untuk buku nonfiksi. Prakata memuat "sekurang-kurangnya tujuan penulisan, pembaca sasaran, keunggulan buku, dan amanat/pesan"; pada buku teks, introduksi dapat memberi "petunjuk penggunaan buku" | Lampiran III, Tabel 1, hlm. 65–67 | **33 (baru)** |
| Anatomi buku (bagian isi) | Khusus buku teks, subbab dapat memuat pengayaan, pelatihan atau penugasan, rangkuman atau refleksi, dan soal evaluasi | Lampiran III, Tabel 2, hlm. 68 | 25, 26, 27 |
| Anatomi buku (bagian akhir) | Daftar pustaka wajib untuk buku nonfiksi; glosarium, indeks, dan kredit gambar opsional dalam tabel, tetapi Lampiran II menyebut ketiganya sebagai bagian akhir nonfiksi yang "perlu disusun sesuai dengan aturan"; riwayat singkat pelaku perbukuan (penulis, editor, desainer, dan ilustrator bila ada ilustrasi asli) wajib pada buku pendidikan | Lampiran III, Tabel 3, hlm. 69–71; Lampiran II, hlm. 55 | 33 |
| Nama penulis | Nama penulis ditulis sebagai nama pena atau "nama asli tanpa mencantumkan gelar akademis" | Lampiran II, hlm. 55 | 33 |
| Desain dan tipografi | Jumlah *typeface* "paling optimal adalah dua jenis"; panjang baris "antara 40―70 karakter"; bebas "baris tunggal (orphan/widow line)"; fon diperoleh secara legal dan dicantumkan di halaman hak cipta; artwork cetak 300 dpi | Lampiran II, hlm. 50–51; Lampiran III, hlm. 76, 84–85 | 13, **34 (baru)** |
| Buku elektronik | Keterbacaan "pada berbagai perangkat dan platform", ukuran fail relatif ringan, daftar isi interaktif; adaptibilitas mencakup kebutuhan khusus penyandang disabilitas | Pasal 12 ayat (4), hlm. 9; Lampiran I, hlm. 41; Lampiran III, hlm. 78 | **35 (baru)** |

Catatan penerapan:

- Kriteria yang mengacu pada "standar nasional pendidikan dan kurikulum yang berlaku" (Pasal 9 ayat 5 huruf b) dapat dibaca untuk buku ajar sebagai keselarasan dengan CPL/CPMK dan SN-Dikti (butir 1). Ini tafsiran penyusun, bukan bunyi peraturan.
- Peraturan menetapkan gaya selingkung buku pendidikan oleh Pusat Perbukuan (Lampiran II, hlm. 56). Untuk buku terbitan penerbit kampus atau penerbit umum, yang berlaku adalah gaya selingkung penerbitnya.
- Pasal 70 (hlm. 33) mencabut sebagian Permendikbud Nomor 8 Tahun 2016 tentang Buku yang Digunakan oleh Satuan Pendidikan.

---

## 2. Kerangka 5W1H dalam Buku Ajar

### 2.1 Asal-usul

Daftar pertanyaan "siapa, apa, kapan, di mana, mengapa, bagaimana" berakar pada retorika klasik, yaitu pada "keadaan" (*circumstantiae*) yang dipakai untuk memeriksa suatu perkara. Tradisi ini lazim dikaitkan dengan Hermagoras dari Temnos. Sloan (2010), menurut ringkasan sekunder, berargumen bahwa sumber paling awal ketujuh keadaan (*septem circumstantiae*) adalah *Etika Nikomakea* karya Aristoteles (III.1, 1111a). Dalam jurnalisme, rumus ini menjadi pegangan untuk paragraf pembuka berita pada awal abad ke-20. Sajak Kipling tentang "enam pelayan setia" dalam *Just So Stories* (1902) sering dikutip, tetapi itu rujukan sastra, bukan asal kerangkanya.

Jadi, 5W1H lahir sebagai **alat kelengkapan**: memastikan tidak ada keadaan penting suatu peristiwa yang terlewat. Ia tidak dirancang sebagai urutan pengajaran.

### 2.2 Kegunaannya

Sebagai alat perencanaan, 5W1H membantu penulis memeriksa apakah sebuah bab sudah menjawab pertanyaan yang wajar diajukan pembaca. Untuk metode statistika, pertanyaan "mengapa" dan "kapan" paling sering terlewat. Buku sering menjelaskan cara menghitung, tetapi tidak menjelaskan mengapa metode itu ada dan kapan ia gagal. Pertanyaan pemandu juga sejalan dengan bukti tentang pertanyaan mendalam (Pashler dkk., 2007) dan interogasi elaboratif (Dunlosky dkk., 2013).

### 2.3 Keterbatasan bila diterapkan secara mekanis

- **Tidak semua W relevan.** "Siapa" dan "di mana" jarang bermakna untuk konsep seperti fungsi kemungkinan. Memaksakannya melahirkan paragraf pengisi.
- **5W1H tidak mengatur urutan belajar.** Ia tidak menyebut contoh terselesaikan, latihan, atau umpan balik. Bab yang menjawab enam pertanyaan dapat tetap gagal karena tidak ada latihan yang selaras dengan tujuan (Biggs, 1996).
- **Subjudul berupa enam pertanyaan berulang** di setiap subbab membuat struktur buku monoton dan mengaburkan isi. Pembaca yang memindai daftar isi melihat "Apa itu…?" berkali-kali, bukan nama konsep. Ini bertentangan dengan prinsip penanda (Mayer, 2020), yang menghendaki struktur isi tampak.
- **"Bagaimana" terlalu lebar.** Dalam statistika, "bagaimana" mencakup setidaknya tiga hal yang berbeda: bagaimana menghitung, bagaimana menafsirkan, dan bagaimana memeriksa.

### 2.4 Rekomendasi: 5W1H yang disesuaikan untuk statistika

Pakai 5W1H sebagai **daftar periksa perencanaan bab** yang tidak tampil sebagai struktur naskah. Untuk setiap metode, versi yang lebih tepat adalah enam pertanyaan berikut.

| Pertanyaan perencanaan | Wujud di naskah |
|---|---|
| Apa masalahnya? | Kasus pembuka dengan data nyata |
| Mengapa metode ini (dan bukan cara naif)? | Kegagalan cara naif ditunjukkan dengan angka atau gambar |
| Kapan metode ini dipakai, dan apa asumsinya? | Daftar asumsi dan cara memeriksanya |
| Bagaimana menghitungnya? | Intuisi → rumus → kode → keluaran |
| Bagaimana menafsirkannya? | Kalimat tafsiran dalam bahasa substansi, lengkap dengan satuan |
| Kapan metode ini gagal? | Contoh pelanggaran asumsi beserta diagnostiknya |

### 2.5 Perbandingan dengan kerangka lain

| Kerangka | Kekuatan | Kelemahan | Peran yang disarankan |
|---|---|---|---|
| 5W1H | Memeriksa kelengkapan isi | Tidak mengatur urutan dan asesmen | Daftar periksa perencanaan |
| Tujuan–konsep–contoh–latihan | Mengatur urutan pengajaran dan selaras dengan bukti contoh terselesaikan | Bisa melupakan "mengapa" dan "kapan gagal" | Kerangka utama bab |
| ABCD (Mager) | Membuat tujuan terukur | Hanya mengatur rumusan tujuan | Rumusan tujuan di awal bab |
| Keselarasan konstruktif (Biggs) | Mengunci tujuan, kegiatan, dan asesmen | Abstrak, perlu diterjemahkan | Uji keselarasan saat review |

Rekomendasi akhir: kerangka utama bab adalah **tujuan (ABCD) → konsep (konkret ke abstrak) → contoh terselesaikan → latihan bertingkat → umpan balik**. Enam pertanyaan dalam 2.4 dipakai untuk memeriksa kelengkapan. Keselarasan diuji di tahap review.

---

## 3. Pertanyaan Bergaya Sokratik dalam Teks Tertulis

### 3.1 Jenis pertanyaan

Paul dan Elder (2006), dalam *The Thinker's Guide to the Art of Socratic Questioning*, menyusun taksonomi pertanyaan Sokratik berdasarkan konsep berpikir kritis. Versi enam kategori yang banyak dipakai dalam pengajaran adalah sebagai berikut, dengan contoh untuk statistika.

| Jenis | Fungsi | Contoh dalam bab statistika |
|---|---|---|
| Klarifikasi | Memperjelas makna | Apa yang sebenarnya diukur oleh "rata-rata pengeluaran per kapita" di sini: per orang, atau per rumah tangga dibagi jumlah anggota? |
| Asumsi | Menggali yang dianggap benar | Model ini menganggap pengamatan saling bebas. Apakah dua rumah tangga di blok sensus yang sama benar-benar bebas? |
| Alasan dan bukti | Menguji dasar klaim | Grafik mana yang mendukung klaim bahwa sisaan berdistribusi normal? |
| Sudut pandang | Mempertimbangkan alternatif | Bagaimana pembuat kebijakan dan peneliti membaca selang yang sama secara berbeda? |
| Implikasi | Menelusuri akibat | Jika prior dibuat lebih lebar sepuluh kali, apa yang berubah pada posterior? |
| Pertanyaan tentang pertanyaan | Memeriksa apakah pertanyaannya tepat | Apakah pertanyaan "apakah efeknya signifikan?" sudah menjawab kebutuhan pengambil keputusan? |

Sumber sekunder mencatat bahwa bukti empiris tentang tanya-jawab Sokratik paling banyak berasal dari diskusi kelas di bidang humaniora dan ilmu sosial, sedangkan bukti di bidang STEM lebih tipis. Karena itu, dasar empiris untuk teks tertulis lebih kuat diambil dari penelitian pertanyaan sisipan.

### 3.2 Bukti efektivitas pertanyaan sisipan

Rothkopf (1970) memperkenalkan konsep *mathemagenic activities*, yaitu kegiatan pembaca yang melahirkan belajar. Konsep ini lahir dari penelitiannya tentang pertanyaan yang disisipkan dalam teks. Hamaker (1986) meninjau penelitian tentang pertanyaan sisipan (*adjunct questions*) faktual dan tingkat tinggi. Temuannya: pertanyaan sisipan memberi efek kuat pada butir tes yang sama dengan pertanyaannya dan efek lebih lemah pada butir yang berkaitan. Pertanyaan tingkat tinggi juga meningkatkan kinerja pada butir tes tingkat tinggi, termasuk yang tidak berkaitan langsung dengan pertanyaan sisipan.

Interogasi elaboratif dan penjelasan diri memberi dukungan tambahan (Chi dkk., 1989; Dunlosky dkk., 2013). Rozenblit dan Keil (2002) menunjukkan ilusi kedalaman penjelasan: orang merasa memahami suatu mekanisme jauh lebih baik daripada kemampuannya menjelaskan. Pertanyaan yang memaksa pembaca menjelaskan membongkar ilusi itu.

### 3.3 Cara menerapkannya di prosa tanpa menyebut istilahnya

Naskah tidak perlu menyebut "pertanyaan Sokratik". Yang dibutuhkan adalah pertanyaan yang muncul di tempat yang tepat dan **dijawab**, segera atau sesudah jeda.

1. **Pertanyaan sebelum penjelasan.** Ajukan satu pertanyaan sebelum membuka rumus, misalnya: "Jika sampel diperbesar empat kali, seberapa sempit selang ini?" Lalu jawab dengan perhitungan. Pertanyaan semacam ini menyiapkan pembaca untuk memperhatikan bagian yang penting.
2. **Pertanyaan berhenti sejenak.** Sesudah contoh terselesaikan, tanyakan "mengapa langkah ketiga membagi dengan *n* − 1?" dan berikan jawabannya di catatan akhir bab atau kunci. Ini meniru penjelasan diri.
3. **Pertanyaan asumsi menjelang diagnostik.** Sebelum subbab pemeriksaan model, ajukan pertanyaan asumsi, lalu tunjukkan grafik yang menjawabnya.
4. **Pertanyaan implikasi sebagai latihan.** Pindahkan pertanyaan "bagaimana jika…?" ke latihan dengan kode yang dapat diubah pembaca.
5. **Batasi jumlah.** Sebagai pegangan kerja (bukan angka dari penelitian), satu hingga tiga pertanyaan sungguhan per subbab sudah cukup.

### 3.4 Risiko

- **Pertanyaan retoris berlebihan.** Pertanyaan yang langsung dijawab di kalimat berikutnya tanpa memberi ruang berpikir hanya menambah kata. Rentetan pertanyaan juga mudah terbaca sebagai gaya yang dibuat-buat.
- **Subjudul berupa pertanyaan.** Subjudul seperti "Mengapa kita butuh prior?" menyembunyikan nama konsep dari daftar isi dan indeks. Gunakan frasa ("Peran prior dalam estimasi") dan letakkan pertanyaannya di kalimat pertama subbab bila perlu.
- **Pertanyaan tanpa jawaban.** Hamaker (1986) mengukur efek pertanyaan yang dikerjakan pembaca. Pertanyaan yang tidak pernah dijawab di mana pun membuat pembaca mandiri tidak bisa memeriksa pemahamannya. Setiap pertanyaan harus punya jawaban di naskah, di catatan, atau di kunci.
- **Pertanyaan menggiring.** Pertanyaan yang jawabannya sudah tersirat ("Bukankah jelas bahwa…?") tidak melatih penalaran.

---

## 4. Teknik Feynman: Asal, Bentuk, dan Dasar Ilmiahnya

### 4.1 Apa yang dapat dilacak dan apa yang tidak

"Teknik Feynman" sebagai **empat langkah** (pilih konsep, jelaskan seolah kepada pemula, temukan celah lalu kembali ke sumber, sederhanakan dan pakai analogi) **bukan tulisan Richard Feynman**. Penelusuran tidak menemukan nama maupun urutan langkah itu dalam tulisan Feynman. Beberapa penelusur sekunder menemukan jejak paling awal nama tersebut pada tulisan blog Scott Young sekitar Agustus–September 2011. Versi empat langkah dipopulerkan Farnam Street (Parrish) sekitar April 2012. Kedua penanggalan ini berasal dari sumber sekunder dan laman blog, sehingga statusnya adalah formulasi populer, bukan metode yang divalidasi dalam penelitian.

Yang dapat dilacak ke kehidupan Feynman hanyalah kebiasaan dan anekdot:

- Gleick (1992), dalam biografi *Genius*, menceritakan buku catatan Feynman semasa mahasiswa yang diberi judul kira-kira "buku catatan tentang hal-hal yang tidak saya ketahui". Di buku itu Feynman menyusun ulang pengetahuannya. Informasi ini terbaca dari catatan pembaca atas buku tersebut, bukan dari teks Gleick langsung.
- Goodstein dan Goodstein (1996), dalam *Feynman's Lost Lecture*, mencatat anekdot (dikenal penyusun dari kutipan sekunder) bahwa Feynman gagal menyusun kuliah tingkat mahasiswa baru tentang statistik Fermi–Dirac untuk partikel berspin setengah. Ia lalu menyimpulkan bahwa kegagalan menurunkan penjelasan ke tingkat itu berarti fisikawan belum benar-benar memahaminya.

Jadi yang otentik adalah sikapnya: kemampuan menjelaskan dengan sederhana dipakai sebagai uji pemahaman. Kemasan empat langkahnya datang kemudian.

### 4.2 Kaitan dengan temuan penelitian

Unsur-unsur teknik ini masing-masing punya padanan yang diteliti:

| Unsur populer | Padanan penelitian | Status bukti |
|---|---|---|
| Menjelaskan dengan kata sendiri | Efek penjelasan diri (Chi dkk., 1989) | Utilitas sedang menurut Dunlosky dkk. (2013) |
| Menemukan celah ketika menjelaskan | Ilusi kedalaman penjelasan (Rozenblit & Keil, 2002) | Efek kuat untuk pengetahuan penjelasan |
| Seolah mengajar orang lain | *Protégé effect*: siswa berusaha lebih keras belajar demi agen yang mereka ajari (Chase dkk., 2009) | Dua studi dengan agen yang dapat diajari |
| Analogi dan bahasa sederhana | Pemetaan struktur (Gentner, 1983); dukungan kognitif untuk analogi (Richland dkk., 2007) | Lihat Bagian 5 |

### 4.3 Penerapan dalam menulis

Teknik ini paling berguna sebagai **disiplin penulis**, bukan sebagai isi buku.

1. **Draf penjelasan tanpa notasi.** Sebelum menulis rumus, tulis satu paragraf yang menjelaskan konsep tanpa simbol. Jika paragraf itu tidak bisa ditulis, penulis belum siap menulis subbabnya.
2. **Tandai lompatan.** Baca ulang draf dan tandai setiap kata "jelas", "mudah dilihat", "dapat ditunjukkan". Di balik kata-kata itu biasanya ada langkah yang dilewati.
3. **Sederhanakan, tetapi jangan keliru.** Kalimat sederhana yang salah (misalnya "nilai-p adalah peluang H₀ benar") lebih berbahaya daripada kalimat teknis yang benar. Sederhanakan struktur kalimat, jangan sederhanakan isi.
4. **Analogi dengan batas.** Lihat Bagian 5.4.

Naskah tidak perlu menyebut nama teknik ini. Yang tampak bagi pembaca hanyalah hasilnya: penjelasan intuitif mendahului rumus, dan tidak ada langkah yang dilewati.

### 4.4 Penerapan dalam uji pembaca

- **Uji jelaskan kembali.** Minta pembaca uji (mahasiswa tingkat sasaran) membaca satu subbab, menutup buku, lalu menjelaskan konsepnya secara lisan atau tertulis dalam lima kalimat. Bagian yang tidak muncul atau keliru dalam penjelasan mereka adalah celah naskah.
- **Uji ajarkan kepada adik tingkat.** Minta pembaca uji menyiapkan penjelasan untuk mahasiswa satu tingkat di bawahnya. Menurut Chase dkk. (2009), peran mengajar mendorong usaha belajar lebih besar, sehingga pertanyaan yang muncul saat persiapan itu memetakan kesulitan nyata.
- **Catat, jangan berdebat.** Penulis mencatat di mana pembaca tersendat, bukan membela naskah.

---

## 5. Contoh yang Mudah Dipahami dan Pengetahuan Umum

### 5.1 Analogi: cara kerja dan dukungan yang dibutuhkan

Gentner (1983) memandang analogi sebagai pemetaan dari ranah sumber ke ranah sasaran. Yang dipertahankan adalah hubungan antarobjek, bukan atribut objeknya. Orang juga cenderung memilih pemetaan yang memuat hubungan tingkat tinggi seperti sebab-akibat. Gick dan Holyoak (1983) menunjukkan bahwa membandingkan dua analog membantu terbentuknya skema umum, dan skema itu memudahkan transfer. Richland dkk. (2007) membandingkan video pelajaran matematika dari TIMSS 1999. Guru AS memakai analogi sesering guru Hong Kong dan Jepang, tetapi lebih jarang memberi dukungan kognitif seperti representasi visual, gambaran mental, dan gestur yang menautkan sumber dengan sasaran.

Implikasinya: analogi yang hanya disebut sekilas kurang efektif. Analogi perlu dipetakan secara eksplisit: unsur mana di sumber berpadanan dengan unsur mana di sasaran.

### 5.2 Contoh sehari-hari dan konteks lokal

Walkington (2013) mempersonalisasi soal cerita aljabar sesuai minat siswa (olahraga, musik, film) dengan struktur matematika yang tetap sama. Siswa dalam kelompok personalisasi menyelesaikan soal lebih cepat dan lebih akurat. Efek terbesar muncul pada keterampilan menulis persamaan dari cerita, terutama pada siswa yang kesulitan, dan manfaatnya bertahan setelah personalisasi dihentikan.

GAISE College Report (Carver dkk., 2016) merekomendasikan penggunaan data nyata yang memiliki konteks dan tujuan. Gelman dan Nolan (2017) menghimpun kegiatan kelas statistika yang bertumpu pada pengalaman konkret mahasiswa.

Untuk mahasiswa STIS, konteks yang akrab sekaligus relevan dengan profesi mereka antara lain:

| Konsep | Konteks lokal yang cocok |
|---|---|
| Distribusi dan ukuran pemusatan | Pengeluaran per kapita rumah tangga (Susenas), dengan kemencengan ke kanan sebagai alasan memakai median |
| Proporsi dan ketidakpastian | Hitung cepat pemilu: mengapa sampel TPS beberapa ribu cukup |
| Deret waktu dan musiman | Harga beras bulanan, inflasi menjelang Lebaran |
| Waktu tunggu dan sebaran eksponensial | Waktu tunggu ojek daring |
| Pembobotan survei | Penimbang Sakernas atau Susenas dan perbedaan estimasi tertimbang dengan tidak tertimbang |
| Data spasial | Angka kemiskinan kabupaten/kota |
| Prior dan pembaruan keyakinan | Perkiraan panen petugas lapangan sebelum dan sesudah ubinan |

Angka dalam contoh harus berasal dari publikasi resmi BPS atau data mikro yang sah, dengan sumber dan tahun disebut. Jika data nyata tidak dapat dipakai, nyatakan dengan jelas bahwa data itu simulasi.

### 5.3 Contoh terselesaikan sebagai jenis contoh utama

Analogi menjelaskan "seperti apa", sedangkan contoh terselesaikan menunjukkan "bagaimana". Untuk prosedur, contoh terselesaikan dengan data lokal lebih bernilai daripada analogi (Atkinson dkk., 2000). Dua contoh dengan struktur sama tetapi konteks berbeda, misalnya proporsi pemilih dan proporsi rumah tangga miskin, juga membantu pembentukan skema (Gick & Holyoak, 1983).

### 5.4 Risiko analogi dan cara memberi batas

Model *Teaching With Analogies* (Glynn dkk., 1995) dikembangkan dari analogi guru dan penulis buku teks yang dinilai baik. Model ini memuat langkah eksplisit untuk menyebut **di mana analogi tidak berlaku**. Penelitian pendidikan fisika yang lebih baru mencatat bahwa langkah ini sering dilewati, sehingga risiko salah pemetaan meningkat.

Contoh risiko dalam statistika:

- "Selang kepercayaan 95% seperti jaring yang menangkap ikan 95% kali" itu benar untuk prosedurnya. Namun, pembaca mudah berpindah ke "parameter 95% berada di dalam selang ini", yang keliru dalam kerangka frekuentis.
- "Prior adalah opini" mendorong anggapan bahwa analisis Bayesian subjektif dan bebas aturan.
- "Overfitting seperti menghafal soal ujian" itu berguna, tetapi tidak menjelaskan mengapa model yang lebih sederhana bisa lebih baik.

Cara memberi batas:

1. Petakan secara eksplisit dalam tabel dua kolom (sumber ↔ sasaran).
2. Tulis satu kalimat batas: "Analogi ini berhenti berlaku ketika…".
3. Segera kembali ke representasi formal atau simulasi yang menunjukkan perilaku sebenarnya.
4. Jangan memakai satu analogi untuk dua konsep yang berbeda dalam buku yang sama.

---

## 6. Pembaca Berlapis

### 6.1 Efek pembalikan keahlian

Kalyuga dkk. (2003) meninjau penelitian yang menunjukkan bahwa teknik yang membantu pemula (misalnya contoh terselesaikan lengkap atau teks penjelas yang terintegrasi dengan diagram) dapat kehilangan manfaat, bahkan merugikan, bagi pemelajar berpengalaman. Kalyuga (2007) menjelaskannya dengan teori beban kognitif: bimbingan dari luar yang tumpang-tindih dengan skema yang sudah dimiliki pemelajar menambah beban yang tidak perlu. Ia juga menarik implikasi untuk pembelajaran yang disesuaikan dengan pemelajar, misalnya pemudaran yang adaptif.

Konsekuensinya bagi buku: satu tingkat rincian tidak akan cocok untuk semua pembaca. Penulis perlu memberi **jalur**, bukan menulis satu jalur rata-rata.

### 6.2 Teknik menulis satu buku untuk beberapa tingkat

| Teknik | Pemula | Menengah | Mahir |
|---|---|---|---|
| Teks inti | Dibaca penuh | Dibaca penuh | Dipindai |
| Contoh terselesaikan | Semua langkah | Bisa melompat ke contoh yang dipudarkan | Dilewati, langsung latihan |
| Kotak penurunan ("Penurunan lengkap") | Opsional | Dianjurkan | Dibaca |
| Kotak lanjutan ("Untuk pendalaman") | Dilewati tanpa kehilangan alur | Opsional | Dibaca |
| Latihan | Tingkat 1 (konseptual dan komputasi terpandu) | Tingkat 2 (komputasi mandiri) | Tingkat 3 (terbuka, pembuktian, desain simulasi) |

Prinsip penyusunannya:

- **Teks inti harus utuh tanpa kotak lanjutan.** Pembaca pemula yang melewati semua kotak tetap mencapai tujuan bab.
- **Peta jalur baca** di awal buku menunjukkan bab mana yang wajib, opsional, dan lanjutan untuk tiap jenis pembaca (misalnya mahasiswa D-IV, pembaca yang mempelajari sendiri, peneliti).
- **Prasyarat eksplisit** di awal bab, dengan rujukan ke bab atau lampiran untuk pembaca yang belum memenuhinya. Ini fungsi pralatih (Mayer, 2020) dan pengatur awal (Ausubel, 1960).
- **Penanda tingkat latihan** (misalnya satu, dua, atau tiga tanda) agar pembaca memilih sendiri.
- **Pemudaran contoh** (Renkl & Atkinson, 2003) sekaligus berfungsi sebagai jalur: pembaca mahir dapat langsung masuk ke contoh yang sudah dipudarkan.

### 6.3 Pembaca uji di tiap tingkat

| Tingkat | Siapa | Tugas | Yang dicatat |
|---|---|---|---|
| Pemula | Mahasiswa yang belum mengambil mata kuliah terkait | Membaca teks inti, mengerjakan latihan tingkat 1, uji jelaskan kembali | Istilah yang tidak dikenal, langkah yang dilewati, tempat tersendat |
| Menengah | Mahasiswa yang sudah lulus mata kuliah prasyarat | Menjalankan seluruh kode, mengerjakan latihan tingkat 2 | Kode yang gagal, angka yang tidak cocok, ketidakselarasan tujuan dan latihan |
| Mahir | Dosen atau alumni praktisi BPS | Membaca kotak lanjutan, memeriksa ketepatan teknis | Kesalahan konsep, penyederhanaan yang menyesatkan, rujukan |

Urutan kerja yang disarankan: pembaca mahir lebih dulu (ketepatan isi), lalu pembaca pemula (keterbacaan), lalu pembaca menengah (keterjalanan kode dan latihan). Temuan pembaca pemula tidak boleh diselesaikan dengan menambah penjelasan di teks inti yang mengganggu pembaca mahir. Penjelasan tambahan sebaiknya dimasukkan ke kotak atau lampiran (Kalyuga dkk., 2003).

---

## 7. Prinsip Khusus Buku Statistika dan Komputasi

### 7.1 Kode yang dijalankan dan direproduksi

Knuth (1984) memperkenalkan *literate programming*: program ditulis sebagai karya yang ditujukan untuk dibaca manusia, dengan penjelasan dan kode terjalin. Peng (2011) mengusulkan reproduksibilitas sebagai standar minimum bagi klaim ilmiah ketika replikasi independen tidak dapat dilakukan, dan menggambarkannya sebagai spektrum: dari publikasi saja, ke kode, ke kode dan data, sampai kode dan data yang terhubung dan dapat dieksekusi.

Bagi buku ajar, ini berarti:

- naskah ditulis dalam format yang mengeksekusi kode saat dirender (Quarto, R Markdown, Jupyter);
- versi perangkat lunak dan paket dicatat;
- benih acak (*seed*) ditetapkan untuk setiap simulasi;
- data disertakan atau diambil dengan skrip yang tercatat.

### 7.2 Angka di prosa dihitung dari kode

Setiap angka di kalimat yang berasal dari analisis (rata-rata, estimasi, batas selang, nilai statistik) harus disisipkan dari hasil kode, bukan diketik ulang. Dengan begitu, perubahan data atau model otomatis memperbarui prosa, dan angka di teks tidak berbeda dengan angka di keluaran. Ini penerapan langsung gagasan Knuth (1984) dan Peng (2011). Gerbang mutu dapat memeriksa adanya angka berdesimal yang diketik manual di prosa.

### 7.3 Urutan intuisi → rumus → interpretasi

Urutan ini adalah bentuk *concreteness fading* (Fyfe dkk., 2014) dan sejalan dengan rekomendasi GAISE untuk mengutamakan pemahaman konseptual (Carver dkk., 2016).

1. **Intuisi**: pertanyaan nyata, data, dan gambar.
2. **Rumus**: notasi dengan setiap simbol dijelaskan dalam satu tempat. Penurunan dipecah menjadi langkah bernomor, dan langkah yang panjang dipindah ke kotak.
3. **Kode**: implementasi yang dapat dicocokkan baris demi baris dengan rumus.
4. **Interpretasi**: kalimat dalam bahasa substansi, lengkap dengan satuan dan ketidakpastian, misalnya "rata-rata pengeluaran per kapita diperkirakan Rp… per bulan, dengan selang 95%…".

### 7.4 Simulasi untuk intuisi

Simulasi membuat konsep sampling yang abstrak menjadi dapat diamati. Contohnya: distribusi sampling rata-rata, makna frekuentis selang kepercayaan (berapa dari 100 selang yang memuat parameter), sebaran posterior yang menyempit saat data bertambah, dan dampak pelanggaran asumsi. GAISE menganjurkan penggunaan teknologi untuk mengeksplorasi konsep, bukan hanya untuk menghitung (Carver dkk., 2016). Simulasi juga cocok sebagai jembatan konkret ke abstrak (Fyfe dkk., 2014).

### 7.5 Data riil dan data simulasi

| Data | Kegunaan | Risiko |
|---|---|---|
| Riil (BPS, survei, administratif) | Relevansi dan motivasi; latihan menghadapi data berantakan; sesuai rekomendasi GAISE | Struktur rumit dapat mengaburkan konsep inti; ada isu lisensi dan kerahasiaan |
| Simulasi | Parameter sebenarnya diketahui, sehingga metode dapat diverifikasi; konsep dapat diisolasi | Terasa artifisial dan dapat menyesatkan bila disajikan seolah data riil |

Pola yang disarankan: kenalkan konsep dengan simulasi yang parameternya diketahui, terapkan pada data riil, lalu bandingkan. Setiap set data diberi label sumber yang jelas.

### 7.6 Visualisasi

Tufte (1983; edisi kedua 2001) memperkenalkan rasio *data-ink* (proporsi tinta yang menyajikan data terhadap seluruh tinta) dan istilah *chartjunk* untuk hiasan yang mengalihkan perhatian. Rasio ini paling tepat dipakai sebagai alat berpikir, bukan target yang dimaksimalkan secara mutlak. Wilke (2019) memberi panduan praktis tentang pemetaan data ke estetika, sistem koordinat, warna, dan pemilihan jenis grafik, serta dapat dibaca gratis di situs penulisnya.

Bagi buku ajar, kaidah ini bertemu dengan prinsip Mayer (2020):

- koherensi berarti tanpa *chartjunk*;
- kedekatan spasial berarti label langsung pada garis, bukan legenda yang jauh;
- penanda berarti judul gambar yang menyatakan temuan, bukan hanya nama variabel.

Setiap gambar dirujuk dan ditafsirkan di prosa.

### 7.7 Jenis latihan

| Jenis | Tujuan | Contoh |
|---|---|---|
| Konseptual | Memeriksa pemahaman dan miskonsepsi | Pernyataan benar–salah tentang tafsiran selang, disertai alasan |
| Komputasi | Menerapkan prosedur | Hitung posterior Beta–Binomial untuk data contoh, dengan tangan lalu dengan kode |
| Tafsiran | Menerjemahkan keluaran ke bahasa substansi | Tulis dua kalimat untuk kepala dinas berdasarkan keluaran model |
| Terbuka | Penilaian, desain, dan transfer | Rancang simulasi untuk menunjukkan kapan model gagal |
| Campuran berjarak | Retensi dan pemilihan metode | Soal yang tidak menyebut metodenya, memuat materi bab sebelumnya |

Komposisi ini memenuhi rekomendasi latihan uji, latihan berjarak, dan latihan berselang (Dunlosky dkk., 2013), serta keselarasan dengan tujuan (Biggs, 1996).

### 7.8 Kunci jawaban dan rubrik

- **Kunci untuk soal tertutup** memuat langkah dan alasan, bukan hanya angka (Shute, 2008). Kunci juga menyebut kesalahan yang lazim dan cara mengenalinya.
- **Rubrik untuk soal terbuka** menjabarkan kriteria (ketepatan, kecukupan asumsi, kejelasan tafsiran, keterulangan kode) dan tingkat capaian.
- **Kode kunci** dijalankan dalam pipeline yang sama dengan naskah, sehingga angka di kunci juga dihitung, bukan diketik.
- **Penempatan**: kunci soal ganjil dapat dimuat di buku untuk belajar mandiri, sedangkan kunci lengkap dan rubrik disediakan untuk dosen. Ini konvensi penerbitan buku teks, bukan temuan penelitian.

---

## 8. Daftar Periksa untuk Penulis dan Reviewer

Daftar ini dipakai per bab, kecuali butir yang ditandai "tingkat buku". Kolom "Dasar" menunjuk bagian kajian. Butir 31–35 ditambahkan dari Permendikbudristek 22/2022 (lihat 1.12).

| No. | Butir | Dasar |
|---|---|---|
| 1 | Tujuan bab ditulis dengan kata kerja terukur (format ABCD) dan dipetakan ke CPMK | 1.1, 2.5 |
| 2 | Setiap tujuan punya minimal satu latihan dan satu butir kunci yang mengujinya | 1.1, 7.7 |
| 3 | Prasyarat dan notasi kunci dinyatakan di awal bab | 1.3, 6.2 |
| 4 | Bab dibuka dengan masalah atau data nyata yang mengaitkan pengetahuan lama | 1.8, 5.2 |
| 5 | Enam pertanyaan perencanaan (apa, mengapa, kapan dipakai, bagaimana menghitung, bagaimana menafsirkan, kapan gagal) terjawab untuk setiap metode | 2.4 |
| 6 | Subjudul berupa frasa yang menyebut konsep, bukan kalimat tanya | 2.3, 3.4 |
| 7 | Urutan intuisi → rumus → kode → interpretasi diikuti | 1.6, 7.3 |
| 8 | Setiap simbol dijelaskan ketika pertama muncul; tidak ada "jelas" atau "mudah dilihat" yang menutupi langkah | 4.3 |
| 9 | Setiap prosedur baru diperkenalkan dengan satu contoh terselesaikan lengkap | 1.2, 5.3 |
| 10 | Contoh berikutnya dipudarkan bertahap sebelum soal mandiri | 1.7 |
| 11 | Teks dan gambar atau kode yang saling merujuk diletakkan berdekatan; label berada di dalam gambar | 1.2, 1.3 |
| 12 | Tidak ada redundansi: prosa menafsirkan tabel, tidak menyalinnya | 1.2 |
| 13 | Tidak ada materi dekoratif yang tidak menunjang tujuan | 1.3 |
| 14 | Satu sampai tiga pertanyaan sisipan per subbab, dan semuanya dijawab di teks, catatan, atau kunci | 3.2–3.4 |
| 15 | Pertanyaan meliputi minimal satu jenis asumsi atau bukti, bukan hanya klarifikasi | 3.1 |
| 16 | Minimal satu miskonsepsi yang relevan disebut, disanggah, dan dijelaskan | 1.9 |
| 17 | Setiap analogi dipetakan eksplisit dan diberi kalimat batas | 5.1, 5.4 |
| 18 | Contoh memakai konteks Indonesia yang relevan, dengan sumber data dan tahun disebut | 5.2 |
| 19 | Data simulasi diberi label sebagai simulasi; data riil diberi sumber dan lisensi | 7.5 |
| 20 | Semua kode dieksekusi saat naskah dirender, dengan benih acak dan versi paket tercatat | 7.1 |
| 21 | Tidak ada angka hasil analisis yang diketik manual di prosa | 7.2 |
| 22 | Minimal satu simulasi untuk membangun intuisi konsep sampling atau ketidakpastian | 7.4 |
| 23 | Gambar tanpa *chartjunk*, berlabel langsung, judulnya menyatakan temuan, dan ditafsirkan di prosa | 7.6 |
| 24 | Teks inti utuh tanpa kotak lanjutan; kotak lanjutan ditandai jelas | 6.2 |
| 25 | Latihan diberi tanda tingkat dan mencakup jenis konseptual, komputasi, tafsiran, dan terbuka | 6.2, 7.7 |
| 26 | Latihan akhir bab memuat soal dari bab sebelumnya dan soal yang tidak menyebut metodenya | 1.4, 7.7 |
| 27 | Kunci jawaban memuat alasan dan kesalahan lazim; soal terbuka punya rubrik | 1.10, 7.8 |
| 28 | Uji jelaskan kembali dengan pembaca uji pemula sudah dilakukan dan temuannya ditangani | 4.4, 6.3 |
| 29 | Pembaca uji mahir memeriksa ketepatan teknis, termasuk penyederhanaan yang keliru | 4.3, 6.3 |
| 30 | Bahasa sesuai EYD V (diksi, ejaan, kalimat efektif, paragraf; istilah mengikuti Pedoman Umum Pembentukan Istilah); empat standar mutu Permendikbudristek 22/2022 (materi, penyajian, desain, grafika) sudah ditinjau | 1.11, 1.12 |
| 31 | Isi dan gambar bebas dari unsur yang bertentangan dengan Pancasila, diskriminasi SARA, pornografi, kekerasan, ujaran kebencian, bias gender, dan perundungan; contoh data tentang kelompok suku, agama, atau gender ditafsirkan tanpa stereotip | 1.12 |
| 32 | Kutipan teks, gambar, data, dan kode pihak lain sah secara hak cipta dan izinnya; setiap kutipan terhubung ke daftar pustaka; setiap gambar punya judul, keterangan, legenda yang jelas, dan sumber | 1.12 |
| 33 | (Tingkat buku) Anatomi lengkap: halaman judul penuh, halaman hak cipta (ISBN, fon yang dipakai), daftar isi, prakata (tujuan, pembaca sasaran, keunggulan, pesan), petunjuk penggunaan buku, daftar pustaka, glosarium dan indeks, riwayat singkat penulis dan pelaku perbukuan; nama penulis tanpa gelar akademis | 1.12 |
| 34 | (Tingkat buku) Desain dan tipografi: paling banyak dua *typeface*, 40–70 karakter per baris, tanpa baris yatim/janda, fon berlisensi sah, gambar cetak minimal 300 dpi, gaya visual seluruh gambar selaras | 1.12 |
| 35 | (Bila ada versi elektronik) Terbaca baik di berbagai perangkat, ukuran fail relatif ringan, daftar isi tertaut, dan memperhatikan aksesibilitas bagi penyandang disabilitas | 1.12 |

---

## Daftar Pustaka

Tanda status: **[A]** berarti metadata dan temuan inti terkonfirmasi dari abstrak, katalog, atau laman penerbit; **[S]** berarti isi dikenal dari ringkasan sekunder dan perlu dicek ke teks asli sebelum dikutip. Untuk butir [S], DOI ditulis dari katalog atau ingatan penyusun dan perlu dicek ulang.

### Pendidikan, psikologi kognitif, dan desain instruksional

- Atkinson, R. K., Derry, S. J., Renkl, A., & Wortham, D. (2000). Learning from examples: Instructional principles from the worked examples research. *Review of Educational Research, 70*(2), 181–214. https://doi.org/10.3102/00346543070002181 [A]
- Atkinson, R. K., Renkl, A., & Merrill, M. M. (2003). Transitioning from studying examples to solving problems: Effects of self-explanation prompts and fading worked-out steps. *Journal of Educational Psychology, 95*(4), 774–783. https://doi.org/10.1037/0022-0663.95.4.774 [S]
- Ausubel, D. P. (1960). The use of advance organizers in the learning and retention of meaningful verbal material. *Journal of Educational Psychology, 51*(5), 267–272. https://doi.org/10.1037/h0046669 [S]
- Biggs, J. (1996). Enhancing teaching through constructive alignment. *Higher Education, 32*(3), 347–364. https://doi.org/10.1007/BF00138871 [A]
- Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin, 132*(3), 354–380. https://doi.org/10.1037/0033-2909.132.3.354 [A]
- Chandler, P., & Sweller, J. (1991). Cognitive load theory and the format of instruction. *Cognition and Instruction, 8*(4), 293–332. https://doi.org/10.1207/s1532690xci0804_2 [S]
- Chase, C. C., Chin, D. B., Oppezzo, M. A., & Schwartz, D. L. (2009). Teachable agents and the protégé effect: Increasing the effort towards learning. *Journal of Science Education and Technology, 18*(4), 334–352. https://doi.org/10.1007/s10956-009-9180-4 [A]
- Chi, M. T. H., Bassok, M., Lewis, M. W., Reimann, P., & Glaser, R. (1989). Self-explanations: How students study and use examples in learning to solve problems. *Cognitive Science, 13*(2), 145–182. https://doi.org/10.1207/s15516709cog1302_1 [A]
- Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques: Promising directions from cognitive and educational psychology. *Psychological Science in the Public Interest, 14*(1), 4–58. https://doi.org/10.1177/1529100612453266 [A]
- Fyfe, E. R., McNeil, N. M., Son, J. Y., & Goldstone, R. L. (2014). Concreteness fading in mathematics and science instruction: A systematic review. *Educational Psychology Review, 26*(1), 9–25. https://doi.org/10.1007/s10648-014-9249-3 [S]
- Gentner, D. (1983). Structure-mapping: A theoretical framework for analogy. *Cognitive Science, 7*(2), 155–170. https://doi.org/10.1207/s15516709cog0702_3 [A]
- Gick, M. L., & Holyoak, K. J. (1983). Schema induction and analogical transfer. *Cognitive Psychology, 15*(1), 1–38. https://doi.org/10.1016/0010-0285(83)90002-6 [A]
- Glynn, S. M., Duit, R., & Thiele, R. B. (1995). Teaching science with analogies: A strategy for constructing knowledge. Dalam S. M. Glynn & R. Duit (Ed.), *Learning Science in the Schools: Research Reforming Practice* (hlm. 247–273). Lawrence Erlbaum. Ringkasan: https://www.csun.edu/~vceed002/books/sourcebook/chapters/10-analogies/teaching-analogies.html [S]
- Hamaker, C. (1986). The effects of adjunct questions on prose learning. *Review of Educational Research, 56*(2), 212–242. https://doi.org/10.3102/00346543056002212 [A]
- Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research, 77*(1), 81–112. https://doi.org/10.3102/003465430298487 [A]
- Kalyuga, S. (2007). Expertise reversal effect and its implications for learner-tailored instruction. *Educational Psychology Review, 19*(4), 509–539. https://doi.org/10.1007/s10648-007-9054-3 [A]
- Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). The expertise reversal effect. *Educational Psychologist, 38*(1), 23–31. https://doi.org/10.1207/S15326985EP3801_4 [A]
- Mager, R. F. (1997). *Preparing Instructional Objectives* (ed. ke-3). Center for Effective Performance. (Edisi pertama 1962.) [S]
- Mayer, R. E. (2020). *Multimedia Learning* (ed. ke-3). Cambridge University Press. https://www.cambridge.org/9781107187504 (ISBN 978-1-107-18750-4) [A]
- Pashler, H., Bain, P. M., Bottge, B. A., Graesser, A., Koedinger, K., McDaniel, M., & Metcalfe, J. (2007). *Organizing Instruction and Study to Improve Student Learning* (NCER 2007-2004). Institute of Education Sciences, U.S. Department of Education. https://ies.ed.gov/ncee/WWC/Docs/PracticeGuide/20072004.pdf [S]
- Paul, R., & Elder, L. (2006). *The Thinker's Guide to the Art of Socratic Questioning*. Foundation for Critical Thinking. https://www.criticalthinking.org/TGS_files/SocraticQuestioning2006.pdf [S]
- Pressley, M., McDaniel, M. A., Turnure, J. E., Wood, E., & Ahmad, M. (1987). Generation and precision of elaboration: Effects on intentional and incidental learning. *Journal of Experimental Psychology: Learning, Memory, and Cognition, 13*(2), 291–300. https://doi.org/10.1037/0278-7393.13.2.291 [S]
- Renkl, A., & Atkinson, R. K. (2003). Structuring the transition from example study to problem solving in cognitive skill acquisition: A cognitive load perspective. *Educational Psychologist, 38*(1), 15–22. https://doi.org/10.1207/S15326985EP3801_3 [A]
- Richland, L. E., Zur, O., & Holyoak, K. J. (2007). Cognitive supports for analogies in the mathematics classroom. *Science, 316*(5828), 1128–1129. https://doi.org/10.1126/science.1142103 [A]
- Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science, 17*(3), 249–255. https://doi.org/10.1111/j.1467-9280.2006.01693.x [A]
- Rothkopf, E. Z. (1970). The concept of mathemagenic activities. *Review of Educational Research, 40*(3), 325–336. https://doi.org/10.3102/00346543040003325 [S]
- Rozenblit, L., & Keil, F. (2002). The misunderstood limits of folk science: An illusion of explanatory depth. *Cognitive Science, 26*(5), 521–562. https://doi.org/10.1207/s15516709cog2605_1 [A]
- Shute, V. J. (2008). Focus on formative feedback. *Review of Educational Research, 78*(1), 153–189. https://doi.org/10.3102/0034654307313795 [A]
- Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science, 12*(2), 257–285. https://doi.org/10.1207/s15516709cog1202_4 [S]
- Sweller, J., van Merriënboer, J. J. G., & Paas, F. (2019). Cognitive architecture and instructional design: 20 years later. *Educational Psychology Review, 31*(2), 261–292. https://doi.org/10.1007/s10648-019-09465-5 [A]
- Tippett, C. D. (2010). Refutation text in science education: A review of two decades of research. *International Journal of Science and Mathematics Education, 8*(6), 951–970. https://doi.org/10.1007/s10763-010-9203-x [S]
- Walkington, C. A. (2013). Using adaptive learning technologies to personalize instruction to student interests: The impact of relevant contexts on performance and learning outcomes. *Journal of Educational Psychology, 105*(4), 932–945. https://doi.org/10.1037/a0031882 [A]
- Wood, D., Bruner, J. S., & Ross, G. (1976). The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry, 17*(2), 89–100. https://doi.org/10.1111/j.1469-7610.1976.tb00381.x [A]

### Statistika, komputasi, dan visualisasi

- Carver, R., Everson, M., Gabrosek, J., Horton, N., Lock, R., Mocko, M., Rossman, A., Roswell, G. H., Velleman, P., Witmer, J., & Wood, B. (2016). *Guidelines for Assessment and Instruction in Statistics Education (GAISE) College Report 2016*. American Statistical Association. https://www.amstat.org/asa/files/pdfs/GAISE/GaiseCollege_Full.pdf [A]
- Gelman, A., & Nolan, D. (2017). *Teaching Statistics: A Bag of Tricks* (ed. ke-2). Oxford University Press. https://academic.oup.com/book/27473 [A]
- Knuth, D. E. (1984). Literate programming. *The Computer Journal, 27*(2), 97–111. https://doi.org/10.1093/comjnl/27.2.97 [A]
- Peng, R. D. (2011). Reproducible research in computational science. *Science, 334*(6060), 1226–1227. https://doi.org/10.1126/science.1213847 [A]
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (ed. ke-2). Graphics Press. (Edisi pertama 1983.) [S]
- Wilke, C. O. (2019). *Fundamentals of Data Visualization: A Primer on Making Informative and Compelling Figures*. O'Reilly Media. https://clauswilke.com/dataviz/ [A]

### 5W1H, retorika, dan Feynman

- Gleick, J. (1992). *Genius: The Life and Science of Richard Feynman*. Pantheon Books. [S]
- Goodstein, D. L., & Goodstein, J. R. (1996). *Feynman's Lost Lecture: The Motion of Planets Around the Sun*. W. W. Norton. [S]
- Sloan, M. C. (2010). Aristotle's *Nicomachean Ethics* as the original locus for the *septem circumstantiae*. *Classical Philology, 105*(3), 236–251. (DOI tidak terverifikasi; telusuri lewat JSTOR atau laman jurnal.) [S]
- Farnam Street. (t.t.). The Feynman technique. https://fs.blog/feynman-technique/ (formulasi populer empat langkah; dirujuk sebagai bukti asal-usul, bukan sebagai bukti efektivitas) [S]
- Learning Subwiki. (t.t.). Feynman technique. https://learning.subwiki.org/wiki/Feynman_technique (penelusuran penanggalan nama "Feynman technique" ke 2011) [S]

### Regulasi dan pedoman Indonesia

- Republik Indonesia. (2017). *Undang-Undang Nomor 3 Tahun 2017 tentang Sistem Perbukuan*. [S]
- Republik Indonesia. (2019). *Peraturan Pemerintah Nomor 75 Tahun 2019 tentang Peraturan Pelaksanaan UU Nomor 3 Tahun 2017 tentang Sistem Perbukuan*. [S]
- Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi. (2022a). *Peraturan Menteri Pendidikan, Kebudayaan, Riset, dan Teknologi Nomor 22 Tahun 2022 tentang Standar Mutu Buku, Standar Proses dan Kaidah Pemerolehan Naskah, serta Standar Proses dan Kaidah Penerbitan Buku* (Berita Negara Republik Indonesia Tahun 2022 Nomor 527; ditetapkan 10 Mei 2022, diundangkan 25 Mei 2022). https://static.buku.kemdikbud.go.id/content/undang-undang/PERMENDIKBUDRISTEK%20NOMOR%2022%20TAHUN%202022.pdf. Salinan lokal: `sumber/permendikbudristek-22-2022.pdf` dan `.md` (salinan JDIH, 87 halaman, diunggah penulis 7 November 2026). [A, terverifikasi dari teks lengkap]
- Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi. (2022b). *Peraturan Menteri Nomor 25 Tahun 2022 tentang Penilaian Buku Pendidikan*. https://www.peraturan.go.id/files/bn604-2022.pdf [S]
- Badan Standar, Kurikulum, dan Asesmen Pendidikan. (2022). *Peraturan Kepala BSKAP Nomor 039/H/P/2022 tentang Pedoman Penilaian Buku Pendidikan*. https://static.buku.kemdikbud.go.id/content/undang-undang/Peraturan%20kabadan%20tentang%20pedoman%20penilaian%20NOMOR%20039HP2022.pdf [S]
- Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi. (2023). *Peraturan Menteri Nomor 53 Tahun 2023 tentang Penjaminan Mutu Pendidikan Tinggi*. https://pasal.id/peraturan/permen/permendikbudriset-no-53-tahun-2023 [S]
- Direktorat Jenderal Sumber Daya Iptek dan Dikti. (2019). *Pedoman Operasional Penilaian Angka Kredit Kenaikan Jabatan Akademik/Pangkat Dosen*. https://core.ac.uk/download/200252628.pdf [S]

---

## Lampiran: Butir yang Perlu Diverifikasi Sebelum Dikutip di Naskah Buku

1. ~~Bunyi persis Pasal 8–12 Permendikbudristek 22/2022~~ **Terverifikasi 7 November 2026** dari salinan resmi yang diunggah penulis (`sumber/permendikbudristek-22-2022.md`); hasilnya di 1.11 dan 1.12. Yang masih perlu diverifikasi: isi lampiran instrumen BSKAP 039/H/P/2022 dan Permendikbudristek 25/2022 (prosedur penilaian Buku Pendidikan), termasuk apakah buku perguruan tinggi termasuk objek penilaian.
2. Status PO PAK 2019 dan definisi buku ajar dalam ketentuan angka kredit dosen yang berlaku pada 2026.
3. Rincian Permendiktisaintek 39/2025 yang menggantikan atau menyesuaikan Permendikbudristek 53/2023.
4. Penanggalan pasti tulisan Scott Young dan Farnam Street tentang "Feynman technique", serta teks anekdot Goodstein dan Goodstein (1996).
5. Daftar enam langkah model TWA dalam Glynn dkk. (1995).
6. Nomor halaman Rothkopf (1970), yang berbeda antarsumber (325–336 atau 325–337).
