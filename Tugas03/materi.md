# Materi Fungsi Penting: Analisis Citra Ijazah

Materi ini merangkum fungsi utama pada `analisis_citra_ijazah.py`. Program
membaca gambar ijazah dari folder `gambar_ijazah`, menganalisis kualitas
citranya, mencoba memperbaiki citra, lalu menyimpan gambar dan laporan di
folder `output_folder`.

## 1. Fungsi `enhancement`

Fungsi ini memilih metode perbaikan berdasarkan statistik citra yang dihitung
sebelumnya. Fungsi menerima citra grayscale (`gray`), rata-rata intensitas
(`mean`), standar deviasi intensitas (`std`), indikator noise (`noise`), dan
variasi pencahayaan antarbagiannya (`uneven`). Hasilnya adalah citra yang telah
diproses dan teks nama metode yang digunakan.

```python
def enhancement(gray, mean, std, noise, uneven):
    metode = []

    if noise > 12:
        gray = cv2.medianBlur(gray, 3)
        metode.append("Median Filter")

    if uneven > 25:
        ukuran = max(31, min(101, min(gray.shape) // 8))
        if ukuran % 2 == 0:
            ukuran += 1

        latar = cv2.GaussianBlur(gray, (ukuran, ukuran), 0)
        hasil = (gray.astype(float) + 1) / (latar.astype(float) + 1)
        gray = np.clip(hasil * np.median(latar), 0, 255).astype(np.uint8)
        metode.append("Background Normalization")

    if mean < 90:
        tabel = np.array([((i / 255) ** 0.6) * 255
                          for i in range(256)]).astype(np.uint8)
        gray = cv2.LUT(gray, tabel)
        metode.append("Gamma Correction")

    elif mean > 180:
        tabel = np.array([((i / 255) ** 1.5) * 255
                          for i in range(256)]).astype(np.uint8)
        gray = cv2.LUT(gray, tabel)
        metode.append("Gamma Correction")

    if std < 45 or uneven > 25:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        metode.append("CLAHE")

    elif std < 60:
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        metode.append("Contrast Stretching")

    return gray, " + ".join(metode) if metode else "Tidak ada enhancement tambahan"
```

### Konsep pada fungsi

- **Median Filter** (`cv2.medianBlur`) membantu mengurangi noise dengan
  mengganti nilai piksel berdasarkan median di lingkungan berukuran `3 × 3`.
- **Background Normalization** memperkirakan latar menggunakan Gaussian Blur,
  lalu menormalkan citra terhadap perkiraan latar. Metode ini dipilih jika
  variasi pencahayaan (`uneven`) lebih dari `25`.
- **Gamma Correction** mengubah pemetaan intensitas. Untuk citra gelap
  (`mean < 90`) dipakai pangkat `0.6` agar citra lebih terang; untuk citra
  terang (`mean > 180`) dipakai pangkat `1.5` agar citra lebih gelap.
- **CLAHE** meningkatkan kontras secara lokal. Metode ini dipakai ketika
  `std < 45` atau pencahayaan tidak merata.
- **Contrast Stretching** menormalkan rentang intensitas ke `0–255`; dipakai
  bila CLAHE tidak dipilih dan `std < 60`.

Urutan pemeriksaan penting: pengurangan noise dilakukan lebih dulu, kemudian
normalisasi latar, koreksi gamma, dan peningkatan kontras. Ambang tersebut
merupakan aturan praktis yang ditetapkan dalam skrip, bukan batas universal
untuk semua jenis gambar.

## 2. Fungsi `proses_citra`

Fungsi ini memproses satu file gambar. Ia membaca file, membuat representasi
RGB dan grayscale, menghitung statistik, menentukan masalah, menjalankan
enhancement, menyimpan hasil visualisasi, lalu mengembalikan data untuk laporan
CSV.

```python
def proses_citra(file):
    bgr = cv2.imread(str(file))
    if bgr is None:
        print(f"Gagal membaca {file.name}")
        return None

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    # Statistik intensitas
    mean = float(np.mean(gray))
    std = float(np.std(gray))

    # Variasi rata-rata pencahayaan pada beberapa bagian
    area_mean = [
        np.mean(area)
        for row in np.array_split(gray, min(4, gray.shape[0]), axis=0)
        for area in np.array_split(row, min(4, gray.shape[1]), axis=1)
    ]
    uneven = float(np.std(area_mean))

    # Indikator kasar noise
    median = cv2.medianBlur(gray, 3)
    noise = float(np.std(gray.astype(float) - median.astype(float)))

    masalah = []
    if mean < 90:
        masalah.append("Terlalu gelap")
    elif mean > 180:
        masalah.append("Terlalu terang")
    if std < 45:
        masalah.append("Kontras rendah")
    if uneven > 25:
        masalah.append("Kemungkinan pencahayaan tidak merata")
    if noise > 12:
        masalah.append("Indikasi noise")
    if not masalah:
        masalah.append("Tidak ada masalah utama berdasarkan ambang awal")

    hasil, metode = enhancement(gray.copy(), mean, std, noise, uneven)
    nama = file.stem

    # Simpan grayscale dan enhancement
    cv2.imwrite(str(OUTPUT_FOLDER / "grayscale" / f"{nama}_gray.png"), gray)
    cv2.imwrite(str(OUTPUT_FOLDER / "enhancement" / f"{nama}_enhanced.png"), hasil)

    # Histogram RGB dan grayscale
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    for kanal, warna in enumerate(["red", "green", "blue"]):
        hist = cv2.calcHist([rgb], [kanal], None, [256], [0, 256])
        ax[0].plot(hist, color=warna, label=warna.upper())

    ax[0].set_title("Histogram RGB")
    ax[0].set_xlabel("Intensitas")
    ax[0].set_ylabel("Frekuensi")
    ax[0].legend()

    ax[1].hist(gray.ravel(), bins=256, range=(0, 256))
    ax[1].set_title("Histogram Grayscale")
    ax[1].set_xlabel("Intensitas")
    ax[1].set_ylabel("Frekuensi")

    fig.tight_layout()
    fig.savefig(OUTPUT_FOLDER / "histogram" / f"{nama}_histogram.png")
    plt.close(fig)

    # Perbandingan gambar
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    ax[0].imshow(rgb)
    ax[0].set_title("Citra Asli RGB")
    ax[1].imshow(gray, cmap="gray", vmin=0, vmax=255)
    ax[1].set_title("Grayscale")
    ax[2].imshow(hasil, cmap="gray", vmin=0, vmax=255)
    ax[2].set_title("Enhancement")

    for a in ax:
        a.axis("off")

    fig.tight_layout()
    fig.savefig(OUTPUT_FOLDER / "perbandingan" / f"{nama}_perbandingan.png")
    plt.close(fig)

    print(f"\nCitra: {file.name}")
    print(f"Rata-rata intensitas: {mean:.2f}")
    print(f"Standar deviasi: {std:.2f}")
    print(f"Masalah: {', '.join(masalah)}")
    print(f"Enhancement: {metode}")

    return {
        "nama_file": file.name,
        "rata_rata_intensitas": round(mean, 2),
        "standar_deviasi": round(std, 2),
        "variasi_pencahayaan": round(uneven, 2),
        "indikasi_noise": round(noise, 2),
        "masalah": "; ".join(masalah),
        "metode_enhancement": metode
    }
```

### Cara membaca analisisnya

1. `cv2.imread` membaca gambar dalam format BGR. Kode mengubahnya menjadi RGB
   untuk visualisasi Matplotlib, lalu menjadi grayscale untuk analisis
   intensitas.
2. `mean` adalah rata-rata intensitas piksel. Dalam skrip ini, nilai di bawah
   `90` dianggap terlalu gelap dan nilai di atas `180` dianggap terlalu terang.
3. `std` adalah standar deviasi intensitas seluruh piksel; nilai di bawah `45`
   ditandai sebagai kontras rendah.
4. `uneven` adalah standar deviasi rata-rata intensitas dari sejumlah bagian
   citra (maksimal empat baris dan empat kolom bagian). Nilai di atas `25`
   menjadi indikasi pencahayaan tidak merata.
5. `noise` dihitung sebagai standar deviasi selisih antara citra asli dan hasil
   Median Filter `3 × 3`. Nilai di atas `12` ditandai sebagai indikasi noise.
   Ini indikator sederhana, bukan pengukuran noise yang sempurna.
6. `enhancement(gray.copy(), ...)` menerima salinan grayscale agar proses
   perbaikan tidak mengubah variabel `gray` yang dipakai untuk disimpan dan
   dibandingkan.
7. Histogram menggambarkan frekuensi intensitas; gambar perbandingan
   menampilkan citra asli, grayscale, dan hasil enhancement.
8. Dictionary yang dikembalikan menjadi satu baris data laporan CSV.

## 3. Fungsi `main`

Fungsi utama menyiapkan daftar gambar yang didukung, memproses satu per satu,
dan menulis ringkasan hasil ke `hasil_analisis.csv`.

```python
def main():
    if not FOLDER_CITRA.exists():
        print(f"Folder tidak ditemukan: {FOLDER_CITRA}")
        return

    gambar = sorted([
        f for f in FOLDER_CITRA.iterdir()
        if f.is_file() and f.suffix.lower() in EKSTENSI
    ])

    if not gambar:
        print("Masukkan gambar ijazah ke folder gambar_ijazah.")
        return

    laporan = []
    for file in gambar:
        try:
            hasil = proses_citra(file)
            if hasil:
                laporan.append(hasil)
        except Exception as e:
            print(f"Error pada {file.name}: {e}")

    if laporan:
        with open(OUTPUT_FOLDER / "hasil_analisis.csv",
                  "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=laporan[0].keys())
            writer.writeheader()
            writer.writerows(laporan)

    print(f"\nSelesai. Hasil tersimpan di: {OUTPUT_FOLDER.resolve()}")


if __name__ == "__main__":
    main()
```

`EKSTENSI` pada skrip membatasi masukan ke format JPG, JPEG, PNG, BMP, TIF,
dan TIFF. Pemanggilan `if __name__ == "__main__":` memastikan `main()` berjalan
ketika file Python dijalankan langsung. CSV ditulis dengan encoding
`utf-8-sig`, yang membantu aplikasi spreadsheet mengenali teks UTF-8.

## Ringkasan keluaran

Untuk setiap gambar, program menyimpan:

- hasil grayscale di `output_folder/grayscale/`;
- hasil peningkatan citra di `output_folder/enhancement/`;
- histogram RGB dan grayscale di `output_folder/histogram/`;
- gambar perbandingan di `output_folder/perbandingan/`.

Ringkasan nilai statistik, masalah yang terdeteksi, dan metode enhancement
disimpan dalam `output_folder/hasil_analisis.csv`.