# Materi Pengolahan Citra Digital: Image Enhancement dan OCR

## 1. Grayscale Conversion

Grayscale Conversion adalah proses mengubah citra berwarna menjadi citra keabuan. Citra grayscale memiliki satu kanal intensitas dengan rentang nilai piksel 0–255.

Kode penting:

```python
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
```

Keterangan:
- `roi` adalah area citra yang diproses.
- `cv2.COLOR_BGR2GRAY` mengubah citra BGR menjadi grayscale.

## 2. Region of Interest (ROI)

ROI (*Region of Interest*) adalah bagian tertentu dari citra yang dipilih untuk menjadi fokus pengolahan.

Kode penting:

```python
h, w = img.shape[:2]

roi = img[
    int(0.887 * h):int(0.988 * h),
    int(0.157 * w):int(0.314 * w)
]
```

ROI digunakan untuk mengambil area yang diperkirakan berisi nomor ijazah sehingga proses OCR berfokus pada bagian tersebut.

## 3. Metode Image Enhancement

Image Enhancement merupakan proses meningkatkan kualitas visual citra agar informasi di dalamnya lebih mudah diamati atau diproses.

### 3.1 Brightness

Brightness adalah metode untuk menyesuaikan kecerahan citra.

Kode penting:

```python
cv2.convertScaleAbs(gray, beta=50)
```

Fungsi:
- `gray` merupakan citra grayscale yang diproses.
- `beta=50` menambahkan offset kecerahan sebesar 50.
- Metode ini membuat citra cenderung lebih terang.

### 3.2 Contrast

Contrast Enhancement bertujuan memperlebar rentang intensitas piksel agar perbedaan antara bagian gelap dan terang lebih terlihat.

Kode penting:

```python
contrast = np.clip(
    (gray.astype(float) - mn) * 255 / (mx - mn),
    0, 255
).astype(np.uint8) if mx != mn else gray.copy()
```

Keterangan:
- `mn` adalah intensitas minimum.
- `mx` adalah intensitas maksimum.
- `np.clip()` membatasi nilai piksel pada rentang 0–255.
- Jika `mn` sama dengan `mx`, program menggunakan salinan citra asli untuk menghindari pembagian dengan nol.

### 3.3 Histogram Equalization

Histogram Equalization berfungsi untuk meningkatkan kontras dengan meratakan distribusi intensitas piksel.

Kode penting:

```python
cv2.equalizeHist(gray)
```

Metode ini bekerja pada citra grayscale dan dapat membantu memperjelas detail tertentu yang sebelumnya kurang terlihat.

## 4. Histogram Citra

Histogram citra menggambarkan distribusi frekuensi intensitas piksel.

Kode penting:

```python
plt.hist(citra.ravel(), bins=256, range=(0, 256))
```

Keterangan:
- `citra.ravel()` meratakan matriks citra menjadi satu dimensi.
- `bins=256` membagi intensitas menjadi 256 kelompok.
- `range=(0, 256)` menetapkan rentang intensitas yang ditampilkan.

Histogram digunakan untuk mengamati distribusi intensitas sebelum dan sesudah enhancement.

## 5. Optical Character Recognition (OCR)

OCR (*Optical Character Recognition*) adalah teknologi yang digunakan untuk mengenali teks dari gambar dan mengubahnya menjadi teks digital.

Kode penting:

```python
teks = pytesseract.image_to_string(
    citra,
    config=CONFIG
)
```

Konfigurasi OCR:

```python
CONFIG = "--psm 7 -c tessedit_char_whitelist=0123456789"
```

Keterangan:
- `pytesseract.image_to_string()` mengambil teks dari citra.
- `--psm 7` mengatur Tesseract agar memproses area sebagai satu baris teks.
- `tessedit_char_whitelist=0123456789` membatasi karakter yang dikenali menjadi angka.

Untuk menyaring hasil OCR agar hanya berisi angka:

```python
teks = "".join(c for c in teks if c.isdigit())
```

## 6. Character Error Rate (CER)

CER (*Character Error Rate*) merupakan ukuran untuk mengevaluasi kesalahan karakter pada hasil OCR dengan membandingkannya terhadap teks referensi atau *ground truth*.

Rumus:

\[
CER = \frac{S+D+I}{N}\times100\%
\]

Keterangan:
- \(S\): jumlah karakter yang salah diganti (*substitution*).
- \(D\): jumlah karakter yang hilang (*deletion*).
- \(I\): jumlah karakter tambahan (*insertion*).
- \(N\): jumlah karakter pada teks referensi.

Kode pemanggilan perhitungan CER:

```python
cer = round(
    hitung_cer(GROUND_TRUTH, teks), 2
)
```

Interpretasi:
- CER 0% berarti hasil OCR sama persis dengan teks referensi.
- Semakin rendah nilai CER, semakin kecil tingkat kesalahan karakter.
- CER yang tinggi menunjukkan lebih banyak kesalahan pengenalan karakter.

## 7. Perbandingan Metode Enhancement

Program membandingkan hasil OCR dari:
1. Tanpa Enhancement sebagai baseline.
2. Brightness.
3. Contrast.
4. Histogram Equalization.

Setiap hasil OCR dievaluasi menggunakan CER. Metode enhancement dengan nilai CER terendah dipilih sebagai metode terbaik di antara metode yang diuji.

Hasil terbaik dapat berbeda bergantung pada kondisi citra, kualitas gambar, pencahayaan, dan kejelasan karakter.

## 8. Penyimpanan Hasil Analisis

Program menyimpan hasil evaluasi dalam file CSV.

Kode penting:

```python
pd.DataFrame(semua).to_csv(
    OUTPUT / "perbandingan_ketiga_metode.csv",
    index=False,
    encoding="utf-8-sig"
)
```

CSV digunakan untuk menyimpan tabel hasil OCR dan CER agar mudah diperiksa serta dibuka menggunakan aplikasi spreadsheet.

## 9. Kesimpulan Materi

Image enhancement dapat membantu memperbaiki tampilan citra sebelum proses OCR. Brightness mengatur kecerahan, Contrast meregangkan rentang intensitas, dan Histogram Equalization memperbaiki distribusi intensitas. Kualitas hasil pengenalan teks kemudian dievaluasi menggunakan CER untuk mengetahui tingkat kesalahan karakter.

Metode dengan CER terendah merupakan metode terbaik berdasarkan hasil pengujian pada citra yang digunakan.