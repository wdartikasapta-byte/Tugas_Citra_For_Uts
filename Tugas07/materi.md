# Materi Pengolahan Citra Digital: Integrasi OCR dan Deteksi Tanda Tangan Ijazah

## 1. Deskripsi Materi

Program ini mengintegrasikan dua proses pengolahan citra, yaitu pembacaan nomor ijazah menggunakan Optical Character Recognition (OCR) dan deteksi tanda tangan menggunakan thresholding serta operasi morfologi.

Hasil kedua proses digunakan untuk menghasilkan keputusan verifikasi berdasarkan kesesuaian nomor ijazah dengan teks acuan dan keberadaan tanda tangan yang terdeteksi.

## 2. Konfigurasi Program

**Kode penting:**

```python
FOLDER_CITRA = "gambar_ijazah"
GROUND_TRUTH = "571012022000056"
OUTPUT_FOLDER = "hasil_integrasi_proyek_mini"

IJAZAH_ROIS = {
    "nomor": (0.887, 0.988, 0.157, 0.314),
    "ttd": (0.600, 0.850, 0.650, 0.900),
}
```

**Fungsi:**
- `FOLDER_CITRA`: folder gambar ijazah masukan.
- `GROUND_TRUTH`: nomor referensi untuk mengevaluasi hasil OCR.
- `OUTPUT_FOLDER`: folder penyimpanan hasil pengolahan.
- `IJAZAH_ROIS`: koordinat relatif untuk area nomor dan tanda tangan.

## 3. Crop Region of Interest (ROI)

ROI (*Region of Interest*) adalah bagian citra yang dipilih sebagai fokus pengolahan.

**Kode penting:**

```python
h, w = img.shape[:2]
y1_rel, y2_rel, x1_rel, x2_rel = IJAZAH_ROIS[section]

y1, y2 = int(y1_rel * h), int(y2_rel * h)
x1, x2 = int(x1_rel * w), int(x2_rel * w)

return img[y1:y2, x1:x2].copy()
```

**Fungsi:** Mengubah koordinat relatif menjadi koordinat piksel, kemudian mengambil area nomor ijazah atau tanda tangan.

## 4. Grayscale dan CLAHE

### 4.1 Grayscale Conversion

**Kode penting:**

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

**Fungsi:** Mengubah citra berwarna menjadi citra keabuan untuk mempermudah pengolahan intensitas piksel.

### 4.2 CLAHE

**Kode penting:**

```python
clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

enhanced = clahe.apply(gray)
```

**Fungsi:** Meningkatkan kontras lokal citra agar detail tertentu lebih terlihat. Citra hasil CLAHE kemudian digunakan untuk mengambil ROI nomor dan tanda tangan.

## 5. Filtering pada Nomor Ijazah

Program menerapkan empat jenis filter pada ROI nomor ijazah.

### 5.1 Mean Filter

```python
cv2.blur(crop_nomor, (3, 3))
```

Menghaluskan citra dengan menghitung rata-rata piksel pada lingkungan kernel 3 × 3.

### 5.2 Median Filter

```python
cv2.medianBlur(crop_nomor, 3)
```

Mengurangi noise dengan mengganti nilai piksel berdasarkan median piksel tetangganya.

### 5.3 Gaussian Filter

```python
cv2.GaussianBlur(crop_nomor, (3, 3), 0)
```

Menghaluskan citra menggunakan pembobotan Gaussian untuk mengurangi noise.

### 5.4 Sharpening

```python
cv2.filter2D(
    crop_nomor,
    -1,
    np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
)
```

Mempertegas tepi dan detail karakter agar bentuk angka lebih terlihat.

## 6. Optical Character Recognition (OCR)

OCR adalah proses mengenali teks dari gambar menjadi teks digital menggunakan mesin pengenalan karakter.

**Kode penting:**

```python
custom_config = (
    r"--psm 7 -c tessedit_char_whitelist=0123456789/ABCDEFGHIJKLMNOPQRSTUVWXYZ.-"
)

return pytesseract.image_to_string(
    crop_nomor_filtered,
    config=custom_config
).strip()
```

**Fungsi:**
- `pytesseract.image_to_string()` membaca teks dari citra.
- `--psm 7` mengatur citra sebagai satu baris teks.
- `tessedit_char_whitelist` membatasi karakter yang diizinkan.
- `.strip()` menghapus spasi di awal dan akhir hasil OCR.

## 7. Evaluasi OCR dengan Character Error Rate (CER)

CER (*Character Error Rate*) mengukur tingkat kesalahan karakter hasil OCR terhadap teks acuan.

**Kode penting:**

```python
return (
    dp[len(ref)][len(hyp)] / float(len(ref))
    if len(ref) > 0 else 0.0
)
```

Program menggunakan jarak Levenshtein dengan *Dynamic Programming* untuk menghitung jumlah minimum operasi perubahan karakter.

Rumus:

\[
CER = \frac{S+D+I}{N}
\]

Keterangan:
- \(S\): karakter yang salah diganti (*substitution*).
- \(D\): karakter yang hilang (*deletion*).
- \(I\): karakter tambahan (*insertion*).
- \(N\): jumlah karakter pada teks acuan.

CER dikembalikan dalam bentuk rasio, bukan persentase. Nilai CER yang lebih rendah menunjukkan hasil OCR yang lebih mendekati teks acuan.

## 8. Deteksi Tanda Tangan

Deteksi tanda tangan dilakukan pada ROI TTD yang telah dipotong dari citra hasil CLAHE.

### 8.1 Otsu Thresholding

**Kode penting:**

```python
_, thresh_ttd = cv2.threshold(
    crop_ttd,
    0,
    255,
    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)
```

**Fungsi:** Mengubah citra menjadi citra biner dan menentukan nilai ambang secara otomatis menggunakan metode Otsu. `THRESH_BINARY_INV` membalik hasil biner sehingga goresan gelap umumnya menjadi piksel putih.

### 8.2 Morphological Opening

**Kode penting:**

```python
opening_ttd = cv2.morphologyEx(
    thresh_ttd,
    cv2.MORPH_OPEN,
    kernel
)
```

**Fungsi:** Mengurangi noise kecil pada citra biner.

### 8.3 Morphological Closing

**Kode penting:**

```python
morph_ttd = cv2.morphologyEx(
    opening_ttd,
    cv2.MORPH_CLOSE,
    kernel
)
```

**Fungsi:** Membantu menutup celah kecil dan menyambungkan bagian goresan yang terputus.

### 8.4 Penghitungan Piksel dan Penentuan Status

**Kode penting:**

```python
pixel_count = cv2.countNonZero(morph_ttd)
status_ttd = "PRESENT" if pixel_count > 500 else "ABSENT"
```

**Fungsi:** Menghitung piksel putih setelah morfologi. Jika jumlahnya lebih dari 500, program menetapkan status `PRESENT`; jika tidak, statusnya `ABSENT`.

Ambang 500 merupakan aturan sederhana yang perlu diuji dan disesuaikan dengan ukuran ROI serta data pengujian.

## 9. Integrasi Keputusan Verifikasi

**Kode penting:**

```python
is_nomor_valid = nomor_text == ground_truth
is_ttd_valid = status_ttd == "PRESENT"

if is_nomor_valid and is_ttd_valid:
    status_verifikasi = "TERVERIFIKASI (VALID)"
elif not is_nomor_valid and not is_ttd_valid:
    status_verifikasi = "GAGAL (Nomor Salah & TTD Absen)"
elif not is_nomor_valid:
    status_verifikasi = "GAGAL (Nomor Tidak Sesuai)"
else:
    status_verifikasi = "GAGAL (TTD Tidak Ditemukan)"
```

**Fungsi:** Menggabungkan hasil OCR dan deteksi tanda tangan untuk menghasilkan status verifikasi akhir.

- Nomor sesuai dan TTD terdeteksi: `TERVERIFIKASI (VALID)`.
- Nomor tidak sesuai dan TTD tidak terdeteksi: `GAGAL (Nomor Salah & TTD Absen)`.
- Nomor tidak sesuai: `GAGAL (Nomor Tidak Sesuai)`.
- Nomor sesuai tetapi TTD tidak terdeteksi: `GAGAL (TTD Tidak Ditemukan)`.

Status tersebut merupakan keputusan berdasarkan aturan program, bukan bukti pasti keaslian dokumen.

## 10. Output Program

Program menyimpan hasil pengolahan ke folder `hasil_integrasi_proyek_mini`, meliputi:

- ROI tanda tangan hasil pemotongan.
- Citra tanda tangan setelah operasi morfologi.
- Citra nomor ijazah hasil setiap metode filtering.
- Tabel hasil OCR, CER, status tanda tangan, dan status verifikasi yang ditampilkan di terminal.

## 11. Alur Proses Program

1. Membaca gambar ijazah.
2. Mengubah citra menjadi grayscale.
3. Menerapkan CLAHE.
4. Mengambil ROI nomor ijazah dan ROI tanda tangan.
5. Memproses ROI nomor menggunakan Mean, Median, Gaussian, dan Sharpening.
6. Membaca nomor ijazah menggunakan Tesseract OCR.
7. Menghitung CER setiap hasil OCR.
8. Memproses ROI tanda tangan menggunakan Otsu Thresholding.
9. Menerapkan Morphological Opening dan Closing.
10. Menghitung piksel putih untuk menentukan status tanda tangan.
11. Menggabungkan hasil nomor dan tanda tangan menjadi status verifikasi.
12. Menyimpan citra hasil pengolahan.

## 12. Kesimpulan

Program ini mengintegrasikan pengolahan citra, filtering, OCR, evaluasi CER, dan deteksi tanda tangan berbasis aturan. Hasil OCR dibandingkan dengan nomor referensi, sedangkan keberadaan tanda tangan diperkirakan melalui jumlah piksel putih setelah thresholding dan operasi morfologi.

Hasil akhirnya ditentukan berdasarkan kedua pemeriksaan tersebut. Keakuratan program tetap bergantung pada kualitas gambar, ketepatan ROI, hasil OCR, dan ambang deteksi tanda tangan yang digunakan.