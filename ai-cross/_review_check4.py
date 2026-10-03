# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
BASE = Path(r"E:\2_AI工作区\agent\zcode\project_项目\20261002_161308_全国三级区套地市")
xl = pd.ExcelFile(BASE / "5_结果" / "未入表单元排查.xlsx")

full = xl.parse("全量未入表")
print("全量未入表: 行数", len(full), "面积和", round(full["面积km2"].sum(),1))
print("占一级区比例% max:", full["占一级区比例%"].max(), " min:", full["占一级区比例%"].min())
top = full.nlargest(8, "占一级区比例%")
print(top[["单元编码13位","一级区码","三级区名","地市名","面积km2","占一级区比例%"]].to_string(index=False))
print("含'乐东'行数:", int(full.astype(str).apply(lambda r: r.str.contains("乐东").any(), axis=1).sum()))

print("\n按一级区汇总(与04报告对照):")
g = full.groupby("一级区码").agg(n=("面积km2","size"), a=("面积km2","sum")).reset_index()
print(g.to_string(index=False))
print("未入表总数:", g["n"].sum(), "总面积:", round(g["a"].sum(),1))

print("\n=== 标准有而矢量无 10 行 ===")
print(xl.parse("标准有而矢量无").to_string(index=False))

print("\n=== 市码对照 31 行 ===")
mc = xl.parse("市码对照")
print(mc.to_string(index=False))
