# Materi Pengolahan Citra Digital: Deteksi Tanda Tangan pada Ijazah

## 1. Pengertian

Program ini menggunakan pengolahan citra digital berbasis aturan (*rule-based*) untuk memperkirakan apakah area tertentu pada ijazah mengandung tanda tangan. Proses dilakukan menggunakan pemotongan area citra, konversi grayscale, thresholding, operasi morphology, dan perhitungan rasio piksel foreground.

## 2. Input dan Output

**Kode penting:**

```python
INPUT = "gambar_ijazah"
OUTPUT = "hasil_ttd"
ROI = (0.60, 0.65, 0.90, 0.85)
```

**Fungsi:**
- `INPUT` adalah folder gambar ijazah yang akan diproses.
- `OUTPUT` adalah folder untuk menyimpan hasil pengolahan.
- `ROI` menentukan area tanda tangan berdasarkan proporsi lebar dan tinggi citra.

## 3. Membaca dan Memeriksa Citra

**Kode penting:**

```python
img = cv2.imread(path)

if img is None:
    return
```

`cv2.imread()` membaca gambar dari file. Jika gambar gagal dibaca, fungsi dihentikan agar program tidak memproses citra yang tidak valid.

## 4. Rotasi Citra

**Kode penting:**

```python
h, w = img.shape[:2]

if h > w:
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    h, w = img.shape[:2]
```

**Fungsi:** Memutar citra sebesar 90 derajat searah jarum jam jika tinggi gambar lebih besar daripada lebarnya. Langkah ini bertujuan menyeragamkan orientasi citra sebelum ROI diambil.

## 5. Region of Interest (ROI)

ROI (*Region of Interest*) adalah area tertentu pada citra yang menjadi fokus analisis.

**Kode penting:**

```python
x0, y0, x1, y1 = ROI

crop = img[
    int(y0 * h):int(y1 * h),
    int(x0 * w):int(x1 * w)
]
```

**Fungsi:** Mengambil area gambar berdasarkan proporsi koordinat yang ditentukan dalam variabel `ROI`.

Dengan pengaturan `(0.60, 0.65, 0.90, 0.85)`, program mengambil area dari 60% hingga 90% lebar gambar dan 65% hingga 85% tinggi gambar.

## 6. Grayscale Conversion

**Kode penting:**

```python
gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
```

**Fungsi:** Mengubah ROI menjadi citra grayscale. Citra ini digunakan sebagai input untuk proses thresholding.

## 7. Metode Thresholding

Thresholding mengubah citra grayscale menjadi citra biner berdasarkan nilai ambang (*threshold*).

### 7.1 Global Threshold

**Kode penting:**

```python
_, global_bw = cv2.threshold(
    gray, 127, 255, cv2.THRESH_BINARY_INV
)
```

**Fungsi:**
- `127` adalah nilai ambang tetap.
- `255` adalah nilai maksimum piksel keluaran.
- `cv2.THRESH_BINARY_INV` menghasilkan citra biner terbalik.

Pada metode ini, piksel dengan intensitas lebih besar dari ambang akan menjadi hitam, sedangkan piksel dengan intensitas kurang dari atau sama dengan ambang akan menjadi putih.

### 7.2 Otsu Thresholding

**Kode penting:**

```python
nilai_otsu, otsu_bw = cv2.threshold(
    gray, 0, 255,
    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)
```

**Fungsi:** Menentukan nilai ambang secara otomatis berdasarkan distribusi intensitas citra.

Berbeda dengan Global Threshold yang menggunakan ambang tetap 127, Otsu memilih ambang berdasarkan histogram intensitas untuk memisahkan kelompok piksel.

Variabel `nilai_otsu` menyimpan nilai ambang yang dipilih secara otomatis.

## 8. Morphological Operations

Morphology adalah operasi pengolahan citra biner yang menggunakan elemen struktur (*structuring element*) untuk memperbaiki bentuk objek.

### 8.1 Kernel

**Kode penting:**

```python
kernel = cv2.getStructuringElement(
    cv2.MORPH_ELLIPSE, (3, 3)
)
```

**Fungsi:** Membuat elemen struktur berbentuk elips berukuran 3 × 3 yang digunakan dalam operasi morphology.

### 8.2 Morphological Opening

**Kode penting:**

```python
hasil = cv2.morphologyEx(
    bw, cv2.MORPH_OPEN, kernel
)
```

**Fungsi:** Melakukan erosi yang diikuti dilasi. Opening membantu mengurangi noise kecil yang terpisah dari objek utama.

### 8.3 Morphological Closing

**Kode penting:**

```python
hasil = cv2.morphologyEx(
    hasil, cv2.MORPH_CLOSE, kernel
)
```

**Fungsi:** Melakukan dilasi yang diikuti erosi. Closing dapat membantu menyambungkan goresan tanda tangan yang terputus atau menutup celah kecil.

## 9. Menghitung Foreground dan Rasio Tinta

Setelah thresholding dan morphology, program menghitung jumlah piksel foreground.

**Kode penting:**

```python
foreground = cv2.countNonZero(hasil)
rasio = foreground / hasil.size
```

**Fungsi:**
- `cv2.countNonZero(hasil)` menghitung jumlah piksel yang bernilai bukan nol.
- `hasil.size` menghitung jumlah seluruh piksel pada citra.
- `rasio` menunjukkan proporsi piksel foreground terhadap seluruh piksel ROI.

Karena menggunakan `THRESH_BINARY_INV`, piksel tinta yang gelap pada citra asli biasanya menjadi putih atau bernilai 255. Oleh karena itu, foreground digunakan sebagai perkiraan jumlah piksel tinta setelah morphology.

## 10. Penentuan Status Tanda Tangan

**Kode penting:**

```python
status = (
    "SIGNATURE PRESENT"
    if 0.004 <= rasio <= 0.25
    else "SIGNATURE ABSENT"
)
```

**Fungsi:** Menentukan status berdasarkan rentang rasio foreground.

- Jika rasio berada antara 0,004 dan 0,25, hasilnya `SIGNATURE PRESENT`.
- Jika rasio berada di luar rentang tersebut, hasilnya `SIGNATURE ABSENT`.

Ambang ini merupakan aturan sederhana yang perlu disesuaikan dan diuji menggunakan data citra yang tersedia. Hasilnya merupakan perkiraan berbasis aturan, bukan bukti pasti keberadaan tanda tangan.

## 11. Menyimpan Hasil Pengolahan

**Kode penting:**

```python
cv2.imwrite(
    f"{OUTPUT}/{dasar}_{nama}_gray.png",
    gray
)

cv2.imwrite(
    f"{OUTPUT}/{dasar}_{nama}_threshold.png",
    bw
)

cv2.imwrite(
    f"{OUTPUT}/{dasar}_{nama}_hasil.png",
    hasil
)
```

**Fungsi:** Menyimpan citra grayscale, hasil thresholding, dan hasil morphology untuk setiap metode, yaitu Global dan Otsu.

Hasil ini dapat digunakan untuk membandingkan bagaimana kedua metode memisahkan piksel foreground dan background.

## 12. Alur Proses Program

1. Membaca gambar ijazah.
2. Memeriksa orientasi dan memutar gambar jika diperlukan.
3. Mengambil ROI tanda tangan.
4. Mengubah ROI menjadi grayscale.
5. Melakukan Global Threshold dan Otsu Thresholding.
6. Menerapkan Morphological Opening.
7. Menerapkan Morphological Closing.
8. Menghitung jumlah foreground dan rasio tinta.
9. Menentukan status berdasarkan ambang rasio.
10. Menyimpan hasil pengolahan ke folder `hasil_ttd`.

## 13. Kesimpulan

Program ini membandingkan Global Threshold dan Otsu Thresholding untuk memisahkan foreground dan background pada area tanda tangan ijazah. Hasil citra biner diperbaiki menggunakan Morphological Opening dan Closing, kemudian dianalisis melalui rasio foreground untuk memperkirakan keberadaan tanda tangan.

Metode ini sederhana dan tidak membutuhkan pelatihan model machine learning. Namun, ketepatan hasil bergantung pada pemilihan ROI, kualitas citra, orientasi gambar, serta ambang rasio yang digunakan.