import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
import csv

INPUT = Path("gambar_ijazah")
OUTPUT = Path("output_folder")
EKSTENSI = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

for folder in ["grayscale", "histogram", "enhancement", "perbandingan"]:
    (OUTPUT / folder).mkdir(parents=True, exist_ok=True)


def enhancement(gray):
    mean, std = np.mean(gray), np.std(gray)
    hasil = gray.copy()
    metode = []

    # 4. Median Filter
    noise = np.std(gray.astype(float) -
                   cv2.medianBlur(gray, 3).astype(float))
    if noise > 12:
        hasil = cv2.medianBlur(hasil, 3)
        metode.append("Median Filter")

    # 5. Background Normalization
    latar = cv2.GaussianBlur(hasil, (51, 51), 0)
    if np.std(latar) > 25:
        hasil = np.clip(
            (hasil.astype(float) + 1) /
            (latar.astype(float) + 1) * np.median(latar),
            0, 255
        ).astype(np.uint8)
        metode.append("Background Normalization")

    # 6. Gamma Correction
    gamma = 0.6 if mean < 90 else 1.5 if mean > 180 else 1
    if gamma != 1:
        tabel = np.array([
            (i / 255) ** gamma * 255 for i in range(256)
        ]).astype(np.uint8)
        hasil = cv2.LUT(hasil, tabel)
        metode.append("Gamma Correction")

    # 7. CLAHE
    if std < 45:
        hasil = cv2.createCLAHE(
            clipLimit=2.0, tileGridSize=(8, 8)
        ).apply(hasil)
        metode.append("CLAHE")

    # 8. Contrast Stretching
    elif std < 60:
        hasil = cv2.normalize(
            hasil, None, 0, 255, cv2.NORM_MINMAX
        )
        metode.append("Contrast Stretching")

    return hasil, ", ".join(metode) or "Tidak diperlukan"


def proses(file):
    bgr = cv2.imread(str(file))
    if bgr is None:
        print(f"Gagal membaca {file.name}")
        return None

    # 1. Grayscale Conversion
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    # 2. RGB Histogram dan 3. Grayscale Histogram
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for kanal, warna in enumerate(["red", "green", "blue"]):
        ax[0].plot(
            cv2.calcHist([rgb], [kanal], None, [256], [0, 256]),
            color=warna
        )
    ax[0].set_title("Histogram RGB")
    ax[1].hist(gray.ravel(), bins=256, range=(0, 256))
    ax[1].set_title("Histogram Grayscale")
    fig.tight_layout()
    fig.savefig(OUTPUT / "histogram" / f"{file.stem}_hist.png")
    plt.close(fig)

    hasil, metode = enhancement(gray)

    cv2.imwrite(str(OUTPUT / "grayscale" / f"{file.stem}_gray.png"), gray)
    cv2.imwrite(str(OUTPUT / "enhancement" / f"{file.stem}_enhanced.png"), hasil)

    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    for a, gambar, judul, cmap in zip(
        ax, [rgb, gray, hasil],
        ["Citra Asli", "Grayscale", "Enhancement"],
        [None, "gray", "gray"]
    ):
        a.imshow(gambar, cmap=cmap)
        a.set_title(judul)
        a.axis("off")
    fig.tight_layout()
    fig.savefig(OUTPUT / "perbandingan" / f"{file.stem}_banding.png")
    plt.close(fig)

    print(f"{file.name} | Rata-rata: {np.mean(gray):.2f} | "
          f"Kontras: {np.std(gray):.2f} | Metode: {metode}")

    return {
        "nama_file": file.name,
        "rata_rata_intensitas": round(float(np.mean(gray)), 2),
        "standar_deviasi": round(float(np.std(gray)), 2),
        "metode_enhancement": metode
    }


def main():
    gambar = sorted(
        f for f in INPUT.glob("*")
        if f.is_file() and f.suffix.lower() in EKSTENSI
    )

    if not gambar:
        print("Masukkan gambar ke folder gambar_ijazah.")
        return

    laporan = [hasil for f in gambar if (hasil := proses(f)) is not None]

    if laporan:
        with open(OUTPUT / "hasil_analisis.csv", "w",
                  newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=laporan[0].keys())
            writer.writeheader()
            writer.writerows(laporan)

    print(f"Hasil tersimpan di: {OUTPUT.resolve()}")


if __name__ == "__main__":
    main()
