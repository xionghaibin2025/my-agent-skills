# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas>=2.0", "numpy>=1.24", "openpyxl"]
# ///
"""Profile the distribution shape of numeric columns to guide chart choice.

Reports facts (n, skewness, zero share, outliers, bimodality, spread and
scale differences between groups) and the shape flags used in
references/encoding-by-shape.md. It does not run hypothesis tests.

Usage:
    uv run profile_shape.py data.csv --y conc --group site
    uv run profile_shape.py data.xlsx --sheet 1 --y a b --group treat --json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

# Screening thresholds; flags are hints for choosing candidates, not rules.
SMALL_N = 10
VERY_SMALL_N = 5
LARGE_N = 200
SKEW = 1.0
SPAN_ORDERS = 100.0
ZERO_SHARE = 0.20
OUTLIER_SHARE = 0.05
BIMODAL_BC = 0.555
BIMODAL_MIN_N = 20
DISCRETE_LEVELS = 7
DISCRETE_INT_LEVELS = 15
SPREAD_RATIO = 3.0
SCALE_GAP = 10.0
UNEQUAL_N = 3.0
MANY_GROUPS = 8
SHAPE_MIN_N = 8  # skew and outlier flags need at least this many values
POOLED_FLAGS = {"span_orders", "has_negative"}
WITHIN_GROUP_FLAGS = {"right_skew", "left_skew", "bimodal", "many_zeros", "outliers", "discrete"}


def read_table(path: Path, sheet: str | None) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        sheet_arg: str | int = 0 if sheet is None else (int(sheet) if sheet.isdigit() else sheet)
        return pd.read_excel(path, sheet_name=sheet_arg)
    if suffix == ".parquet":
        try:
            return pd.read_parquet(path)
        except ImportError:
            sys.exit("读取 parquet 需要 pyarrow：uv run --with pyarrow profile_shape.py ...")
    if suffix in {".tsv", ".txt"}:
        return pd.read_csv(path, sep="\t")
    return pd.read_csv(path)


def skewness(x: np.ndarray) -> float:
    n = x.size
    if n < 3:
        return math.nan
    sd = x.std(ddof=0)
    if sd == 0:
        return 0.0
    g1 = np.mean((x - x.mean()) ** 3) / sd**3
    return float(g1 * math.sqrt(n * (n - 1)) / (n - 2))


def excess_kurtosis(x: np.ndarray) -> float:
    n = x.size
    if n < 4:
        return math.nan
    sd = x.std(ddof=0)
    if sd == 0:
        return 0.0
    g2 = np.mean((x - x.mean()) ** 4) / sd**4 - 3
    return float(((n + 1) * g2 + 6) * (n - 1) / ((n - 2) * (n - 3)))


def bimodality_coefficient(x: np.ndarray) -> float:
    n = x.size
    g, k = skewness(x), excess_kurtosis(x)
    if math.isnan(g) or math.isnan(k):
        return math.nan
    return float((g**2 + 1) / (k + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))))


def describe(x: np.ndarray) -> dict:
    n = int(x.size)
    if n == 0:
        return {"n": 0}
    q1, med, q3 = np.percentile(x, [25, 50, 75])
    iqr = q3 - q1
    outside = (x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)
    positive = x[x > 0]
    levels = int(np.unique(x).size)
    skew = skewness(x)
    # The bimodality coefficient rises with skewness alone; judge skewed
    # positive data on the log scale so a long tail is not read as two modes.
    bc_basis = np.log(x) if x.min() > 0 and not math.isnan(skew) and skew > SKEW else x
    is_int = bool(np.all(np.equal(np.mod(x, 1), 0)))
    return {
        "n": n,
        "min": float(x.min()),
        "q1": float(q1),
        "median": float(med),
        "q3": float(q3),
        "max": float(x.max()),
        "mean": float(x.mean()),
        "sd": float(x.std(ddof=1)) if n > 1 else math.nan,
        "iqr": float(iqr),
        "skew": skew,
        "bimodality": bimodality_coefficient(bc_basis),
        "zero_share": float(np.mean(x == 0)),
        "negative_share": float(np.mean(x < 0)),
        "outlier_share": float(np.mean(outside)),
        "levels": levels,
        "integer": is_int,
        "positive_span": float(positive.max() / positive.min()) if positive.size else math.nan,
    }


def column_flags(d: dict) -> list[str]:
    flags = []
    if d["n"] > LARGE_N:
        flags.append("large_n")
    if d["n"] >= SHAPE_MIN_N and not math.isnan(d["skew"]):
        if d["skew"] > SKEW:
            flags.append("right_skew")
        elif d["skew"] < -SKEW:
            flags.append("left_skew")
    if not math.isnan(d["positive_span"]) and d["positive_span"] >= SPAN_ORDERS:
        flags.append("span_orders")
    if d["zero_share"] >= ZERO_SHARE:
        flags.append("many_zeros")
    if d["negative_share"] > 0:
        flags.append("has_negative")
    zero_spike = d["zero_share"] >= ZERO_SHARE  # reported as many_zeros instead
    if d["n"] >= BIMODAL_MIN_N and not zero_spike and not math.isnan(d["bimodality"]) and d["bimodality"] > BIMODAL_BC:
        flags.append("bimodal")
    if d["n"] >= SHAPE_MIN_N and d["outlier_share"] > OUTLIER_SHARE:
        flags.append("outliers")
    few_levels = d["levels"] <= DISCRETE_LEVELS or (d["integer"] and d["levels"] <= DISCRETE_INT_LEVELS)
    if few_levels and d["levels"] <= d["n"] / 2:  # repeated values, not just a short sample
        flags.append("discrete")
    return flags


def group_summary(groups: dict[str, dict]) -> tuple[dict, list[str]]:
    stats = {k: v for k, v in groups.items() if v.get("n", 0) > 0}
    flags: list[str] = []
    if not stats:
        return {}, flags
    ns = [v["n"] for v in stats.values()]
    out: dict = {"groups": len(stats), "n_min": min(ns), "n_max": max(ns)}
    if min(ns) < VERY_SMALL_N:
        flags.append("very_small_n")
    if min(ns) < SMALL_N:
        flags.append("small_n")
    if max(ns) > LARGE_N:
        flags.append("large_n")
    if min(ns) > 0 and max(ns) / min(ns) >= UNEQUAL_N:
        flags.append("unequal_n")
    if len(stats) > MANY_GROUPS:
        flags.append("many_groups")
    iqrs = [v["iqr"] for v in stats.values() if v["iqr"] > 0]
    if len(iqrs) >= 2:
        out["iqr_ratio"] = max(iqrs) / min(iqrs)
        if out["iqr_ratio"] >= SPREAD_RATIO:
            flags.append("unequal_spread")
    meds = [abs(v["median"]) for v in stats.values() if v["median"] != 0]
    if len(meds) >= 2:
        out["median_ratio"] = max(meds) / min(meds)
        if out["median_ratio"] >= SCALE_GAP:
            flags.append("scale_gap")
    pairs = list(combinations(stats.values(), 2))
    if pairs:
        overlap = sum(1 for a, b in pairs if a["q1"] <= b["q3"] and b["q1"] <= a["q3"])
        out["iqr_overlap_share"] = overlap / len(pairs)
        if out["iqr_overlap_share"] > 0.5:
            flags.append("high_overlap")
    out["order_by_median"] = sorted(stats, key=lambda k: stats[k]["median"])
    return out, flags


def profile(df: pd.DataFrame, ys: list[str], group: list[str]) -> dict:
    result: dict = {"rows": int(len(df)), "group_by": group, "columns": {}}
    for y in ys:
        values = pd.to_numeric(df[y], errors="coerce")
        missing = int(values.isna().sum())
        finite = values[np.isfinite(values)]
        overall = describe(finite.to_numpy(dtype=float))
        entry: dict = {"missing": missing, "overall": overall}
        flags = column_flags(overall) if overall["n"] else []
        if group:
            keyed = df.assign(_y=values).dropna(subset=["_y"])
            keyed = keyed[np.isfinite(keyed["_y"])]
            groups = {}
            for key, sub in keyed.groupby(group, dropna=False, observed=True):
                label = " / ".join(map(str, key)) if isinstance(key, tuple) else str(key)
                groups[label] = describe(sub["_y"].to_numpy(dtype=float))
            summary, gflags = group_summary(groups)
            entry["groups"] = groups
            entry["between_groups"] = summary
            # Pooling groups creates spurious skew and bimodality, so shape
            # flags come from within-group data only.
            flags = [f for f in flags if f in POOLED_FLAGS]
            for label, g in groups.items():
                if g.get("n", 0):
                    gf = [f for f in column_flags(g) if f in WITHIN_GROUP_FLAGS]
                    g["flags"] = gf
                    flags.extend(gf)
            flags.extend(gflags)
        else:
            if overall.get("n", 0) and overall["n"] < SMALL_N:
                flags.append("very_small_n" if overall["n"] < VERY_SMALL_N else "small_n")
        entry["flags"] = sorted(set(flags))
        result["columns"][y] = entry
    return result


def fmt(v) -> str:
    if isinstance(v, float):
        if math.isnan(v):
            return "—"
        return f"{v:.3g}"
    return str(v)


def to_markdown(res: dict) -> str:
    lines = [f"行数 {res['rows']}；分组 {', '.join(res['group_by']) or '无'}", ""]
    for y, e in res["columns"].items():
        o = e["overall"]
        lines.append(f"## {y}")
        lines.append(f"形状标记：{', '.join(e['flags']) or '无'}")
        lines.append(f"缺失 {e['missing']}；n {o.get('n', 0)}；偏度 {fmt(o.get('skew', math.nan))}；"
                     f"零值 {fmt(o.get('zero_share', math.nan))}；离群 {fmt(o.get('outlier_share', math.nan))}；"
                     f"取值种类 {o.get('levels', 0)}；正值跨度 {fmt(o.get('positive_span', math.nan))} 倍")
        if "groups" in e:
            b = e["between_groups"]
            lines.append(f"组间：{b.get('groups', 0)} 组，n {b.get('n_min')}–{b.get('n_max')}；"
                         f"IQR 比 {fmt(b.get('iqr_ratio', math.nan))}；中位数比 {fmt(b.get('median_ratio', math.nan))}；"
                         f"IQR 重叠组对占比 {fmt(b.get('iqr_overlap_share', math.nan))}")
            lines.append("")
            lines.append("| 组 | n | 中位数 | Q1–Q3 | 最小–最大 | 偏度 | 零值 | 离群 | 组内标记 |")
            lines.append("|---|---|---|---|---|---|---|---|---|")
            for g in b.get("order_by_median", []):
                d = e["groups"][g]
                lines.append(f"| {g} | {d['n']} | {fmt(d['median'])} | {fmt(d['q1'])}–{fmt(d['q3'])} | "
                             f"{fmt(d['min'])}–{fmt(d['max'])} | {fmt(d['skew'])} | {fmt(d['zero_share'])} | {fmt(d['outlier_share'])} | {', '.join(d.get('flags', [])) or '—'} |")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path)
    ap.add_argument("--y", nargs="+", help="numeric columns (default: all numeric columns)")
    ap.add_argument("--group", nargs="+", default=[], help="grouping column(s)")
    ap.add_argument("--sheet", help="Excel sheet name or index")
    ap.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    args = ap.parse_args()

    df = read_table(args.path, args.sheet)
    missing_cols = [c for c in (args.y or []) + args.group if c not in df.columns]
    if missing_cols:
        print(f"列不存在：{missing_cols}；可用列：{list(df.columns)}", file=sys.stderr)
        return 2
    ys = args.y or [c for c in df.select_dtypes("number").columns if c not in args.group]
    res = profile(df, ys, args.group)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2, default=lambda v: None if isinstance(v, float) and math.isnan(v) else v))
    else:
        print(to_markdown(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
