
import cv2
import numpy as np
import pytesseract
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# KONFIGURASI
BASE = Path(__file__).resolve().parent
INPUT = BASE / "gambar_ijazah"
OUTPUT = BASE / "output_folder"
GROUND_TRUTH = "571012022000056"

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
CONFIG = "--psm 7 -c tessedit_char_whitelist=0123456789"

for folder in ["enhancement", "histogram", "perbandingan"]:
    (OUTPUT / folder).mkdir(parents=True, exist_ok=True)


# IMAGE ENHANCEMENT
def enhancement(gray):
    mn, mx = int(gray.min()), int(gray.max())

    contrast = (
        np.clip((gray.astype(float) - mn) * 255 / (mx - mn), 0, 255).astype(np.uint8)
        if mx != mn else gray.copy()
    )

    return {
        "Brightness": cv2.convertScaleAbs(gray, beta=50),
        "Contrast": contrast,
        "Histogram": cv2.equalizeHist(gray)
    }


# CER
def hitung_cer(benar, hasil):
    dp = list(range(len(hasil) + 1))

    for i, a in enumerate(benar, 1):
        baru = [i]
        for j, b in enumerate(hasil, 1):
            baru.append(min(
                dp[j] + 1,
                baru[j - 1] + 1,
                dp[j - 1] + (a != b)
            ))
        dp = baru

    return dp[-1] / len(benar) * 100 if benar else 0


# PROSES CITRA, OCR, DAN HISTOGRAM
def proses(path):
    img = cv2.imread(str(path))
    if img is None:
        return [], None

    h, w = img.shape[:2]
    roi = img[int(.887*h):int(.988*h), int(.157*w):int(.314*w)]
    if roi.size == 0:
        return [], None

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    metode = {"Tanpa Enhancement": gray, **enhancement(gray)}
    laporan = []

    fig, axes = plt.subplots(4, 2, figsize=(11, 12))

    for i, (nama, citra) in enumerate(metode.items()):
        teks = pytesseract.image_to_string(citra, config=CONFIG)
        teks = "".join(c for c in teks if c.isdigit())
        cer = round(hitung_cer(GROUND_TRUTH, teks), 2)

        laporan.append({
            "Nama Gambar": path.name,
            "Metode": nama,
            "Hasil OCR": teks or "(kosong)",
            "CER (%)": cer
        })

        axes[i, 0].imshow(citra, cmap="gray")
        axes[i, 0].set_title(nama)
        axes[i, 0].axis("off")

        axes[i, 1].hist(citra.ravel(), bins=256, range=(0, 256))
        axes[i, 1].set_title("Histogram " + nama)
        axes[i, 1].set_xlim(0, 255)

        if nama != "Tanpa Enhancement":
            cv2.imwrite(
                str(OUTPUT / "enhancement" / f"{path.stem}_{nama}.png"),
                citra
            )

        # Histogram tersimpan terpisah
        plt.figure(figsize=(7, 3))
        plt.hist(citra.ravel(), bins=256, range=(0, 256))
        plt.title(f"{path.name} - {nama}")
        plt.xlabel("Intensitas Piksel")
        plt.ylabel("Frekuensi")
        plt.tight_layout()
        plt.savefig(OUTPUT / "histogram" / f"{path.stem}_{nama}.png")
        plt.close()

    fig.suptitle("Perbandingan Citra dan Histogram: " + path.name)
    fig.tight_layout()
    fig.savefig(OUTPUT / "perbandingan" / f"{path.stem}_perbandingan.png")
    plt.close(fig)

    # Cari metode enhancement terbaik, tanpa baseline
    hasil = [x for x in laporan if x["Metode"] != "Tanpa Enhancement"]
    nilai_min = min(x["CER (%)"] for x in hasil)
    terbaik = ", ".join(x["Metode"] for x in hasil if x["CER (%)"] == nilai_min)

    kesimpulan = {
        "Nama Gambar": path.name,
        "Metode Terbaik": terbaik,
        "CER Terendah (%)": nilai_min
    }
    return laporan, kesimpulan


# MAIN DAN TABEL

# MAIN DAN TABEL
def main():
    if not INPUT.exists():
        print("Folder gambar_ijazah tidak ditemukan.")
        return

    gambar = sorted(
        p for p in INPUT.iterdir()
        if p.suffix.lower() in {
            ".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"
        }
    )

    if not gambar:
        print("Folder gambar_ijazah masih kosong.")
        return

    semua, kesimpulan = [], []

    for p in gambar:
        laporan, hasil = proses(p)
        semua.extend(laporan)

        if hasil:
            kesimpulan.append(hasil)

    # TABEL PERBANDINGAN OCR
    print("\n" + "=" * 100)
    print("PERBANDINGAN HASIL OCR DAN CER")
    print("=" * 100)

    for baris in semua:
        print(
            f"{baris['Nama Gambar']} | "
            f"Metode: {baris['Metode']} | "
            f"Hasil OCR: {baris['Hasil OCR']} | "
            f"CER: {baris['CER (%)']:.2f}%"
        )
        print("-" * 100)

    pd.DataFrame(semua).to_csv(
        OUTPUT / "perbandingan_ketiga_metode.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # TABEL KESIMPULAN
    print("\n" + "=" * 100)
    print("KESIMPULAN METODE ENHANCEMENT TERBAIK")
    print("=" * 100)

    for baris in kesimpulan:
        print(
            f"{baris['Nama Gambar']} | "
            f"Metode Terbaik: {baris['Metode Terbaik']} | "
            f"CER Terendah: {baris['CER Terendah (%)']:.2f}%"
        )
        print("-" * 100)

    pd.DataFrame(kesimpulan).to_csv(
        OUTPUT / "kesimpulan_metode_terbaik.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nSemua hasil tersimpan di:", OUTPUT.resolve())


if __name__ == "__main__":
    main()
