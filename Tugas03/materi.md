## Metode Image Enhancement

Pada fungsi `enhancement(gray)`, terdapat lima metode image enhancement yang digunakan untuk meningkatkan kualitas citra sebelum proses deteksi tanda tangan.

### 1. Median Filter

**Kode penting:**

```python
hasil = cv2.medianBlur(hasil, 3)
```

**Fungsi:** Mengurangi noise atau bintik-bintik pada citra menggunakan filter median dengan ukuran kernel 3 × 3.

### 2. Background Normalization

**Kode penting:**

```python
latar = cv2.GaussianBlur(hasil, (51, 51), 0)

hasil = np.clip(
    (hasil.astype(float) + 1) /
    (latar.astype(float) + 1) * np.median(latar),
    0, 255
).astype(np.uint8)
```

**Fungsi:** Membantu meratakan pencahayaan latar citra agar perbedaan pencahayaan pada beberapa bagian gambar dapat dikurangi.

### 3. Gamma Correction

**Kode penting:**

```python
tabel = np.array([
    (i / 255) ** gamma * 255
    for i in range(256)
]).astype(np.uint8)

hasil = cv2.LUT(hasil, tabel)
```

**Fungsi:** Menyesuaikan kecerahan citra berdasarkan nilai gamma. Gamma kurang dari 1 cenderung mencerahkan citra, sedangkan gamma lebih dari 1 cenderung menggelapkan citra.

### 4. CLAHE (Contrast Limited Adaptive Histogram Equalization)

**Kode penting:**

```python
hasil = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
).apply(hasil)
```

**Fungsi:** Meningkatkan kontras lokal citra sehingga detail pada bagian yang kurang jelas dapat terlihat lebih baik.

### 5. Contrast Stretching

**Kode penting:**

```python
hasil = cv2.normalize(
    hasil, None, 0, 255,
    cv2.NORM_MINMAX
)
```

**Fungsi:** Meregangkan rentang intensitas piksel ke rentang 0–255 agar perbedaan antara bagian gelap dan terang lebih terlihat.

### Catatan Pemilihan Metode

Setiap metode diterapkan berdasarkan kondisi tertentu dalam fungsi `enhancement(gray)`:

- **Median Filter:** diterapkan jika perkiraan noise lebih besar dari 12.
- **Background Normalization:** diterapkan jika simpangan baku citra latar lebih besar dari 25.
- **Gamma Correction:** dipilih berdasarkan rata-rata intensitas citra.
- **CLAHE:** diterapkan jika simpangan baku citra kurang dari 45.
- **Contrast Stretching:** dipilih jika kondisi CLAHE tidak terpenuhi dan simpangan baku citra kurang dari 60.

**Catatan:** CLAHE dan Contrast Stretching menggunakan struktur `if` dan `elif`, sehingga keduanya merupakan metode alternatif dan tidak dijalankan bersamaan dalam satu pemanggilan fungsi.