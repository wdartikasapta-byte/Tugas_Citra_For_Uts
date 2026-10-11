# Tugas 07 — Integrasi OCR Nomor Ijazah dan Deteksi Tanda Tangan

## Deskripsi

Mini project ini menggabungkan dua pemeriksaan pada gambar ijazah:

1. Membaca nomor ijazah dengan Tesseract OCR dan mengukur kesalahan hasilnya
   menggunakan *Character Error Rate* (CER).
2. Memperkirakan ada atau tidaknya tanda tangan kepala sekolah berdasarkan
   jumlah piksel foreground pada ROI tanda tangan.

Nomor hasil OCR dan status tanda tangan kemudian digabungkan menjadi status
verifikasi. Program ini merupakan demonstrasi pengolahan citra berbasis
aturan; hasilnya bukan bukti keaslian ijazah.

## Repository dan Kode

- Repository: [wdartikasapta-byte/Tugas_Citra_For_Uts](https://github.com/wdartikasapta-byte/Tugas_Citra_For_Uts)
- Folder Tugas 07: [Tugas07](https://github.com/wdartikasapta-byte/Tugas_Citra_For_Uts/tree/main/Tugas07)
- Skrip utama: [`verifikasi_file_ijazah.py`](verifikasi_file_ijazah.py)

## Isi Folder

```text
Tugas07/
├── gambar_ijazah/
│   └── 9 gambar ijazah dengan variasi kualitas
├── hasil_integrasi_proyek_mini/
│   └── hasil crop tanda tangan, morphology, dan filter nomor
├── verifikasi_file_ijazah.py
├── materi.md
└── README.md
```

Gambar input mencakup variasi kualitas seperti kontras rendah, blur, noise,
resolusi rendah, underexposure, perubahan warna, artefak JPEG, dan degradasi
gabungan.

## Metode

### Persiapan gambar dan ROI

Skrip membaca gambar dari `gambar_ijazah/`, mengubahnya menjadi grayscale,
kemudian menerapkan CLAHE (*Contrast Limited Adaptive Histogram
Equalization*) dengan `clipLimit=2.0` dan `tileGridSize=(8, 8)`. CLAHE
meningkatkan kontras lokal sebelum dua ROI dipotong berdasarkan proporsi
koordinat gambar:

- **Nomor:** `(ymin, ymax, xmin, xmax) = (0.887, 0.988, 0.157, 0.314)`.
- **Tanda tangan:** `(0.600, 0.850, 0.650, 0.900)`.

Koordinat tersebut mengasumsikan gambar memiliki orientasi dan tata letak
seperti dataset. Jika tata letak masukan berbeda, ROI perlu disesuaikan.

### Membaca nomor dengan OCR

Pada ROI nomor, skrip membandingkan empat filter:

- **Mean** — perataan lokal 3 × 3 untuk menghaluskan noise, tetapi dapat
  mengaburkan detail angka.
- **Median** — median lokal dengan kernel 3 × 3; berguna untuk noise impulsif
  dan cenderung menjaga tepi.
- **Gaussian** — penghalusan berbobot Gaussian dengan kernel 3 × 3.
- **Sharpen** — penajaman dengan kernel
  `[[0,-1,0],[-1,5,-1],[0,-1,0]]` untuk menegaskan tepi; dapat memperkuat
  noise.

Setiap hasil filter dikirim ke Tesseract dengan `--psm 7` (satu baris) dan
whitelist karakter `0123456789/ABCDEFGHIJKLMNOPQRSTUVWXYZ.-`. Hasil OCR
dibandingkan dengan ground truth `571012022000056`.

CER dihitung menggunakan jarak Levenshtein:

\[
CER = \frac{S + D + I}{N}
\]

dengan \(S\) sebagai substitution, \(D\) sebagai deletion, \(I\) sebagai
insertion, dan \(N\) sebagai jumlah karakter ground truth. CER berupa rasio;
nilai lebih kecil berarti OCR lebih dekat ke acuan, dan CER 0 berarti cocok
persis.

### Menentukan filter paling efektif berdasarkan CER

Metode yang paling efektif adalah metode dengan CER paling rendah. Periksa
CER untuk setiap filter pada setiap gambar di tabel terminal. Untuk
menentukan metode terbaik secara keseluruhan pada dataset, hitung rata-rata
CER per filter dari semua gambar yang sama-sama berhasil diproses, lalu pilih
rata-rata terendah. Hindari menyimpulkan metode terbaik hanya dari satu
gambar.

| Filter | CER per gambar ditampilkan skrip | Rata-rata CER tersedia di berkas |
|---|---|---|
| Mean | Ya | Tidak |
| Median | Ya | Tidak |
| Gaussian | Ya | Tidak |
| Sharpen | Ya | Tidak |

Folder saat ini berisi citra input dan hasil filter, bukan catatan angka CER
dari eksekusi. Selain itu, skrip hanya mencetak CER per gambar dan tidak
menghitung rata-rata antar-gambar atau menyimpan tabel metrik. Karena itu,
metode dengan CER terendah secara aktual belum dapat ditetapkan dari berkas
yang tersedia. Jalankan skrip dan bandingkan nilai yang dicetak; jangan
menganggap salah satu filter pasti terbaik tanpa nilai hasil pengujian.

### Deteksi tanda tangan kepala sekolah

Pada ROI tanda tangan, skrip:

1. Menggunakan Otsu thresholding inversi untuk memisahkan goresan gelap dari
   latar.
2. Menerapkan morphological opening lalu closing dengan kernel 3 × 3.
   Opening mengurangi komponen kecil; closing membantu menyambungkan goresan
   atau menutup celah kecil.
3. Menghitung piksel putih dengan `cv2.countNonZero`.
4. Menetapkan `PRESENT` jika hitungan piksel lebih dari 500, dan `ABSENT`
   jika tidak.

Nilai 500 adalah ambang heuristik yang dapat dipengaruhi ukuran ROI, kualitas
citra, tulisan lain, dan noise. Karena itu, status tersebut sebaiknya
divalidasi dengan gambar berlabel tanda tangan hadir dan tidak hadir.

### Keputusan verifikasi gabungan

Skrip menyatakan nomor valid hanya jika teks OCR sama persis dengan ground
truth dan tanda tangan berstatus `PRESENT`.

| Nomor cocok dengan ground truth | Tanda tangan terdeteksi | Hasil |
|---|---|---|
| Ya | Ya | `TERVERIFIKASI (VALID)` |
| Tidak | Ya | `GAGAL (Nomor Tidak Sesuai)` |
| Ya | Tidak | `GAGAL (TTD Tidak Ditemukan)` |
| Tidak | Tidak | `GAGAL (Nomor Salah & TTD Absen)` |

Hasil verifikasi akhir dicetak untuk setiap gambar dan filter nomor. Deteksi
tanda tangan yang sama digunakan pada keempat baris filter untuk sebuah
gambar.

## Cara Menjalankan

### 1. Persiapan

Pasang Python 3 dan Tesseract OCR. Instal paket Python yang diperlukan:

```bash
python -m pip install opencv-python numpy pytesseract
```

Skrip menetapkan lokasi executable Tesseract pada baris berikut:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

Ubah path tersebut jika Tesseract terpasang di lokasi lain. Pastikan instalasi
Tesseract dapat dijalankan sebelum memproses gambar.

### 2. Jalankan dari folder Tugas07

```bash
cd Tugas07
python verifikasi_file_ijazah.py
```

Letakkan file `.jpg`, `.jpeg`, atau `.png` di `gambar_ijazah/`. Skrip akan
memproses setiap gambar dan menampilkan tabel berisi nama file, filter, hasil
OCR, CER, status tanda tangan, dan hasil verifikasi.

### 3. Periksa hasil

Keluaran gambar disimpan di `hasil_integrasi_proyek_mini/`:

- `*_ttd_crop.png` — ROI tanda tangan setelah CLAHE.
- `*_ttd_morfologi.png` — mask tanda tangan setelah Otsu dan morphology.
- `*_nomor_mean.png`, `*_nomor_median.png`, `*_nomor_gaussian.png`, dan
  `*_nomor_sharpen.png` — ROI nomor hasil masing-masing filter.

Bandingkan nilai CER pada terminal untuk menentukan metode terbaik. Nilai
hasil run tidak disimpan otomatis sebagai CSV.

## Kesimpulan

Sistem menggunakan CLAHE dan empat filter sebagai preprocessing OCR, lalu
membandingkan hasil pengenalan dengan ground truth melalui CER. Sementara
itu, keberadaan tanda tangan diperkirakan dengan Otsu thresholding,
morphological opening/closing, dan ambang hitungan foreground. Filter terbaik
ditentukan dari CER terendah—sebaiknya berdasarkan rata-rata seluruh gambar.
Karena nilai CER aktual tidak tersimpan dalam folder hasil, kesimpulan tentang
filter yang paling efektif harus dibuat setelah menjalankan skrip dan membaca
hasilnya.