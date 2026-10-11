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

- `gambar_ijazah/` — menyimpan gambar ijazah sebagai input.
- `output_folder/` — menyimpan hasil pengolahan citra.
- `analisis_citra_ijazah.py` — kode utama untuk menjalankan analisis citra.
- `materi.md` — dokumentasi materi pembelajaran.
- `README.md` — deskripsi dan petunjuk proyek.

## Output Program
Program menghasilkan:
- Citra grayscale.
- Histogram RGB dan grayscale.
- Citra hasil enhancement.
- Gambar perbandingan citra asli, grayscale, dan enhancement.
- Laporan analisis `hasil_analisis.csv`.

## Cara Menjalankan Program

1. Pastikan Python sudah terpasang.
2. Instal pustaka yang dibutuhkan:

   ```bash
   pip install opencv-python numpy matplotlib
   ```

3. Masukkan gambar ijazah ke folder `gambar_ijazah/`.
4. Jalankan program:

   ```bash
   python analisis_citra_ijazah.py
   ```

5. Periksa hasil pengolahan pada folder `output_folder/`.

## Kesimpulan
Program ini digunakan untuk mempelajari analisis dan peningkatan kualitas citra ijazah melalui konversi grayscale, analisis histogram, serta metode enhancement adaptif. Hasil pengolahan disimpan agar dapat diperiksa dan dibandingkan dengan citra asli.