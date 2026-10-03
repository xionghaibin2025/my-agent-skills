# -*- coding: utf-8 -*-
import geopandas as gpd, shapely
from pathlib import Path
BASE = Path(r"E:\2_AI工作区\agent\zcode\project_项目\20261002_161308_全国三级区套地市")
GPKG = BASE / "2_数据处理" / "中间数据.gpkg"
RES = BASE / "5_结果"
ALBERS = (BASE / "2_数据处理" / "albers_crs.wkt").read_text(encoding="utf-8")
def a_km2(geom_series):
    return gpd.GeoSeries([shapely.union_all(geom_series.to_numpy())], crs="EPSG:4326").to_crs(ALBERS).area.iloc[0]/1e6

j1 = gpd.read_file(GPKG, layer="j1")      # 原始一级 11 面
j2 = gpd.read_file(GPKG, layer="j2")      # 原始二级 206 面
y1 = gpd.read_file(RES / "一级流域_完善版.shp")
y2 = gpd.read_file(RES / "二级流域_完善版.shp")

for ref, ours, tag in [(j1, y1, "一级"), (j2, y2, "二级")]:
    ref_u = shapely.union_all(ref.geometry.to_numpy())
    ours_u = shapely.union_all(ours.geometry.to_numpy())
    inter = ref_u.intersection(ours_u)
    ra = gpd.GeoSeries([ref_u], crs="EPSG:4326").to_crs(ALBERS).area.iloc[0]/1e6
    ia = gpd.GeoSeries([inter], crs="EPSG:4326").to_crs(ALBERS).area.iloc[0]/1e6
    print(f"{tag}: 原层并集 {ra:.1f} km2, 被完善版覆盖 {ia:.1f} km2, 覆盖率 {ia/ra*100:.4f}%")
