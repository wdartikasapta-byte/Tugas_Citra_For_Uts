
import cv2
import numpy as np
import os
import glob

INPUT = "gambar_ijazah"
OUTPUT = "hasil_ttd"
ROI = (0.60, 0.65, 0.90, 0.85)

os.makedirs(OUTPUT, exist_ok=True)


def proses(path):
    img = cv2.imread(path)
    if img is None:
        return

    h, w = img.shape[:2]
    if h > w:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        h, w = img.shape[:2]

    x0, y0, x1, y1 = ROI
    crop = img[int(y0*h):int(y1*h), int(x0*w):int(x1*w)]
    if crop.size == 0:
        print("Crop kosong:", path)
        return

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    # Dua metode thresholding
    _, global_bw = cv2.threshold(
        gray, 127, 255, cv2.THRESH_BINARY_INV
    )
    nilai_otsu, otsu_bw = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    for nama, bw in [("Global", global_bw), ("Otsu", otsu_bw)]:
        # Opening mengurangi noise kecil
        hasil = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)
        # Closing menyambungkan goresan yang terputus
        hasil = cv2.morphologyEx(hasil, cv2.MORPH_CLOSE, kernel)

        foreground = cv2.countNonZero(hasil)
        rasio = foreground / hasil.size

        # Aturan sederhana; perlu disesuaikan dengan data pengujian
        status = "SIGNATURE PRESENT" if 0.004 <= rasio <= 0.25 else "SIGNATURE ABSENT"

        print("-" * 65)
        print(f"Gambar       : {os.path.basename(path)}")
        print(f"Metode       : {nama}")
        print(f"Threshold    : {127 if nama == 'Global' else nilai_otsu:.0f}")
        print(f"Foreground   : {foreground} piksel")
        print(f"Rasio tinta  : {rasio * 100:.2f}%")
        print(f"Hasil        : {status}")

        dasar = os.path.splitext(os.path.basename(path))[0]
        cv2.imwrite(f"{OUTPUT}/{dasar}_{nama}_gray.png", gray)
        cv2.imwrite(f"{OUTPUT}/{dasar}_{nama}_threshold.png", bw)
        cv2.imwrite(f"{OUTPUT}/{dasar}_{nama}_hasil.png", hasil)


def main():
    gambar = sorted(
        f for pola in ("*.jpg", "*.jpeg", "*.png")
        for f in glob.glob(os.path.join(INPUT, pola))
    )

    if not gambar:
        print(f"Tidak ada gambar di folder '{INPUT}'.")
        return

    for path in gambar:
        proses(path)

    print("-" * 65)
    print("Proses selesai. Hasil tersimpan di:", OUTPUT)


if __name__ == "__main__":
    main()
