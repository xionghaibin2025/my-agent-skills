# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow>=10.0"]
# ///
"""Tile candidate figures into one labelled comparison sheet.

Images are placed at their original pixel size so that candidates rendered at
the same final size and dpi keep their true relative size. Use --width only to
bring screenshots of an existing figure to the width of a new render.

Usage:
    uv run contact_sheet.py cand_A.png cand_B.png cand_C.png \
        --labels "A 箱线+点" "B 对数轴" "C 云雨图" --cols 3 -o compare.png
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
]


def load_font(size: int) -> ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def flatten(img: Image.Image) -> Image.Image:
    if img.mode in ("RGBA", "LA") or "transparency" in img.info:
        bg = Image.new("RGB", img.size, "white")
        bg.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[-1])
        return bg
    return img.convert("RGB")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("images", nargs="+", type=Path)
    ap.add_argument("--labels", nargs="+", help="one label per image (default: file names)")
    ap.add_argument("--cols", type=int, default=0, help="columns (default: up to 3)")
    ap.add_argument("--width", type=int, default=0, help="resize every image to this pixel width")
    ap.add_argument("--gap", type=int, default=40)
    ap.add_argument("--font-size", type=int, default=0, help="label size in px (default: scaled to images)")
    ap.add_argument("-o", "--output", type=Path, default=Path("compare.png"))
    args = ap.parse_args()

    labels = args.labels or [p.stem for p in args.images]
    if len(labels) != len(args.images):
        print("标签数量须与图片数量相同", file=sys.stderr)
        return 2
    missing = [str(p) for p in args.images if not p.exists()]
    if missing:
        print(f"图片不存在：{missing}", file=sys.stderr)
        return 2

    imgs = [flatten(Image.open(p)) for p in args.images]
    if args.width:
        imgs = [im.resize((args.width, round(im.height * args.width / im.width)), Image.LANCZOS) for im in imgs]

    cols = args.cols or min(3, len(imgs))
    rows = -(-len(imgs) // cols)
    cell_w = max(im.width for im in imgs)
    font_px = args.font_size or max(18, cell_w // 28)
    font = load_font(font_px)
    label_h = int(font_px * 1.8)
    row_h = [
        label_h + max(im.height for im in imgs[r * cols:(r + 1) * cols])
        for r in range(rows)
    ]
    gap = args.gap
    sheet = Image.new("RGB", (cols * cell_w + (cols + 1) * gap, sum(row_h) + (rows + 1) * gap), "white")
    draw = ImageDraw.Draw(sheet)

    y = gap
    for r in range(rows):
        x = gap
        for c in range(cols):
            i = r * cols + c
            if i >= len(imgs):
                break
            im = imgs[i]
            draw.text((x, y), labels[i], fill="black", font=font)
            sheet.paste(im, (x, y + label_h))
            draw.rectangle([x - 1, y + label_h - 1, x + im.width, y + label_h + im.height], outline="#BBBBBB")
            x += cell_w + gap
        y += row_h[r] + gap

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(f"{args.output}  {sheet.width}×{sheet.height}px，{len(imgs)} 个候选")
    return 0


if __name__ == "__main__":
    sys.exit(main())
