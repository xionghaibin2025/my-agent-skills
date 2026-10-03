# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from pathlib import Path

BASE = Path(r"E:\2_AI工作区\agent\zcode\project_项目\20261002_161308_全国三级区套地市")
RES = BASE / "5_结果"; VER = BASE / "4_验证"
GPKG = BASE / "2_数据处理" / "中间数据.gpkg"
ALBERS = (BASE / "2_数据处理" / "albers_crs.wkt").read_text(encoding="utf-8")
def aa(gdf): return gdf.to_crs(ALBERS).geometry.area / 1e6

print("=== init_units 03 报告核验 ===")
iu = gpd.read_file(GPKG, layer="init_units")
print("三级区数:", iu["Z3CD"].nunique(), "地市数:", iu["CITYCD"].nunique())

print("\n=== border_bands ===")
bb = gpd.read_file(GPKG, layer="border_bands")
print("n=", len(bb), f"面积和: {aa(bb).sum():.1f}", "字段:", list(bb.columns))

print("\n=== 新增面明细 csv ===")
df = pd.read_csv(VER / "02_新增面明细.csv")
print(df.columns.tolist())
acol = [c for c in df.columns if "积" in c or "km" in c.lower()][0]
print("行数:", len(df), f"面积和: {df[acol].sum():.1f}", "≥100km2 片数:", int((df[acol]>=100).sum()))

print("\n=== 边境差异带明细 csv ===")
df2 = pd.read_csv(VER / "02_边境差异带明细.csv")
print(df2.columns.tolist())
acol2 = [c for c in df2.columns if "积" in c or "km" in c.lower()][0]
print("行数:", len(df2), f"面积和: {df2[acol2].sum():.1f}")

print("\n=== 三级区面积对照 csv ===")
df3 = pd.read_csv(VER / "05_三级区面积对照.csv")
print(df3.columns.tolist())
print("行数:", len(df3))
pcol = [c for c in df3.columns if "偏差" in c or "%" in c][0]
print("偏差>2% 个数:", int((df3[pcol].abs()>2).sum()), f"中位偏差: {df3[pcol].abs().median():.2f}")
mx = df3.loc[df3[pcol].abs().idxmax()]
print("最大偏差行:", mx.tolist())

print("\n=== 未入表单元排查.xlsx ===")
xl = pd.ExcelFile(RES / "未入表单元排查.xlsx")
print("工作表:", xl.sheet_names)
for sn in xl.sheet_names:
    d = xl.parse(sn)
    print(f"--- {sn}: {len(d)} 行; 列: {d.columns.tolist()}")
