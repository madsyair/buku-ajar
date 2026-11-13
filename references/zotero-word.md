# Sitasi Zotero di DOCX (`zotero-word.lua`)

Dipasang bawaan oleh `siapkan_proyek.py` sejak 2026-11-11: `scripts/zotero-word.lua` disalin ke `_bersama/` dan didaftarkan `at: post-render` sesudah `word-otomatis.lua` di `assets/_quarto.yml`. Filter ini hanya aktif untuk DOCX; PDF tidak berubah. Ia tidak memerlukan Zotero atau Better BibTeX saat render. Asalnya seri statistika Bayesian (`naskah-bersama/zotero-word-2026-11-11.md`, uji pada Buku 3).

## Apa yang dihasilkan

- **Sitasi:** bidang Word `ADDIN ZOTERO_ITEM CSL_CITATION {…}` (format plugin Zotero). JSON-nya memuat `citationID`, `properties` (`formattedCitation`, `plainCitation`, `noteIndex`), `citationItems` dengan `itemData` CSL-JSON tersemat dari `pustaka.bib`, `uris` tiruan, `locator`/`label`/`prefix`/`suffix`/`suppress-author`, dan `schema`. Hasil bidang adalah teks citeproc proyek yang bertaut ke Daftar Pustaka, jadi dokumen tetap terbaca tanpa Zotero.
- **Sitasi naratif** (`@kunci`): nama penulis teks biasa ditambah bidang bersuppress-author "(tahun)".
- **Daftar Pustaka** (`::: {#refs}`): satu bidang `ADDIN ZOTERO_BIBL {"uncited":[],"omitted":[],"custom":[]} CSL_BIBLIOGRAPHY`.
- **Preferensi dokumen Zotero** di `docProps/custom.xml` sebagai `ZOTERO_PREF_1`, `ZOTERO_PREF_2`, … (potongan 255 karakter): `<data data-version="3">` dengan `<session>`, `<style id="…" locale="…" hasBibliography="1" bibliographyStyleHasBeenSet="1"/>`, dan `<pref name="fieldType" value="Field"/>`. Id gaya dibaca dari `<id>` berkas `csl:` (bawaan skill: APA 7, `http://www.zotero.org/styles/apa`) dan bahasa dari `lang:`. Timpa id gaya dengan metadata `zotero-word-style:`, atau matikan fitur dengan `zotero-word: false`.

## Langkah untuk penulis

1. **Pasang Zotero 7** (<https://www.zotero.org/download/>). Plugin Word ikut terpasang dan muncul sebagai tab **Zotero** di Word (Windows dan macOS). Bila tab itu tidak muncul, buka Zotero → *Edit/Zotero → Settings → Cite → Word Processors → Reinstall Microsoft Word Add-in*, lalu buka ulang Word.
2. **Buka DOCX di Word.** Word menawarkan pembaruan bidang; jawab **Ya**. Langkah ini memperbarui nomor halaman daftar isi serta nomor SEQ/REF. Bidang Zotero tidak diubah oleh F9.
3. **Zotero → Refresh** (tab Zotero di Word). Zotero membaca preferensi dokumen (APA 7, `id-ID`) dan memformat ulang semua sitasi dan Daftar Pustaka dengan citeproc-js. Butir yang tidak ada di pustaka Zotero penulis dipakai sebagai **butir tersemat** (*embedded*). Tidak ada sitasi yang hilang.
4. **Mengganti gaya:** Zotero → **Document Preferences** → pilih gaya (mis. *Chicago Manual of Style 17th edition (author-date)*) dan bahasa (*Indonesian*) → OK. Semua sitasi dan Daftar Pustaka diformat ulang. Kembali ke APA dengan cara yang sama.
5. **Menyunting sitasi:** taruh kursor di sitasi → **Add/Edit Citation**. Halaman, awalan ("lihat"), akhiran, dan *Omit Author* dapat diubah di gelembung butir. **Menyunting Daftar Pustaka:** **Add/Edit Bibliography** (mis. mengecualikan butir).
6. **Menambah sitasi baru** memerlukan butir di pustaka Zotero. Impor `pustaka.bib` buku itu sekali saja:
   - tanpa pengaya: Zotero → *File → Import… → pustaka.bib*;
   - disarankan: pasang **Better BibTeX** (<https://retorque.re/zotero-better-bibtex/>) lalu impor `pustaka.bib`. Kunci sitasi (`mroz1987`) tetap sama dengan sumber `.qmd`.
7. **Menyambungkan butir tersemat ke pustaka (opsional).** Sesudah langkah 6, butir tersemat dan butir pustaka yang sama dianggap dua butir berbeda. Untuk menyatukannya, buka Add/Edit Citation pada sitasi itu, hapus gelembung butir tersemat, lalu pilih butir yang sama dari pustaka. Bila tidak disambungkan, sitasi lama tetap benar; hanya sitasi baru dari pustaka yang bisa muncul dua kali di Daftar Pustaka bila datanya berbeda.
8. **Gaya proyek yang persis sama (opsional).** Zotero memakai APA 7 bawaannya dengan bahasa Indonesia. Hasilnya hampir sama dengan PDF; perbedaan yang diketahui ada di bawah (batasan 2). Untuk hasil identik, tambahkan `_bersama/apa.csl` proyek di Zotero → *Settings → Cite → +*. Gaya ini memakai id yang sama dengan APA bawaan, sehingga **menggantikan** APA 7 di Zotero untuk semua dokumen penulis.
9. **Naskah final ke penerbit:** Zotero → *Unlink Citations* mengubah semua bidang menjadi teks biasa. Lakukan pada salinan dokumen, karena langkah ini tidak dapat dibatalkan.

Mematikan fitur per buku: tambahkan `zotero-word: false` di `_quarto.yml` (format `docx`). Sitasi kembali menjadi teks statis bertaut.

## Batasan yang diketahui

1. **Belum diuji di Word + Zotero sungguhan.** Mesin render tidak punya Word atau Zotero. Format kode bidang, preferensi, dan perilaku butir tersemat dicocokkan dengan kode sumber Zotero (`chrome/content/zotero/xpcom/integration.js`: `DocumentData.serialize`, `Citation.loadItemData`, `Citation.toJSON`; `zotero-word-for-windows-integration`: `document.cpp` `setProperty`, potongan 255 karakter `ZOTERO_PREF_n`; `field.cpp` awalan ` ADDIN ZOTERO_`), diambil 2026-11-11. Uji Refresh di Word dulu pada salinan DOCX.
2. **Teks sesudah Refresh dapat sedikit berbeda dari PDF.** PDF diformat citeproc Pandoc dengan `apa.csl` proyek; Word diformat citeproc-js Zotero dengan APA 7 bawaan dan *locale* `id-ID`. Contohnya, istilah "Karya asli terbit" (`apa.csl` skill) menjadi "original work published" (*locale* `id-ID` resmi), dan penulisan edisi bisa berbeda. Langkah 8 menghilangkan perbedaan istilah.
3. **Nama penulis sitasi naratif adalah teks biasa.** Nama itu tidak ikut berubah saat gaya diganti. Pada gaya bernomor, "Mroz (1987)" menjadi "Mroz [1]", jadi kalimatnya perlu disunting manual.
4. **Data butir berasal dari `pustaka.bib` lewat Pandoc.** Entri `@misc` dikirim sebagai jenis CSL `document` (Pandoc memberi jenis kosong). Nomor arXiv (`eprint`) tidak dibawa; URL-nya dibawa. Perlindungan huruf kapital BibTeX (`{R}`, `{Stan}`) hilang di data tersemat. Hal ini tidak berpengaruh pada APA (judul tidak diubah hurufnya), tetapi gaya yang mengubah judul menjadi *title case* atau *sentence case* bisa salah menulis "R".
5. **Sumber kebenaran tetap `.qmd`.** Render Quarto berikutnya menimpa DOCX. Suntingan sitasi di Word tidak kembali ke `.qmd` secara otomatis.
6. **LibreOffice dan Google Docs** menampilkan teks sitasi dan Daftar Pustaka dengan benar (diperiksa lewat konversi PDF LibreOffice), tetapi plugin Zotero untuk LibreOffice dan Google Docs tidak diuji untuk dokumen ini. Google Docs membuang bidang Word.
7. **Sitasi di dalam keterangan gambar/tabel** tetap menjadi bidang Zotero. Entri Daftar Gambar/Tabel (`word-otomatis.lua`) dibuat sebelum citeproc dan memakai teks sitasi mentahnya; Word memperbaikinya saat bidang TOC diperbarui. 

## Cara kerja (untuk pemelihara)

- `_bersama/zotero-word.lua` dipasang `at: post-render` sesudah `word-otomatis.lua` dan hanya aktif untuk DOCX. Filter Quarto `post-render` berjalan **sebelum** citeproc Pandoc. Karena itu, filter menjalankan citeproc sendiri (`pandoc.utils.citeproc`, dengan CSL, `lang`, dan `link-citations` yang sama). Kemudian ia membungkus setiap `Cite` dengan bidang, mengubah `#refs` menjadi bidang ZOTERO_BIBL, dan memasang `suppress-bibliography`, sehingga citeproc kedua (bawaan Pandoc) tidak menambah apa pun.
- `itemData` = CSL-JSON dari `pandoc.utils.references` (hanya butir yang disitasi, dibaca dengan bahasa dokumen sehingga judul tidak diubah menjadi huruf kecil). `uris` diisi URI tiruan `http://zotero.org/users/local/pustakabib/items/bib_<kunci>`. URI ini tidak pernah cocok dengan butir pustaka (kunci Zotero selalu huruf kapital), sehingga Zotero memakai data tersemat. `uris` tidak boleh dikosongkan: `loadItemData` membaca `citationItem.uris.length` untuk butir tersemat.
- `plainCitation` = teks hasil bidang. Bila keduanya berbeda, Zotero menganggap sitasi disunting tangan dan bertanya saat Refresh. `formattedCitation` = RTF (`{\rtf …}` bila ada format atau huruf non-ASCII).
- `citationID` dan id sesi dibuat deterministik, jadi render ulang tanpa perubahan sumber menghasilkan kode yang sama.
- Pemeriksa: gerbang **G-DOCX** (`harness.py --render`, atau `--docx-cek <docx>`) memanggil `masalah_zotero` bila `_quarto.yml` memasang `zotero-word.lua`. Fikstur: `uji-buku/docx/docx-baik.docx` LULUS; `docx-zotero.docx` (JSON rusak) dan `docx-tanpa-otomatis.docx` (sitasi statis) GAGAL (`uji-buku/docx/buat_fikstur.py`).
