# -*- coding: utf-8 -*-
"""render_figures.py — 论文插图渲染提取（paper-translate-skill 阶段 4）。

交付截图一律用渲染法：图注文本块定位条带 → 300 DPI 渲染 → PIL 去白边。
extract_image 的 xref 位图直出天然拿不全合成图，禁止作为交付路径。

版式自适应六规则（经旧流程 37 张返工图验证，详见 references/figures.md）：
  1. 图注块 = Fig./Figure/Extended Data Fig. + N，块宽 > caption-min-width；
  2. 竖直条带 = 上一图注底部（或页顶装饰下缘）至本图注顶部；
  3. 水平范围 = 条带内位图+矢量（剔除通栏细线/页缘竖线）+非正文小文字包络，外扩 x-pad；
  4. 图注栏旁有正文段落（单栏图）时约束到图注栏 ±12 磅、外扩收窄为 4 磅；
  5. 图注在页顶（跨页版式）时图形取上一页图形包络；
  6. 页顶装饰（页眉线/刊头色带/文本页眉）下缘为条带上界。

用法：
  python render_figures.py <PDF> --out <图片目录> [--figs 1,2,5] [--ed] [--tables]
      [--names '{"1":"Fig01_描述"}'] [--coords 覆盖.json] [--dpi 300]
      [--preview-dpi 150] [--page-top 35] [--page-top-caption 150] [--x-pad 25]
      [--caption-min-width 150]

输出：
  <out>/FigNN.png（或 --names 指定名）     交付截图（去白边）
  <out>/整页/pageNN.png                    涉图页整页渲染（对照验收证据，勿删）
  <out>/渲染报告.json                      每图页码/条带坐标/尺寸/来源，附 checked 待宿主回填

依赖：Python 3.10+、pymupdf、pillow。
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageChops

CAPTION_RE = re.compile(r"^\s*(Extended\s+Data\s+)?(?:Fig(?:ure)?\.?|Figure)\s*(\d+)\b")
TABLE_RE = re.compile(r"^\s*Table\s*(\d+)\b")
TRIM_PAD = 8  # 去白边后保留边距（像素）


def find_captions(page, min_width):
    """返回本页 [(num, y0, y1, x0, x1, kind)]，按 y0 升序。kind ∈ {fig, edfig, table}。"""
    out = []
    for b in page.get_text("blocks"):
        text = (b[4] or "").strip()
        if (b[2] - b[0]) <= min_width:
            continue
        m = CAPTION_RE.match(text)
        kind = None
        num = None
        if m:
            kind = "edfig" if m.group(1) else "fig"
            num = int(m.group(2))
        else:
            t = TABLE_RE.match(text)
            if t:
                kind, num = "table", int(t.group(1))
        if kind:
            out.append((num, b[1], b[3], b[0], b[2], kind))
    out.sort(key=lambda t: t[1])
    return out


def content_bbox(page, y_top, y_bot, x_win, pad):
    """条带 ∩ 水平窗口内 位图+矢量（剔除装饰线）+非正文文字 的水平包络。"""
    xw0, xw1 = x_win
    xs0, xs1 = [], []

    def add(rx0, ry0, rx1, ry1):
        if ry0 >= y_bot or ry1 <= y_top:
            return
        ax0, ax1 = max(rx0, xw0), min(rx1, xw1)
        if ax1 > ax0:
            xs0.append(ax0)
            xs1.append(ax1)

    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            if r.width >= 1 or r.height >= 1:
                add(r.x0, r.y0, r.x1, r.y1)
    for d in page.get_drawings():
        r = d["rect"]
        if r.width > 300 and r.height < 3:      # 题注下通栏分隔线
            continue
        if r.width < 3 and r.height > 500 and (r.x1 < 70 or r.x0 > page.rect.width - 70):
            continue                             # 页缘装饰竖线
        if r.width < 0.5 and r.height < 0.5:
            continue
        add(r.x0, r.y0, r.x1, r.y1)
    for blk in page.get_text("dict")["blocks"]:
        if blk["type"] != 0:
            continue
        bx0, by0, bx1, by1 = blk["bbox"]
        if (bx1 - bx0) > 200 and (by1 - by0) > 40 and len(blk["lines"]) >= 3:
            continue                             # 正文段落状大块
        for line in blk["lines"]:
            for span in line["spans"]:
                add(span["bbox"][0], span["bbox"][1], span["bbox"][2], span["bbox"][3])
    if not xs0:
        return None
    return max(xw0, min(xs0) - pad), min(xw1, max(xs1) + pad)


def graphics_bbox(page):
    """整页 位图+矢量（剔除装饰线）包络。"""
    rects = []
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            if r.width >= 1 or r.height >= 1:
                rects.append(pymupdf.Rect(r))
    for d in page.get_drawings():
        r = d["rect"]
        if r.width > 300 and r.height < 3:
            continue
        if r.width < 3 and r.height > 500 and (r.x1 < 70 or r.x0 > page.rect.width - 70):
            continue
        if r.width < 0.5 and r.height < 0.5:
            continue
        rects.append(r)
    if not rects:
        return None
    out = rects[0]
    for r in rects[1:]:
        out |= r
    return out


def header_rule_bottom(page, page_top):
    """页顶装饰（页眉细线/刊头色带/文本页眉）下缘，无则返回 0。"""
    bot = 0.0
    for d in page.get_drawings():
        r = d["rect"]
        if r.width > 300 and r.y1 < 70 and (r.height < 4 or (r.height > 8 and r.y0 < 32)):
            bot = max(bot, r.y1)
    for blk in page.get_text("dict")["blocks"]:  # 文本页眉（GMD 类版式）
        if blk["type"] != 0:
            continue
        bx0, by0, bx1, by1 = blk["bbox"]
        if by1 < page_top + 25 and by0 < 40 and (bx1 - bx0) > 200:
            bot = max(bot, by1)
    return bot


def has_side_text(page, y_top, y_bot, cap_x0, cap_x1):
    """条带内图注栏之外是否存在正文段落状大块（单栏图判定）。"""
    for blk in page.get_text("dict")["blocks"]:
        if blk["type"] != 0:
            continue
        bx0, by0, bx1, by1 = blk["bbox"]
        if by0 >= y_bot or by1 <= y_top:
            continue
        if (bx1 - bx0) > 200 and (by1 - by0) > 40 and len(blk["lines"]) >= 3:
            if bx0 > cap_x1 - 5 or bx1 < cap_x0 + 5:
                return True
    return False


def margin_rule_edges(page):
    W = page.rect.width
    left, right = 0.0, W
    for d in page.get_drawings():
        r = d["rect"]
        if r.width < 3 and r.height > 500:
            if r.x1 < 70:
                left = max(left, r.x1)
            if r.x0 > W - 70:
                right = min(right, r.x0)
    return left, right


def trim_white(img: Image.Image, tol: int = 12) -> Image.Image:
    diff = ImageChops.difference(img.convert("RGB"), Image.new("RGB", img.size, "white")).convert("L")
    bbox = diff.point(lambda p: 255 if p > tol else 0).getbbox()
    if bbox is None:
        return img
    x0, y0, x1, y1 = bbox
    return img.crop((max(0, x0 - TRIM_PAD), max(0, y0 - TRIM_PAD),
                     min(img.width, x1 + TRIM_PAD), min(img.height, y1 + TRIM_PAD)))


def strip_for_caption(doc, page, caps, idx, opts):
    """计算某图注对应的渲染条带 (clip, page_used, mode)。"""
    num, y0, y1, cx0, cx1, kind = caps[idx]
    if kind == "table":  # 表题注在表上方：条带 = 题注底至下方图形包络底
        top = y1 + 2.0
        gb = graphics_bbox(page)
        if gb is None or gb.y1 <= top:
            return None, page, "table_no_graphics"
        bot = gb.y1 + 6.0
        for nb in page.get_text("blocks"):
            if nb[1] > gb.y1 - 20 and (nb[2] - nb[0]) > 200 and nb[1] > top + 10:
                bot = min(bot, nb[1] - 4)
                break
        xr = content_bbox(page, top, bot, (15.0, page.rect.width - 15), opts.x_pad)
        win = xr or (15.0, page.rect.width - 15)
        return pymupdf.Rect(win[0], top, win[1], bot), page, "table_auto"

    if y0 < opts.page_top_caption and page.number > 0:  # 跨页版式
        prev = doc[page.number - 1]
        gb = graphics_bbox(prev)
        if gb is None:
            return None, page, "crosspage_no_graphics"
        bottom = prev.rect.height - 45
        for b in prev.get_text("blocks"):
            if b[1] > gb.y1 - 20 and (b[2] - b[0]) > 200:
                bottom = b[1] - 4
                break
        ml, mr = margin_rule_edges(prev)
        cy0 = max(opts.page_top, header_rule_bottom(prev, opts.page_top) + 3, gb.y0 - 8, ml + 3)
        cx1 = min(prev.rect.width - 40, mr - 3)
        return pymupdf.Rect(max(15.0, ml + 3), cy0, cx1, bottom), prev, "crosspage_auto"

    top = opts.page_top if idx == 0 else caps[idx - 1][2] + 8.0
    if idx == 0:
        top = max(top, header_rule_bottom(page, opts.page_top) + 3)
    bot = y0 - 2.0
    win_all = (15.0, page.rect.width - 15)
    win_col = (max(15.0, cx0 - 12.0), min(page.rect.width - 15, cx1 + 12.0))
    if has_side_text(page, top, bot, cx0, cx1):
        xr = content_bbox(page, top, bot, win_col, 4.0) or win_col
    else:
        xr = content_bbox(page, top, bot, win_all, opts.x_pad) or win_all
    ml, mr = margin_rule_edges(page)
    xr = (max(xr[0], ml + 3), min(xr[1], mr - 3))
    return pymupdf.Rect(xr[0], top, xr[1], bot), page, "auto"


def main() -> None:
    ap = argparse.ArgumentParser(description="论文插图渲染提取（渲染法）")
    ap.add_argument("pdf")
    ap.add_argument("--out", required=True, help="图片输出目录")
    ap.add_argument("--figs", default="", help="只渲染指定正文图号，如 1,2,5；默认全部")
    ap.add_argument("--ed", action="store_true", help="附带 Extended Data 图")
    ap.add_argument("--tables", action="store_true", help="附带表格截图")
    ap.add_argument("--names", default="", help='JSON：{"1":"Fig01_描述"} 指定输出文件名')
    ap.add_argument("--coords", default="", help="JSON 文件：手工坐标覆盖 {\"3\":{\"page\":7,\"rect\":[x0,y0,x1,y1]}}")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--preview-dpi", type=int, default=150, help="整页对照图 DPI，0 关闭")
    ap.add_argument("--page-top", type=float, default=35.0)
    ap.add_argument("--page-top-caption", type=float, default=150.0)
    ap.add_argument("--x-pad", type=float, default=25.0)
    ap.add_argument("--caption-min-width", type=float, default=150.0)
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    want_figs = {int(x) for x in args.figs.split(",") if x.strip().isdigit()} or None
    names = json.loads(args.names) if args.names else {}
    overrides = json.loads(Path(args.coords).read_text(encoding="utf-8")) if args.coords else {}

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    preview_dir = out / "整页"
    if args.preview_dpi:
        preview_dir.mkdir(exist_ok=True)

    class Opts:
        pass
    opts = Opts()
    opts.page_top, opts.page_top_caption, opts.x_pad = args.page_top, args.page_top_caption, args.x_pad

    doc = pymupdf.open(args.pdf)
    report = {"pdf": str(args.pdf), "dpi": args.dpi, "preview_dpi": args.preview_dpi,
              "overrides": {k: overrides[k] for k in overrides}, "figures": [], "preview_pages": []}
    preview_pages = set()

    def render(page, clip, dpi):
        pix = page.get_pixmap(dpi=dpi, clip=clip)
        return trim_white(Image.open(io.BytesIO(pix.tobytes("png"))))

    for page in doc:
        caps = find_captions(page, args.caption_min_width)
        for idx, cap in enumerate(caps):
            num, _, _, _, _, kind = cap
            key = f"{num}"
            if kind == "edfig" and not args.ed:
                continue
            if kind == "table" and not args.tables:
                continue
            if kind == "fig" and want_figs and num not in want_figs:
                continue

            if kind in ("fig", "edfig") and key in overrides:
                ov = overrides[key]
                src_page = doc[int(ov["page"]) - 1]
                clip = pymupdf.Rect(ov["rect"])
                mode, page_used = "coords_override", src_page
                img = render(src_page, clip, args.dpi)
            else:
                clip, page_used, mode = strip_for_caption(doc, page, caps, idx, opts)
                if clip is None:
                    report["figures"].append({"num": num, "kind": kind, "mode": mode,
                                              "page": page.number + 1, "error": "no strip"})
                    continue
                img = render(page_used, clip, args.dpi)

            prefix = {"fig": "Fig", "edfig": "EDFig", "table": "Tab"}[kind]
            stem = names.get(key) or f"{prefix}{num:02d}"
            path = out / f"{stem}.png"
            img.save(path)
            report["figures"].append({
                "num": num, "kind": kind, "mode": mode, "page": page_used.number + 1,
                "strip_rect": [round(v, 1) for v in clip],
                "file": path.name, "width": img.width, "height": img.height,
                "checked": False, "figure_suspect": False,
            })
            preview_pages.add(page.number + 1)
            preview_pages.add(page_used.number + 1)
            print(f"{path.name}  p{page_used.number + 1}  {mode}  {img.width}x{img.height}")

    if args.preview_dpi:
        for pn in sorted(preview_pages):
            pix = doc[pn - 1].get_pixmap(dpi=args.preview_dpi)
            (preview_dir / f"page{pn:02d}.png").write_bytes(pix.tobytes("png"))
    report["preview_pages"] = sorted(preview_pages)
    doc.close()

    (out / "渲染报告.json").write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                       encoding="utf-8")
    print(f"figures={len(report['figures'])} previews={len(report['preview_pages'])} "
          f"report={out / '渲染报告.json'}")


if __name__ == "__main__":
    main()
