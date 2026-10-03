# -*- coding: utf-8 -*-
import geopandas as gpd
from pathlib import Path
BASE = Path(r"E:\2_AI工作区\agent\zcode\project_项目\20261002_161308_全国三级区套地市")
GPKG = BASE / "2_数据处理" / "中间数据.gpkg"
RES = BASE / "5_结果"

import pyogrio
for lyr in ["base3","base3_fixed","base3_z210","j1","j1_fixed","j2","j2_fixed","city","coast_like_pieces","diff_pieces_diag"]:
    info = pyogrio.read_info(GPKG, layer=lyr)
    print(lyr, "features:", info["features"], "crs:", info["crs"][:40])

j1 = gpd.read_file(GPKG, layer="j1")
print("\nj1 n=", len(j1), "字段:", list(j1.columns))
if "CODE" in j1.columns:
    print("j1 CODE 值:", sorted(j1["CODE"].astype(str).tolist()))
j1f = gpd.read_file(GPKG, layer="j1_fixed")
print("j1_fixed n=", len(j1f), "字段:", list(j1f.columns))

# 基底原面未改动核验（对齐后）
b3 = gpd.read_file(GPKG, layer="base3")
b3f = gpd.read_file(GPKG, layer="base3_fixed")
w = gpd.read_file(RES / "三级流域_完善版.shp")
orig = w[w["SRC"]=="基底原面"].reset_index(drop=True)
print("\nbase3 n=", len(b3), " base3_fixed n=", len(b3f), " 完善版基底原面 n=", len(orig))
if len(b3f)==len(orig):
    same = orig.geometry.reset_index(drop=True).geom_equals_exact(b3f.geometry.reset_index(drop=True), tolerance=1e-9)
    print("完善版基底原面 == base3_fixed 几何:", bool(same.all()), "不同:", int((~same).sum()))
if len(b3)==len(orig):
    same2 = orig.geometry.reset_index(drop=True).geom_equals_exact(b3.geometry.reset_index(drop=True), tolerance=1e-9)
    print("完善版基底原面 == base3(原始) 几何:", bool(same2.all()), "不同:", int((~same2).sum()))
