# -*- coding: utf-8 -*-
"""merge_verify.py — 译文块合并与结构化校验（paper-translate-skill 阶段 8）。

按块号合并 块NN_译文.md 为双语对照 Markdown，注入 front matter，做结构化校验，
输出验收 JSON（分面数据，overall 由本脚本预判、宿主按 acceptance.md 终判）。

译文块格式约定：英文原段为 "> " 引用块，紧接中文译文段落；图片以相对路径
![](...) 插入；公式 $...$ / $$...$$；重建假设处标"待确认"。

用法：
  python merge_verify.py --dir <块目录> --out <双语对照.md> \
      --title "Smith2022_植被韧性全球转变" --doi "10.1038/xxx" \
      --source-pdf <底本PDF路径> [--figures-dir <图片目录>]

输出：
  <out> 双语对照 Markdown（UTF-8）
  <out 同目录>/验收.json

依赖：Python 3.10+，无第三方依赖。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
REFS_HEAD_RE = re.compile(r"^#{0,3}\s*\*?\*?(References|参考文献|Literature\s+Cited)")
PAIR_RATE_MIN = 0.98


def parse_units(text: str):
    """把译文拆成单元序列：('en', block) / ('cn', para) / ('other', line)。"""
    units = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            i += 1
            continue
        if s.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i])
                i += 1
            units.append(("en", "\n".join(block)))
        elif s.startswith(("#", "!", "|", "-")):
            units.append(("other", ln))
            i += 1
        else:
            para = [ln]
            i += 1
            while i < len(lines):
                t = lines[i].strip()
                if not t or t.startswith((">", "#", "!", "|")):
                    break
                para.append(lines[i])
                i += 1
            units.append(("cn", "\n".join(para)))
    return units


def analyze(text: str, md_dir: Path):
    units = parse_units(text)
    en_total = sum(1 for k, _ in units if k == "en")
    cn_total = sum(1 for k, _ in units if k == "cn")
    orphan = 0
    for j, (k, _) in enumerate(units):
        if k != "en":
            continue
        nxt = next((kk for kk, _ in units[j + 1:] if kk in ("en", "cn")), None)
        if nxt != "cn":
            orphan += 1

    links, broken = [], []
    for m in IMG_RE.finditer(text):
        target = m.group(1).split("#")[0]
        if re.match(r"^[a-z]+://", target):
            continue
        p = (md_dir / target).resolve()
        (links if p.exists() else broken).append(target)

    refs_section = None
    ref_count = None
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if REFS_HEAD_RE.match(ln.strip()):
            refs_section = "\n".join(lines[i + 1:])
            break
    if refs_section is not None:
        ref_count = sum(1 for l in refs_section.splitlines()
                        if re.match(r"^\s*(?:\[\d+\]|\d{1,3}\.\s|[A-ZÁÉÍÓÚÑ].*\(\d{4}\))", l))

    pair_rate = (en_total - orphan) / en_total if en_total else 1.0
    return {
        "en_blocks": en_total, "cn_paragraphs": cn_total, "orphan_en": orphan,
        "pairing_rate": round(pair_rate, 4),
        "image_links": len(links), "broken_links": broken,
        "formulas_display": text.count("$$") // 2, "formulas_inline": len(re.findall(r"(?<!\$)\$(?!\$)[^$\n]+(?<!\$)\$(?!\$)", text)),
        "pending_confirm": text.count("待确认"),
        "refs_count_estimated": ref_count,
        "has_refs_section": refs_section is not None,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="译文块合并与校验")
    ap.add_argument("--dir", required=True, help="译文块目录")
    ap.add_argument("--out", required=True, help="合并输出 md 路径")
    ap.add_argument("--title", required=True)
    ap.add_argument("--doi", default="")
    ap.add_argument("--source-pdf", default="")
    ap.add_argument("--mode", choices=["bilingual", "zh"], default="bilingual")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    src = Path(args.dir)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    src_blocks = sorted(src.glob("块*_原文.md"),
                        key=lambda p: int(re.search(r"块(\d+)_", p.name).group(1)))
    tr_blocks = {int(re.search(r"块(\d+)_", p.name).group(1)): p
                 for p in src.glob("块*_译文.md")}
    nums = [int(re.search(r"块(\d+)_", p.name).group(1)) for p in src_blocks]
    missing = [n for n in nums if n not in tr_blocks]
    extra = sorted(set(tr_blocks) - set(nums))
    if missing or extra:
        print(f"块配对错误：缺译文块 {missing}；多余译文块 {extra}")
        sys.exit(2)

    parts = [f"# {args.title}\n\n"
             f"<!-- 底本: {args.source_pdf or '未提供'} | DOI: {args.doi or '未探测'} "
             f"| 生成: {dt.date.today().isoformat()} | 模式: {args.mode} "
             f"| 工具: paper-translate-skill -->\n"]
    for n in nums:
        parts.append(tr_blocks[n].read_text(encoding="utf-8-sig").strip())
    text = "\n\n".join(parts) + "\n"
    out.write_text(text, encoding="utf-8")

    a = analyze(text, out.parent)
    if a["broken_links"] or a["pairing_rate"] < PAIR_RATE_MIN:
        overall = "需修复"
    elif a["pending_confirm"] > 0 or not a["has_refs_section"]:
        overall = "degraded"
    else:
        overall = "complete"

    verdict = {
        "file": str(out), "title": args.title, "doi": args.doi,
        "source_pdf": args.source_pdf, "mode": args.mode,
        "chunks_total": len(nums), "overall_pre": overall,
        "coverage": {"pairing_rate": a["pairing_rate"], "en_blocks": a["en_blocks"],
                     "cn_paragraphs": a["cn_paragraphs"], "orphan_en": a["orphan_en"]},
        "figure": {"image_links": a["image_links"], "broken_links": a["broken_links"],
                   "note": "对照验收记录见 图片/渲染报告.json 的 checked 字段"},
        "formula": {"display": a["formulas_display"], "inline": a["formulas_inline"],
                    "pending_confirm": a["pending_confirm"]},
        "refs": {"count_estimated": a["refs_count_estimated"],
                 "has_section": a["has_refs_section"]},
        "asset": None, "output": None,
        "note": "asset/output 分面由宿主按 acceptance.md 回填；overall_pre 仅为脚本预判",
    }
    report_path = out.parent / "验收.json"
    report_path.write_text(json.dumps(verdict, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    print(f"merged={out.name} chunks={len(nums)}")
    print(f"pairing_rate={a['pairing_rate']} orphan={a['orphan_en']} "
          f"broken_links={len(a['broken_links'])}")
    print(f"formulas(display/inline/pending)={a['formulas_display']}/{a['formulas_inline']}/{a['pending_confirm']} "
          f"refs~{a['refs_count_estimated']}")
    print(f"overall_pre={overall} report={report_path}")


if __name__ == "__main__":
    main()
