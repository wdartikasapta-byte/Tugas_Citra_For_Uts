# Tugas 03 — Analisis dan Enhancement Citra Ijazah

## Deskripsi
Tugas ini merupakan implementasi pengolahan citra digital menggunakan Python untuk menganalisis dan meningkatkan kualitas citra ijazah. Program melakukan konversi citra ke grayscale, analisis histogram RGB dan grayscale, serta menerapkan metode image enhancement berdasarkan karakteristik citra.

## Tujuan 
- Memahami proses konversi citra berwarna menjadi grayscale.
- Menganalisis distribusi intensitas piksel menggunakan histogram.
- Mempelajari penerapan metode image enhancement.
- Membandingkan citra asli, grayscale, dan hasil enhancement.
- Menyimpan hasil analisis dalam bentuk gambar dan file CSV.

## Teknologi yang Digunakan
- Python
- OpenCV (`cv2`)
- NumPy
- Matplotlib
- CSV

## Metode Pengolahan Citra
1. Grayscale Conversion
2. Histogram RGB
3. Histogram Grayscale
4. Median Filter
5. Background Normalization
6. Gamma Correction
7. CLAHE (Contrast Limited Adaptive Histogram Equalization)
8. Contrast Stretching

## Struktur Folder

```text
Tugas03/
├── gambar_ijazah/
│   └── *.jpg, *.jpeg, *.png, *.bmp, *.tif, *.tiff
├── output_folder/
│   ├── grayscale/
│   ├── histogram/
│   ├── enhancement/
│   ├── perbandingan/
│   └── hasil_analisis.csv
├── analisis_citra_ijazah.py
├── materi.md
└── README.md
```

- `gambar_ijazah/` — tempat menyimpan gambar masukan.
- `output_folder/` — berisi hasil grayscale, histogram, enhancement,
  perbandingan gambar, dan laporan CSV. Subfolder output dibuat otomatis saat
  program dijalankan.
- `analisis_citra_ijazah.py` — skrip utama untuk menjalankan analisis citra.
- `materi.md` — dokumentasi materi pembelajaran.
- `README.md` — deskripsi proyek dan petunjuk penggunaan.

## Output Program
Program menghasilkan:
- Citra grayscale.
- Histogram RGB dan grayscale.
- Citra hasil enhancement.
- Gambar perbandingan citra asli, grayscale, dan enhancement.
- Laporan analisis `hasil_analisis.csv`.

## Analisis Hasil dan Jawaban

Berdasarkan nilai pada `output_folder/hasil_analisis.csv`, berikut metode yang
paling sesuai menurut aturan enhancement program untuk setiap citra. Nilai
standar deviasi (`std`) digunakan sebagai gambaran sebaran intensitas: pada
program ini, `std < 45` memicu CLAHE. Gamma Correction memakai pangkat `1.5`
untuk citra dengan rata-rata intensitas di atas `180`, sedangkan Median Filter
diterapkan jika indikator noise lebih dari `12`.

| Citra | Rata-rata | Std | Metode pada output | Alasan pemilihan |
|---|---:|---:|---|---|
| `6 Sept 2026 at 06_35(1).jpg` | 231.88 | 31.91 | Median Filter, Gamma Correction, CLAHE | Indikator noise melewati ambang, citra tergolong terang, dan `std < 45`. |
| `6 Sept 2026 at 06_35(2).jpg` | 231.34 | 32.90 | Median Filter, Gamma Correction, CLAHE | Indikator noise melewati ambang, citra tergolong terang, dan `std < 45`. |
| `6 Sept 2026 at 06_35(3).jpg` | 237.72 | 37.87 | Median Filter, Gamma Correction, CLAHE | Indikator noise melewati ambang, citra tergolong terang, dan `std < 45`. |
| `6 Sept 2026 at 06_35(4).jpg` | 239.59 | 28.73 | Gamma Correction, CLAHE | Citra tergolong terang dan `std < 45`; indikator noise tidak melewati ambang Median Filter. |
| `6 Sept 2026 at 06_35(5).jpg` | 239.20 | 33.00 | Median Filter, Gamma Correction, CLAHE | Indikator noise melewati ambang, citra tergolong terang, dan `std < 45`. |
| `6 Sept 2026 at 06_35(6).jpg` | 239.61 | 20.05 | Gamma Correction, CLAHE | Citra tergolong terang dan `std < 45`; indikator noise tidak melewati ambang Median Filter. |
| `6 Sept 2026 at 06_35(7).jpg` | 238.98 | 34.13 | Median Filter, Gamma Correction, CLAHE | Indikator noise melewati ambang, citra tergolong terang, dan `std < 45`. |
| `6 Sept 2026 at 06_35(8).jpg` | 184.56 | 22.20 | Gamma Correction, CLAHE | Rata-rata intensitas sedikit di atas ambang citra terang (`180`) dan `std < 45`. |
| `6 Sept 2026 at 06_35.jpg` | 154.94 | 15.24 | CLAHE | Rata-rata intensitas tidak memicu koreksi gamma; `std < 45` memicu CLAHE. |

Semua citra pada laporan memperoleh CLAHE karena nilai `std`-nya di bawah
`45`. Gamma Correction tidak dipakai pada citra terakhir karena rata-ratanya
berada di antara `90` dan `180`. Background Normalization tidak muncul pada
output ini karena variasi intensitas pada citra hasil Gaussian Blur tidak
melewati ambang program. Contrast Stretching juga tidak dipilih: seluruh citra
masuk ke kondisi CLAHE (`std < 45`) terlebih dahulu. Kombinasi tersebut adalah
pilihan otomatis berdasarkan ambang program; hasil akhirnya tetap perlu
diperiksa pada gambar perbandingan untuk memastikan tulisan ijazah terbaca
jelas dan tidak muncul artefak.

**Apakah histogram yang lebih tersebar selalu menunjukkan kualitas citra yang
lebih baik? Tidak.** Sebaran histogram atau nilai `std` yang lebih besar dapat
menandakan kontras yang lebih kuat, tetapi juga dapat disebabkan oleh noise,
bayangan, pencahayaan tidak merata, atau piksel yang terlalu gelap/terang.
Sebaliknya, histogram yang sempit bisa menunjukkan citra berkontras rendah,
namun belum cukup untuk menilai keterbacaan dokumen. Pada output ini, misalnya,
`6 Sept 2026 at 06_35(3).jpg` memiliki `std` tertinggi (`37.87`), sedangkan
`6 Sept 2026 at 06_35.jpg` memiliki `std` terendah (`15.24`). Angka tersebut
hanya menggambarkan sebaran intensitas, bukan bukti bahwa citra pertama pasti
lebih baik. Penilaian sebaiknya juga melihat keterbacaan teks, detail yang
terjaga, noise, pencahayaan, dan hasil enhancement.

## Cara Menjalankan Program

1. Pastikan Git dan Python sudah terpasang.
2. Clone repositori, lalu masuk ke folder proyek:

   ```bash
   git clone https://github.com/wdartikasapta-byte/Tugas_Citra_For_Uts.git
   cd Tugas_Citra_For_Uts/Tugas03
   ```

3. Masukkan gambar ijazah ke folder `gambar_ijazah/` di dalam `Tugas03/`.
4. Jalankan skrip utama dari folder `Tugas03/`:

   ```bash
   python analisis_citra_ijazah.py
   ```

5. Periksa hasil pengolahan pada folder `Tugas03/output_folder/`.

## Kesimpulan
Program ini digunakan untuk mempelajari analisis dan peningkatan kualitas citra ijazah melalui konversi grayscale, analisis histogram, serta metode enhancement adaptif. Hasil pengolahan disimpan agar dapat diperiksa dan dibandingkan dengan citra asli.