
import cv2
import numpy as np
import pytesseract
import os
import re
import glob

# KONFIGURASI
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

INPUT_FOLDER = "gambar_ijazah"
OUTPUT_FOLDER = "filtered_ijazah"
GROUND_TRUTH = "571012022000056"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# CROP DAN GRAYSCALE TANPA ROTASI
def ambil_area_nomor(path):
    img = cv2.imread(path)

    if img is None:
        return None

    h, w = img.shape[:2]

    crop = img[
        int(0.887 * h):int(0.988 * h),
        int(0.157 * w):int(0.314 * w)
    ]

    if crop.size == 0:
        return None

    return cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)



# EMPAT METODE FILTER
def filtering(gray):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

    return {
        "Original": gray,
        "Mean Filter": cv2.blur(gray, (3, 3)),
        "Median Filter": cv2.medianBlur(gray, 3),
        "Gaussian Filter": cv2.GaussianBlur(gray, (3, 3), 0),
        "Sharpening": cv2.filter2D(gray, -1, kernel)
    }


# OCR DAN AKURASI
def evaluasi(citra):
    besar = cv2.resize(citra, None, fx=4, fy=4,
                       interpolation=cv2.INTER_CUBIC)

    _, binary = cv2.threshold(
        besar, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    teks = pytesseract.image_to_string(
        binary,
        config="--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789"
    )
    teks = re.sub(r"\D", "", teks)

    # Hitung karakter yang benar berdasarkan posisi
    benar = sum(
        a == b for a, b in zip(teks, GROUND_TRUTH)
    )
    akurasi = benar / len(GROUND_TRUTH) * 100

    return teks or "(kosong)", benar, akurasi


# PROSES SEMUA GAMBAR
def main():
    gambar = sorted(
        f for pola in ("*.jpg", "*.jpeg", "*.png")
        for f in glob.glob(os.path.join(INPUT_FOLDER, pola))
    )

    if not gambar:
        print(f"Tidak ada gambar di folder {INPUT_FOLDER}")
        return

    semua_hasil = []

    for nomor, path in enumerate(gambar, 1):
        gray = ambil_area_nomor(path)

        if gray is None:
            print(f"Gagal membaca atau crop kosong: {path}")
            continue

        print(f"\nCITRA {nomor}: {os.path.basename(path)}")
        print("-" * 90)
        print(f"{'Metode':<20} | {'Hasil OCR':<20} | {'Karakter Benar':<15} | Akurasi")
        print("-" * 90)

        for nama, citra in filtering(gray).items():
            teks, benar, akurasi = evaluasi(citra)

            # Simpan citra hasil metode
            nama_file = f"{os.path.splitext(os.path.basename(path))[0]}_{nama.replace(' ', '_')}.jpg"
            cv2.imwrite(os.path.join(OUTPUT_FOLDER, nama_file), citra)

            print(f"{nama:<20} | {teks:<20} | {benar}/{len(GROUND_TRUTH):<13} | {akurasi:.2f}%")

            semua_hasil.append({
                "Metode": nama,
                "Akurasi": akurasi
            })

    # RINGKASAN RATA-RATA
    print("\n" + "=" * 65)
    print("RINGKASAN RATA-RATA AKURASI")
    print("=" * 65)
    print(f"{'Metode':<25} | {'Jumlah Citra':<15} | Rata-rata Akurasi")
    print("-" * 65)

    for nama in filtering(np.zeros((3, 3), dtype=np.uint8)):
        nilai = [x["Akurasi"] for x in semua_hasil if x["Metode"] == nama]
        rata = sum(nilai) / len(nilai) if nilai else 0
        print(f"{nama:<25} | {len(nilai):<15} | {rata:.2f}%")

    print("-" * 65)
    print("Hasil citra tersimpan di:", OUTPUT_FOLDER)


if __name__ == "__main__":
    main()
