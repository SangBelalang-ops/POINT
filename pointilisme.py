"""
Pointilisme: Foto 1 (sumber titik) membentuk gambar Foto 2 (target bentuk)
Cara pakai:
  1. pip install pillow numpy
  2. Ganti SOURCE_IMG dan TARGET_IMG dengan path foto kamu
  3. python pointilisme.py
"""

from PIL import Image, ImageDraw
import numpy as np

# ── KONFIGURASI ──────────────────────────────────────────────
SOURCE_IMG  = "foto1.jpg"   # foto yang diperkecil jadi titik-titik
TARGET_IMG  = "foto2.jpg"   # foto yang membentuk gambar akhir
OUTPUT_IMG  = "hasil_pointilis.jpg"

DOT_SIZE    = 12    # ukuran setiap "titik" (px). Makin kecil = makin detail
SPACING     = 14    # jarak antar titik (px). Sebaiknya >= DOT_SIZE
OUTPUT_W    = 1200  # lebar output final (px)
# ─────────────────────────────────────────────────────────────


def load_and_resize(path, width):
    img = Image.open(path).convert("RGB")
    ratio = width / img.width
    height = int(img.height * ratio)
    return img.resize((width, height), Image.LANCZOS)


def get_pixel_color(img_array, x, y):
    """Ambil warna pixel dari array numpy dengan boundary check."""
    h, w = img_array.shape[:2]
    x = max(0, min(x, w - 1))
    y = max(0, min(y, h - 1))
    return tuple(img_array[y, x])


def pointilisme(source_path, target_path, output_path,
                dot_size=12, spacing=14, output_width=1200):

    print("Memuat gambar...")
    target = load_and_resize(target_path, output_width)
    tw, th = target.size

    # Source diresize ke ukuran yang sama
    source = load_and_resize(source_path, output_width)
    source = source.resize((tw, th), Image.LANCZOS)

    target_arr = np.array(target)
    source_arr = np.array(source)

    # Canvas putih
    canvas = Image.new("RGB", (tw, th), (255, 255, 255))
    draw   = ImageDraw.Draw(canvas)

    radius = dot_size // 2
    total  = (tw // spacing) * (th // spacing)
    count  = 0

    print(f"Membuat {total} titik pointilis...")

    for y in range(0, th, spacing):
        for x in range(0, tw, spacing):
            # Warna bentuk diambil dari TARGET (foto 2)
            tr, tg, tb = get_pixel_color(target_arr, x, y)

            # Hanya gambar titik di area yang tidak terlalu terang
            # (skip background putih/terang dari target)
            brightness = (tr + tg + tb) / 3
            if brightness > 230:
                continue

            # Warna titik diambil dari SOURCE (foto 1) — ini efek pointilisnya
            sr, sg, sb = get_pixel_color(source_arr, x, y)

            # Ukuran titik proporsional dengan kegelapan area target
            scale  = 1.0 - (brightness / 255)
            r_draw = max(2, int(radius * scale * 1.5))

            draw.ellipse(
                [x - r_draw, y - r_draw, x + r_draw, y + r_draw],
                fill=(sr, sg, sb)
            )

            count += 1

    print(f"Selesai! {count} titik digambar.")
    canvas.save(output_path, quality=95)
    print(f"Hasil disimpan: {output_path}")


if __name__ == "__main__":
    pointilisme(
        source_path  = SOURCE_IMG,
        target_path  = TARGET_IMG,
        output_path  = OUTPUT_IMG,
        dot_size     = DOT_SIZE,
        spacing      = SPACING,
        output_width = OUTPUT_W,
    )
