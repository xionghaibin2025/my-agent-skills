# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from pathlib import Path

BASE = Path(r"E:\2_AI工作区\agent\zcode\project_项目\20261002_161308_全国三级区套地市")
RES = BASE / "5_结果"
GPKG = BASE / "2_数据处理" / "中间数据.gpkg"
ALBERS = (BASE / "2_数据处理" / "albers_crs.wkt").read_text(encoding="utf-8")
def aa(g): return g.to_crs(ALBERS).geometry.area/1e6

EXCEL = Path(r"E:\2_AI工作区\agent\zcode\project_项目\只保留最新版文档\5_结果\长江ROWAS复现包_S14\00_公共输入\计算单元与分区\分区编码（PDF2025最新版）.xlsx")
print("Excel 存在:", EXCEL.exists())

s = gpd.read_file(RES / "全国水资源三级区套地市_标准版.shp")
iu = gpd.read_file(GPKG, layer="init_units")

if EXCEL.exists():
    xl = pd.ExcelFile(EXCEL)
    print("工作表:", xl.sheet_names)
    d = xl.parse("三级区套地市代码")
    print("三级区套地市代码 行数:", len(d), "列:", d.columns.tolist())
    print(d.head(3).to_string())
    # 尝试找 13 位码列
    for c in d.columns:
        vals = d[c].astype(str)
        if vals.str.len().eq(13).mean() > 0.9:
            std13 = set(vals)
            print("13位码列:", c, "唯一:", len(std13))
            in_std = s["UNIT13"].isin(std13)
            print("标准版 UNIT13 ∈ Excel:", int(in_std.sum()), "/", len(s))
            missing_in_vec = std13 - set(s["UNIT13"])
            print("Excel 有而矢量无:", len(missing_in_vec), sorted(missing_in_vec))
            break
    ce = xl.parse("单元编码")
    print("单元编码 行数:", len(ce), "列:", ce.columns.tolist()[:8])

# 市码归并模拟：4690xx -> 469000
pre = iu.copy()
pre["CITYCD2"] = pre["CITYCD"].astype(str).where(~pre["CITYCD"].astype(str).str.match(r"4690(0[1-9]|[12][0-9]|30)"), "469000")
pre["U2"] = pre["Z3CD"].astype(str) + pre["CITYCD2"]
print("\n归并后唯一单元数:", pre["U2"].nunique(), "(报告称 1440)")
ledong = pre[pre["CITYCD"].astype(str)=="469027"]
print("乐东(469027) 归并前行数:", len(ledong))
if len(ledong):
    print(ledong[["UNIT13","Z3NAME","CITYNM","a_km2"]].to_string(index=False))
    h_area = aa(pre[pre["Z3CD"].astype(str).str.startswith("H")]).sum()
    ld = ledong["a_km2"].sum()
    print(f"乐东合计 {ld:.1f} km2, 占 H 初版 {h_area:.1f} 的 {ld/h_area*100:.2f}%")

# 覆盖 100% 核验
j1f = gpd.read_file(GPKG, layer="j1_fixed")
y1 = gpd.read_file(RES / "一级流域_完善版.shp")
print("\nj1_fixed n=", len(j1f), "一级完善版 n=", len(y1))
inter = gpd.overlay(j1f, y1, how="intersection")
cov = aa(inter).sum()/aa(j1f).sum()*100
print(f"原一级被完善版一级覆盖: {cov:.2f}%")
j2f = gpd.read_file(GPKG, layer="j2_fixed")
y2 = gpd.read_file(RES / "二级流域_完善版.shp")
inter2 = gpd.overlay(j2f, y2, how="intersection")
cov2 = aa(inter2).sum()/aa(j2f).sum()*100
print(f"j2_fixed n={len(j2f)}, 原二级被完善版二级覆盖: {cov2:.2f}%")

# 基底 362 原面未改动核验
b3 = gpd.read_file(GPKG, layer="base3_fixed")
w = gpd.read_file(RES / "三级流域_完善版.shp")
orig = w[w["SRC"]=="基底原面"].reset_index(drop=True)
b3s = b3.reset_index(drop=True)
same = orig.geometry.geom_equals_exact(b3s.geometry, tolerance=1e-9)
print("\n基底原面与 base3_fixed 几何逐一相同:", bool(same.all()), "不同数:", int((~same).sum()))
