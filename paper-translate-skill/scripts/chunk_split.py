# -*- coding: utf-8 -*-
"""chunk_split.py — 翻译分块（paper-translate-skill 阶段 6）。

把清理后的全文按段落边界切成 ~6000 字符的原文块，供宿主逐块翻译。
宿主翻译时写同号译文块 块NN_译文.md（英文引用块 + 中文），再交 merge_verify.py 合并。

用法：
  python chunk_split.py --input <全文.txt 或 底本.md> --out <块目录> [--size 6000]

输出：
  <out>/块01_原文.md …    原文块（UTF-8）
  <out>/分块清单.json      每块字符数、段落数、全文覆盖范围

规则：段落 = 空行分隔的文本单元；累计不超过 --size；单个超长段独立成块不截断；
块数与字符总量必须覆盖全文（末块允许极小）。
依赖：Python 3.10+，无第三方依赖。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description="翻译分块")
    ap.add_argument("--input", required=True, help="全文 txt 或 markdown 底本")
    ap.add_argument("--out", required=True, help="块输出目录")
    ap.add_argument("--size", type=int, default=6000, help="每块目标字符数")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    text = Path(args.input).read_text(encoding="utf-8-sig")
    paras = [p.strip() for p in re_split(text) if p.strip()]
    oversized = [len(p) for p in paras if len(p) > 2000]
    if oversized:
        print(f"警告：{len(oversized)} 个段落超过 2000 字符（最长 {max(oversized)}），"
              f"输入很可能未按空行分段（如 get_text 逐页原文直拼）。"
              f"请先按 references/extraction.md 清理段落结构，否则翻译块边界会切在页/段中间。")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    chunks, cur, cur_chars = [], [], 0
    for p in paras:
        if cur and cur_chars + len(p) + 2 > args.size:
            chunks.append(cur)
            cur, cur_chars = [], 0
        cur.append(p)
        cur_chars += len(p) + 2
    if cur:
        chunks.append(cur)

    manifest = []
    offset = 0
    for i, paras_ in enumerate(chunks, start=1):
        body = "\n\n".join(paras_)
        f = out / f"块{i:02d}_原文.md"
        f.write_text(body, encoding="utf-8")
        manifest.append({"chunk": i, "file": f.name, "chars": len(body),
                         "paragraphs": len(paras_),
                         "char_range": [offset, offset + len(body)]})
        offset += len(body)
        print(f"{f.name}  {len(body)} chars  {len(paras_)} paras")

    joined_len = len("\n\n".join("\n\n".join(c) for c in chunks))
    (out / "分块清单.json").write_text(json.dumps(
        {"input": str(Path(args.input)), "size_target": args.size,
         "total_chars": joined_len, "chunks": manifest},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"chunks={len(chunks)} total_chars={joined_len}")


def re_split(text: str):
    """按空行分段；也把只有一个换行的短行组视为同段（PDF 提取文本常见）。"""
    import re
    raw = re.split(r"\n\s*\n", text)
    return raw


if __name__ == "__main__":
    main()
