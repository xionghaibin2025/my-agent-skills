# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow>=10.0", "numpy>=1.24"]
# ///
"""Show a figure as seen with deuteranopia, protanopia, and in grayscale.

Uses the Machado et al. (2009) full-severity matrices applied in linear RGB.
The result is a screening view, not an accessibility certification.

Usage:
    uv run cvd_preview.py compare.png -o compare_cvd.png
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from contact_sheet import flatten, load_font  # noqa: E402

MACHADO = {
    "绿色盲模拟": np.array([[0.367322, 0.860646, -0.227968],
                        [0.280085, 0.672501, 0.047413],
                        [-0.011820, 0.042940, 0.968881]]),
    "红色盲模拟": np.array([[0.152286, 1.052583, -0.204868],
                        [0.114503, 0.786281, 0.099216],
                        [-0.003882, -0.048116, 1.051998]]),
}


def to_linear(c: np.ndarray) -> np.ndarray:
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def to_srgb(c: np.ndarray) -> np.ndarray:
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def simulate(img: Image.Image, matrix: np.ndarray) -> Image.Image:
    lin = to_linear(np.asarray(img, dtype=float) / 255)
    out = to_srgb(lin @ matrix.T)
    return Image.fromarray((out * 255 + 0.5).astype(np.uint8))


def grayscale(img: Image.Image) -> Image.Image:
    lin = to_linear(np.asarray(img, dtype=float) / 255)
    y = to_srgb(lin @ np.array([0.2126, 0.7152, 0.0722]))
    return Image.fromarray((y * 255 + 0.5).astype(np.uint8)).convert("RGB")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    if not args.image.exists():
        print(f"图片不存在：{args.image}", file=sys.stderr)
        return 2

    img = flatten(Image.open(args.image))
    views = [("原图", img)] + [(k, simulate(img, m)) for k, m in MACHADO.items()] + [("灰度", grayscale(img))]
    w, h = img.size
    font_px = max(18, w // 30)
    font = load_font(font_px)
    label_h, gap = int(font_px * 1.8), 30
    sheet = Image.new("RGB", (2 * w + 3 * gap, 2 * (h + label_h) + 3 * gap), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (label, view) in enumerate(views):
        x = gap + (i % 2) * (w + gap)
        y = gap + (i // 2) * (h + label_h + gap)
        draw.text((x, y), label, fill="black", font=font)
        sheet.paste(view, (x, y + label_h))

    out = args.output or args.image.with_name(args.image.stem + "_cvd.png")
    sheet.save(out)
    print(f"{out}  {sheet.width}×{sheet.height}px")
    return 0


if __name__ == "__main__":
    sys.exit(main())
