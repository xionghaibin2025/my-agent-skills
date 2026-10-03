# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
import pyogrio
from pathlib import Path

BASE = Path(r"E:\2_AI工作区\agent\zcode\project_项目\20261002_161308_全国三级区套地市")
RES = BASE / "5_结果"
VER = BASE / "4_验证"
GPKG = BASE / "2_数据处理" / "中间数据.gpkg"
ALBERS = (BASE / "2_数据处理" / "albers_crs.wkt").read_text(encoding="utf-8")

def albers_area(gdf):
    return gdf.to_crs(ALBERS).geometry.area / 1e6

print("=== gpkg 图层 ===")
layers = pyogrio.list_layers(GPKG)
print([l[0] for l in layers], "共", len(layers), "层")

print("\n=== 结果 shp 要素数/字段/有效性 ===")
for name in ["三级流域_完善版", "三级流域_完善版_融合", "一级流域_完善版", "二级流域_完善版", "全国水资源三级区套地市_标准版"]:
    g = gpd.read_file(RES / f"{name}.shp")
    print(f"{name}: n={len(g)}, crs={g.crs.to_epsg()}, 无效几何={int((~g.is_valid).sum())}, 字段={list(g.columns)}")

print("\n=== 完善版逐面 ===")
g = gpd.read_file(RES / "三级流域_完善版.shp")
print("SRC 计数:", g["SRC"].value_counts().to_dict())
print("CODE 空值:", int(g["CODE"].isna().sum()), "; CODE 唯一数:", g["CODE"].nunique())
print("NAME_OLD 非空:", int(g["NAME_OLD"].notna().sum()))
print("舟山 G020200 面数:", int((g["CODE"]=="G020200").sum()))

print("\n=== 融合版 ===")
gf = gpd.read_file(RES / "三级流域_完善版_融合.shp")
print("n=", len(gf), "CODE 唯一:", gf["CODE"].nunique())
area_f = albers_area(gf)
print(f"完善版融合总面积: {area_f.sum():.1f} km2")

print("\n=== w3c (gpkg层) ===")
w = gpd.read_file(GPKG, layer="w3c")
print("w3c n=", len(w), "WRRCD 唯一:", w["WRRCD"].nunique())
wz = w.dissolve(by="WRRCD")
print("w3c 融合区数:", len(wz))
area_w = albers_area(wz)
print(f"w3c 融合总面积: {area_w.sum():.1f} km2")
diff_pct = abs(area_f.sum()-area_w.sum())/area_w.sum()*100
print(f"相对差: {diff_pct:.3f}%")

print("\n=== 标准版 ===")
s = gpd.read_file(RES / "全国水资源三级区套地市_标准版.shp")
print("n=", len(s), "UNIT13 唯一:", s["UNIT13"].nunique(), "Z3CD 唯一:", s["Z3CD"].nunique(), "CITYCD 唯一:", s["CITYCD"].nunique())
print(f"AREA_K2 字段和: {s['AREA_K2'].sum():.1f}")
area_s = albers_area(s)
print(f"重算 Albers 面积和: {area_s.sum():.1f}")
print(f"AREA_K2 与重算面积最大差: {(s['AREA_K2']-area_s).abs().max():.4f}")
