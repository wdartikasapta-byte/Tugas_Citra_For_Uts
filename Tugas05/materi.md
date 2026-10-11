# Materi Pengolahan Citra Digital: Image Filtering dan OCR Nomor Ijazah

## 1. Pengertian Image Filtering

Image Filtering adalah proses pengolahan citra untuk mengurangi noise, menghaluskan citra, atau memperjelas detail gambar. Pada program ini, filtering digunakan untuk membandingkan pengaruh beberapa metode terhadap hasil pembacaan nomor ijazah menggunakan Optical Character Recognition (OCR).

## 2. Crop dan Grayscale

### 2.1 Crop Region of Interest (ROI)

ROI (*Region of Interest*) adalah bagian citra yang dipilih untuk diproses lebih lanjut. Pada program ini, ROI digunakan untuk mengambil area yang diperkirakan berisi nomor ijazah.

**Kode penting:**

```python
h, w = img.shape[:2]

crop = img[
    int(0.887 * h):int(0.988 * h),
    int(0.157 * w):int(0.314 * w)
]
```

**Fungsi:**
- `h` menyimpan tinggi citra.
- `w` menyimpan lebar citra.
- `crop` mengambil area tertentu berdasarkan persentase tinggi dan lebar citra.

### 2.2 Grayscale Conversion

Grayscale Conversion adalah proses mengubah citra berwarna menjadi citra keabuan.

**Kode penting:**

```python
return cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
```

**Fungsi:** Mengubah ROI menjadi citra grayscale agar proses filtering dan OCR lebih sederhana.

## 3. Empat Metode Filtering

Program menguji empat metode filtering dan satu citra asli sebagai pembanding.

### 3.1 Original

**Kode penting:**

```python
"Original": gray
```

**Fungsi:** Menggunakan citra grayscale tanpa filtering tambahan sebagai baseline untuk membandingkan hasil metode lainnya.

### 3.2 Mean Filter

**Kode penting:**

```python
cv2.blur(gray, (3, 3))
```

**Fungsi:** Menghaluskan citra dengan menghitung rata-rata nilai piksel pada lingkungan kernel berukuran 3 × 3. Metode ini dapat mengurangi noise, tetapi juga dapat mengaburkan detail karakter.

### 3.3 Median Filter

**Kode penting:**

```python
cv2.medianBlur(gray, 3)
```

**Fungsi:** Mengurangi noise dengan mengganti nilai piksel berdasarkan median piksel di lingkungan berukuran 3 × 3. Metode ini sering digunakan untuk mengurangi noise berbentuk bintik.

### 3.4 Gaussian Filter

**Kode penting:**

```python
cv2.GaussianBlur(gray, (3, 3), 0)
```

**Fungsi:** Menghaluskan citra menggunakan pembobotan Gaussian. Piksel yang lebih dekat dengan pusat kernel memperoleh bobot lebih besar sehingga citra menjadi lebih halus.

### 3.5 Sharpening

**Kode penting:**

```python
kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])

cv2.filter2D(gray, -1, kernel)
```

**Fungsi:** Mempertegas tepi dan detail karakter melalui operasi konvolusi menggunakan kernel sharpening.

## 4. Pembesaran Citra

Sebelum OCR, citra diperbesar empat kali.

**Kode penting:**

```python
besar = cv2.resize(
    citra, None,
    fx=4, fy=4,
    interpolation=cv2.INTER_CUBIC
)
```

**Fungsi:**
- `fx=4` memperbesar lebar empat kali.
- `fy=4` memperbesar tinggi empat kali.
- `cv2.INTER_CUBIC` menggunakan interpolasi kubik untuk memperkirakan nilai piksel baru.

Pembesaran dapat membantu OCR memproses karakter kecil, tetapi tidak menjamin akurasi selalu meningkat.

## 5. Thresholding dengan Metode Otsu

Thresholding mengubah citra grayscale menjadi citra biner berdasarkan ambang intensitas.

**Kode penting:**

```python
_, binary = cv2.threshold(
    besar, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)
```

**Fungsi:**
- `besar` adalah citra yang sudah diperbesar.
- `cv2.THRESH_BINARY` menghasilkan citra biner.
- `cv2.THRESH_OTSU` menentukan ambang secara otomatis berdasarkan histogram intensitas.
- `0` adalah nilai ambang awal yang tidak digunakan sebagai ambang tetap ketika Otsu menghitung ambang optimal.

Hasil thresholding digunakan sebagai input untuk proses OCR.

## 6. Optical Character Recognition (OCR)

OCR adalah teknologi untuk mengenali teks dari citra dan mengubahnya menjadi teks digital.

**Kode penting:**

```python
teks = pytesseract.image_to_string(
    binary,
    config="--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789"
)
```

**Fungsi konfigurasi:**
- `--oem 3` menggunakan pemilihan mesin OCR otomatis yang tersedia pada Tesseract.
- `--psm 7` memperlakukan area sebagai satu baris teks.
- `tessedit_char_whitelist=0123456789` membatasi karakter yang dikenali menjadi angka.

Hasil OCR kemudian dibersihkan agar hanya berisi digit.

**Kode penting:**

```python
teks = re.sub(r"\D", "", teks)
```

Fungsi `re.sub()` menghapus karakter yang bukan angka dari hasil OCR.

## 7. Evaluasi Hasil OCR

Program membandingkan hasil OCR dengan nomor referensi (*ground truth*):

```python
GROUND_TRUTH = "571012022000056"
```

Jumlah karakter yang cocok dihitung berdasarkan posisi:

```python
benar = sum(
    a == b for a, b in zip(teks, GROUND_TRUTH)
)

akurasi = benar / len(GROUND_TRUTH) * 100
```

**Fungsi:**
- `zip()` memasangkan karakter berdasarkan posisinya.
- `a == b` memeriksa apakah dua karakter pada posisi yang sama cocok.
- `benar` menghitung jumlah pasangan karakter yang cocok.
- `akurasi` menghitung persentase kecocokan terhadap panjang teks referensi.

**Catatan:** Perhitungan ini adalah persentase kecocokan karakter berdasarkan posisi, bukan metrik CER yang menghitung operasi substitusi, penghapusan, dan penyisipan. Hasilnya dapat kurang representatif jika panjang teks OCR berbeda dari panjang teks referensi.

## 8. Penyimpanan Citra Hasil Filtering

Program menyimpan citra hasil setiap metode ke folder `filtered_ijazah`.

**Kode penting:**

```python
cv2.imwrite(
    os.path.join(OUTPUT_FOLDER, nama_file),
    citra
)
```

**Fungsi:** Menyimpan citra hasil filtering sebagai file gambar agar dapat diperiksa dan dibandingkan dengan citra metode lainnya.

## 9. Perhitungan Rata-Rata Akurasi

Program mengumpulkan nilai akurasi dari setiap gambar untuk menghitung rata-rata per metode.

**Kode penting:**

```python
nilai = [
    x["Akurasi"]
    for x in semua_hasil
    if x["Metode"] == nama
]

rata = sum(nilai) / len(nilai) if nilai else 0
```

**Fungsi:** Mengambil nilai akurasi untuk metode tertentu, menjumlahkannya, lalu membaginya dengan jumlah hasil yang tersedia. Jika tidak ada data, nilai rata-rata ditetapkan menjadi 0.

## 10. Alur Proses Program

1. Membaca gambar ijazah.
2. Mengambil ROI nomor ijazah.
3. Mengubah ROI menjadi grayscale.
4. Membuat citra Original, Mean Filter, Median Filter, Gaussian Filter, dan Sharpening.
5. Memperbesar setiap citra empat kali.
6. Melakukan thresholding menggunakan Otsu.
7. Membaca nomor menggunakan Tesseract OCR.
8. Membersihkan hasil OCR agar hanya berupa angka.
9. Menghitung persentase kecocokan karakter.
10. Menyimpan citra hasil filtering dan menampilkan ringkasan rata-rata akurasi.

## 11. Kesimpulan

Program ini membandingkan empat metode filtering—Mean Filter, Median Filter, Gaussian Filter, dan Sharpening—dengan citra Original sebagai baseline. Hasil setiap metode diproses melalui pembesaran citra, thresholding Otsu, dan OCR. Persentase kecocokan karakter kemudian digunakan untuk mengevaluasi hasil pembacaan nomor ijazah.

Metode terbaik ditentukan berdasarkan hasil pengujian pada gambar yang digunakan, karena setiap metode dapat memberikan hasil berbeda bergantung pada noise, ketajaman karakter, dan kualitas citra.