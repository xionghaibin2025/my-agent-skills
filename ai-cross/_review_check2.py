# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from pathlib import Path

BASE = Path(r"E:\2_AI工作区\agent\zcode\project_项目\20261002_161308_全国三级区套地市")
RES = BASE / "5_结果"
GPKG = BASE / "2_数据处理" / "中间数据.gpkg"
ALBERS = (BASE / "2_数据处理" / "albers_crs.wkt").read_text(encoding="utf-8")

def albers_area(gdf):
    return gdf.to_crs(ALBERS).geometry.area / 1e6

print("=== w3c 层有效性 ===")
w = gpd.read_file(GPKG, layer="w3c")
print("w3c 无效几何数:", int((~w.is_valid).sum()))

print("\n=== w3c_z210 层 ===")
wz = gpd.read_file(GPKG, layer="w3c_z210")
print("n=", len(wz), "无效:", int((~wz.is_valid).sum()), "字段:", list(wz.columns)[:8])
area_w = albers_area(wz)
print(f"w3c_z210 总面积: {area_w.sum():.1f} km2")

gf = gpd.read_file(RES / "三级流域_完善版_融合.shp")
area_f = albers_area(gf).sum()
print(f"完善版融合总面积: {area_f:.1f}; 相对差: {abs(area_f-area_w.sum())/area_w.sum()*100:.3f}%")

print("\n=== 标准版拓扑 ===")
s = gpd.read_file(RES / "全国水资源三级区套地市_标准版.shp")
area_s = albers_area(s)
print(f"逐面和: {area_s.sum():.1f}; AREA_K2 和: {s['AREA_K2'].sum():.1f}")
print(f"AREA_K2 与重算最大差: {(s['AREA_K2']-area_s).abs().max():.4f} km2")
u = s.geometry.union_all()
ua = gpd.GeoSeries([u], crs=s.crs).to_crs(ALBERS).area.iloc[0]/1e6
print(f"并集面积: {ua:.1f}; 逐面和-并集: {area_s.sum()-ua:.2f} km2")

print("\n=== std_units 层对照 ===")
su = gpd.read_file(GPKG, layer="std_units")
print("std_units n=", len(su))
print("与 shp UNIT13 集合一致:", set(su["UNIT13"])==set(s["UNIT13"]))

print("\n=== init_units 层 ===")
iu = gpd.read_file(GPKG, layer="init_units")
print("init_units n=", len(iu), f"面积和: {albers_area(iu).sum():.1f}")
zcol = [c for c in iu.columns if 'Z3' in c.upper() or 'CD' in c.upper()]
print("字段:", list(iu.columns))
