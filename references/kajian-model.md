# Kajian model per peran agen (uji banding, 2026-11-12/13)

Tujuan: menguji pemetaan model per peran (`agents/00-orkestrator.md`, bagian Hemat token) dengan uji banding pada pekerjaan nyata. Setiap pasangan agen bekerja terpisah pada bahan yang sama dengan instruksi identik.

| Uji | Peran / bahan | Model | Temuan | Token | Waktu | Catatan |
|---|---|---|---|---|---|---|
| 1 | Reviewer isi, bab model Stan | Fable | 1 MAYOR, 7 MINOR | 253 rb | 10,6 mnt | MAYOR identik dengan Opus (dibuktikan dengan CmdStan) |
| 1 | | Opus | 1 MAYOR, 7 MINOR | 273 rb | 11,6 mnt | 3 MINOR sama, masing-masing 4 MINOR unik |
| 2 | Reviewer rumus, bab SBC | Fable | 0 MAYOR, 8 MINOR | 179 rb | 4,3 mnt | Unik: densitas tanpa Jacobian tidak *proper*; tidak menghitung ulang angka Stan |
| 2 | | Opus | 0 MAYOR, 9 MINOR | 182 rb | 4,4 mnt | Unik: syarat *draws* saling bebas (dibantah contoh bab); menghitung ulang SBC, pita, Jacobian, ESS |
| 3 | Pembaca pemula, bab pengantar | Sonnet | 3 MAYOR, 18 MINOR | 125 rb | 2,8 mnt | Tiga masalah inti sama dengan Opus |
| 3 | | Opus | 2 MAYOR, 15 MINOR | 153 rb | 4,0 mnt | Satu temuan tambahan |
| 4 | Inventaris harness (mekanis) | Haiku | G-RUMUS 200, EYD 690 | 212 rb | 2,9 mnt | Angka **tepat** (dicek dengan skrip) |
| 4 | | Sonnet | G-RUMUS 192, EYD 690 | 92 rb | 1,2 mnt | G-RUMUS **salah hitung** 8 |

Kesimpulan:

1. **Fable setara Opus** untuk peran reviewer (isi, rumus) pada dua uji: jumlah dan bobot temuan sama, masalah mayor sama, biaya sedikit lebih rendah. Opus lebih konsisten menghitung ulang angka. Untuk bab penting, dua reviewer dengan model berbeda (Opus dan Fable) menangkap lebih banyak, karena setiap uji memberi temuan unik di kedua sisi.
2. **Sonnet cukup untuk pembaca pemula**: masalah inti sama dengan Opus, ±20% lebih hemat.
3. **Haiku layak untuk tugas mekanis berbasis hitungan**, tetapi memakai token lebih banyak. Hasil hitungan tetap dicek dengan skrip.
4. Keterbatasan: satu bab per uji; temuan unik belum semuanya diverifikasi kebenarannya.

Cara memperbarui tabel model: uji banding per peran dengan pekerjaan nyata, seperti di atas.
