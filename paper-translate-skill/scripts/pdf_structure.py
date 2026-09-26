# -*- coding: utf-8 -*-
"""pdf_structure.py — 论文 PDF 结构提取（paper-translate-skill 阶段 3）。

输入一个 PDF，输出：
  <out>/第NN页.txt      逐页全文文本（UTF-8，压缩行尾空白、保留换行）
  <out>/结构.json       页数、字符数、DOI 探测、逐页图注定位（图/ED图/表）、位图盘点、参考文献节估计
  <out>/图片盘点.txt    每页内嵌位图的 xref/尺寸/格式清单（仅作定位参考，不作交付）

用法：
  python pdf_structure.py <PDF> --out <目录>

依赖：Python 3.10+、pymupdf。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pymupdf

CAPTION_RE = re.compile(
    r"^\s*(Extended\s+Data\s+)?(?:Fig(?:ure)?\.?|Figure)\s*(\d+)\b"
)
TABLE_RE = re.compile(r"^\s*Table\s*(\d+)\b")
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>\]\),;]+)")
REFS_HEAD_RE = re.compile(r"^\s*(References|REFERENCES|Literature\s+Cited)\s*$")
REF_ENTRY_RE = re.compile(r"^\s*(?:\[\d+\]|\d{1,3}\.\s)")


def find_captions(page, min_width: float):
    """返回本页 [{kind, num, bbox, text}]，按 y0 升序。kind ∈ {fig, edfig, table}。"""
    out = []
    for b in page.get_text("blocks"):
        text = (b[4] or "").strip()
        if (b[2] - b[0]) <= min_width:
            continue
        m = CAPTION_RE.match(text)
        if m:
            out.append({
                "kind": "edfig" if m.group(1) else "fig",
                "num": int(m.group(2)),
                "bbox": [round(v, 2) for v in b[:4]],
                "text": text[:100],
            })
            continue
        t = TABLE_RE.match(text)
        if t:
            out.append({"kind": "table", "num": int(t.group(1)),
                        "bbox": [round(v, 2) for v in b[:4]], "text": text[:100]})
    out.sort(key=lambda c: c["bbox"][1])
    return out


def guess_doi(doc):
    meta = doc.metadata or {}
    for src in [meta.get("subject", ""), meta.get("keywords", ""), meta.get("title", "")]:
        m = DOI_RE.search(src or "")
        if m:
            return m.group(1).rstrip(".")
    for i in range(min(3, doc.page_count)):
        m = DOI_RE.search(doc[i].get_text("text") or "")
        if m:
            return m.group(1).rstrip(".")
    return None


def refs_estimate(doc):
    """定位参考文献节起始页并按常见条目模式估计条数。估计值仅供核对。"""
    start = None
    for i in range(doc.page_count - 1, max(doc.page_count - 8, -1), -1):
        for line in (doc[i].get_text("text") or "").splitlines():
            if REFS_HEAD_RE.match(line):
                start = i + 1
                break
        if start:
            break
    if start is None:
        return {"start_page": None, "estimated_count": None, "note": "未定位到参考文献节标题"}
    count = 0
    for i in range(start - 1, doc.page_count):
        for line in (doc[i].get_text("text") or "").splitlines():
            if REF_ENTRY_RE.match(line):
                count += 1
    if count == 0:
        return {"start_page": start, "estimated_count": None,
                "note": "未识别到编号条目（可能为作者-年份格式），需人工计数"}
    return {"start_page": start, "estimated_count": count,
            "note": "按条目模式估计，交付前由宿主逐条核对"}


def main() -> None:
    ap = argparse.ArgumentParser(description="论文 PDF 结构提取")
    ap.add_argument("pdf", help="PDF 路径")
    ap.add_argument("--out", required=True, help="输出目录")
    ap.add_argument("--caption-min-width", type=float, default=150.0,
                    help="图注块最小宽度（磅），默认 150")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    pdf = Path(args.pdf)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf)
    structure = {
        "pdf": str(pdf),
        "page_count": doc.page_count,
        "total_chars": 0,
        "doi": guess_doi(doc),
        "metadata": {k: doc.metadata.get(k) for k in ("title", "author", "producer")},
        "pages": [],
        "references": refs_estimate(doc),
        "note": "caption 定位基于文本块，宽度过窄的图注可能漏检；渲染前与正文最大图号核对",
    }
    inv = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text("text") or ""
        text = "\n".join(ln.rstrip() for ln in text.splitlines())
        (out / f"第{i:02d}页.txt").write_text(text, encoding="utf-8")
        structure["total_chars"] += len(text)
        caps = find_captions(page, args.caption_min_width)
        imgs = []
        for im in page.get_images(full=True):
            xref = im[0]
            info = doc.extract_image(xref)
            imgs.append({"xref": xref, "w": info["width"], "h": info["height"],
                         "ext": info["ext"]})
            inv.append(f"page {i:02d}  xref={xref}  {info['width']}x{info['height']}  {info['ext']}")
        structure["pages"].append({"page": i, "chars": len(text),
                                   "captions": caps, "raster_images": imgs})
    doc.close()

    (out / "结构.json").write_text(json.dumps(structure, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
    (out / "图片盘点.txt").write_text("\n".join(inv) if inv else "(no embedded raster images)",
                                      encoding="utf-8")
    figs = [c for p in structure["pages"] for c in p["captions"] if c["kind"] in ("fig", "edfig")]
    print(f"pages={structure['page_count']} total_chars={structure['total_chars']}")
    print(f"doi={structure['doi']}")
    print(f"captions: fig={sum(1 for c in figs if c['kind']=='fig')} "
          f"edfig={sum(1 for c in figs if c['kind']=='edfig')} "
          f"table={sum(1 for p in structure['pages'] for c in p['captions'] if c['kind']=='table')}")
    print(f"references={structure['references']}")


if __name__ == "__main__":
    main()
