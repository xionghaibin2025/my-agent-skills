# Results（结果）润色规范

> 文中句型只用于识别语步和诊断缺失，不作生成模板；写作时用带内容的具体句替代模板句，见 `de-ai-style.md`。

## 核心原则

> Results以报告发现为主，可以解释统计量或数据模式的直接含义；未经验证的机制、因果推断和文献比较放入Discussion。

## 组织原则

按研究问题与发现组织，分析方法是证据的取得方式，不必各占同等篇幅。决定主张的阴性结果、冲突和敏感性结果随相关发现报告，不能为突出主线隐藏。常规输出可在适当表格或补充材料中完整呈现。

| 组织方式 | 适用场景 |
|----------|----------|
| 按假设顺序 | 最常用，验证多个假设 |
| 从宏观到微观 | 先整体趋势，后细节分析 |
| 时间顺序 | 时间序列研究 |
| 重要性递进 | 突出核心发现 |

## 时态规则

| 内容 | 时态 | 示例 |
|------|------|------|
| 描述实验结果 | **过去时** | "The concentration increased by 20%..." |
| 引用图表 | **现在时** | "Figure 3 shows the distribution..." |
| 引用表格 | **现在时** | "Table 2 summarizes the results..." |

## 写作规范

### ✅ 允许
- 描述数据模式和趋势
- 报告统计显著性
- 指出数据关联
- 比较不同组/条件的差异

### ❌ 移出Results

| 内容 | 示例 | 处理 |
|----------|----------|----------|
| 未经验证的机制 | "This pattern may result from pumping-induced leakage..." | 移至Discussion |
| 情感词 | "Interestingly...", "Surprisingly...", "Remarkably..." | 删除 |
| 因果推断 | "The reason for this is...", "This is because..." | 移至Discussion |
| 机制推测 | "might be due to [process]" | 移至Discussion |

对统计量或数据模式直接含义的一句说明（如 "the zone effect exceeds the elevation effect"）可以保留，不因出现 indicate/show 就整句删除。

## 统计结果报告格式

### 基本格式

```
t检验:     t(df) = value, p = 0.XXX
           示例: t(33) = 2.10, p = 0.034

ANOVA:     F(df_between, df_within) = value, p = 0.XXX
           示例: F(2, 45) = 4.52, p = 0.016

相关:      r = 0.XX, p = 0.XXX
           示例: r = 0.85, p < 0.001

卡方:      χ²(df) = value, p = 0.XXX
           示例: χ²(2) = 8.45, p = 0.015
```

地学期刊（Catena、Journal of Hydrology、Geoderma 等）通常保留前导零；省略前导零的 APA 写法只在目标期刊要求时使用。

### p值规范
服从目标期刊格式。精确报告统计量和 *p* 值，极小值不写作 *p* = 0.000；前导零、变量斜体和小数位应全文一致。

### 效应量
- Cohen's d（t检验）
- η²（ANOVA）
- OR（回归）

### 置信区间
- 格式：95% CI [lower, upper]
- 示例：95% CI [2.34, 5.67]

## 图文互涉原则

> 文字**概括趋势和模式**，不逐点重复图表数据

### ❌ 低级写法
```
"Figure 3 shows the discharge is 10 m³/s in Jan, 20 m³/s in Feb, 
15 m³/s in Mar, 25 m³/s in Apr..."
```

### ✅ 高级写法
```
"As shown in Figure 3, discharge exhibits a distinct seasonal pattern, 
peaking in July (45 m³/s) and reaching minimum values in February (8 m³/s)."
```

### 图表引用句型
```
- "As shown in Figure X, ..."
- "Figure X illustrates the relationship between..."
- "Table X summarizes..."
- "The spatial distribution of X is presented in Figure X..."
```

## 负面结果处理

> **必须如实报告**（科学诚信要求）

### ❌ 错误表达
```
"The intervention had no effect"
"p > .05"（无具体值）
```

### ✅ 正确表达
```
"No significant difference was observed between groups (t(28) = 1.23, p = 0.23)"
"The correlation was not statistically significant (r = 0.18, p = 0.15)"
```

## 句型模板

### 趋势描述
```
- "X showed an increasing/decreasing trend over the study period..."
- "A significant increase/decrease in X was observed..."
- "[Variable] varied from [min] to [max], with a mean of [value]..."
```

### 比较描述
```
- "X was significantly higher/lower in [Group A] than in [Group B] (具体统计)..."
- "Compared to [reference], X increased by [%]..."
- "The difference between [A] and [B] was statistically significant..."
```

### 相关性描述
```
- "A strong positive/negative correlation was found between X and Y (r = 0.XX, p < 0.XX)..."
- "X was positively/negatively correlated with Y..."
- "No significant correlation was observed between X and Y (r = 0.XX, p = 0.XX)..."
```

### 空间/时间分布
```
- "Spatial analysis revealed that X was concentrated in [region]..."
- "Temporal variation showed distinct seasonality, with peaks in [season]..."
- "The highest values of X were observed in [location/time]..."
```

## 核心规范

| 规范项 | 要求 |
|--------|------|
| 客观性 | 结果为主，允许解释数据模式的直接含义 |
| 定量性 | 具体数值、统计参数 |
| 完整性 | 负面结果也要报告 |
| 对应性 | 与Methods完全对应 |
| 主题先行 | 每段开头给出要点 |

## 润色检查清单

- [ ] 未把未经验证的机制或因果推断写入Results
- [ ] 无情感词（interestingly, surprisingly等）
- [ ] 未将未经验证的因果解释当作结果
- [ ] 统计格式符合目标期刊并全文一致
- [ ] 图文互涉（概括趋势，不重复数据）
- [ ] 负面结果如实报告
- [ ] 时态正确（结果过去时，图表现在时）
- [ ] 每段有主题句
- [ ] 与Methods章节对应

## 常见问题修正

| 问题 | 原始 | 修正 |
|------|------|------|
| 解释性语言 | "This suggests that pumping caused the decline" | "Groundwater levels declined by 2.3 m during the pumping period" |
| 情感词 | "Interestingly, the concentration increased" | "The concentration increased from 5.2 to 8.7 mg/L" |
| p值格式 | 同一稿内 "p = .034" 与 "p = 0.034" 混用 | 按目标期刊统一（地学期刊多保留前导零） |
| 重复图表数据 | 逐点列举 | 概括趋势+关键数值 |
| 负面结果回避 | "No significant effect" | "No significant difference was observed (p = 0.23)" |
| 缺少主题句 | 直接列数据 | 添加"Groundwater levels showed significant seasonal variation" |
