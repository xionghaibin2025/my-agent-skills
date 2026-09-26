# Methods（方法）润色规范

> 文中句型只用于识别语步和诊断缺失，不作生成模板；写作时用带内容的具体句替代模板句，见 `de-ai-style.md`。

## 黄金标准

> **可重复性**：描述足够详细，使独立研究者能重复研究并验证结论

## 标准结构模块

### 1. 研究区域概况（Study Area）
按研究问题选择相关信息，保证读者理解研究设计；以下是候选项，不要求每个项目齐全：
- 地理位置（经纬度）
- 气候特征（柯本气候分类、年均温降水）
- 地质构造
- 水文地质条件（含水层类型）
- 土地利用概况
- 研究区域图引用（通常Figure 1）

### 2. 数据采集与处理（Data Acquisition）
**必含信息**：
- 野外采样：时间、频率、数量、方法
- 实验室分析：方法、仪器、检测限
- 遥感数据：数据源、分辨率、预处理步骤
- QA/QC流程：质量控制措施

### 3. 数学模型与统计框架（按研究类型选择）
**必含信息**：
- 模型名称和版本
- 控制方程
- 边界条件
- 初始条件
- **所有符号必须定义**

### 4. 模型评估（按模型用途选择）
预测、模拟和过程模型说明目标函数、参数化、校准/验证数据与相应性能指标。解释性回归、空间统计、Geodetector和GWR/MGWR应报告适合其用途的模型诊断、残差结构、空间依赖、稳健性或敏感性，不强制训练集/验证集或NSE。

### 5. 不确定性分析（按研究类型选择）
预测和过程模型报告敏感性分析与异参同效性；解释性与统计模型报告稳健性检查（子集重跑、替代规格、阈值敏感性）。

## 设备软件规范格式

```
设备名称 + 型号 + (厂商名称, 城市, 国家)
```

**示例**：
- `ArcGIS 10.8 (Esri, Redlands, CA, USA)`
- `Dionex ICS-2100 ion chromatograph (Thermo Fisher Scientific, Waltham, MA, USA)`
- `MODFLOW-2005 (USGS, Reston, VA, USA)`

## 模型性能指标标准

| 指标 | 公式说明 | 合格标准 |
|------|----------|----------|
| NSE | Nash-Sutcliffe Efficiency | 结合研究领域、基线和数据尺度解释 |
| RMSE | Root Mean Square Error | 越小越好，需与观测值量级对比 |
| PBIAS | Percent Bias | 结合变量和应用目的解释 |
| R² | 决定系数 | 报告解释度，不设脱离语境的统一合格线 |

## 时态规则

| 内容 | 时态 | 示例 |
|------|------|------|
| 实验步骤 | **过去时** | "Samples were collected..." |
| 引用图表 | 现在时 | "Figure 1 shows the study area..." |
| 方程性质 | 现在时 | "Equation 1 describes the flow..." |
| 标准方法引用 | 过去时 | "Analysis followed APHA (2012) standard methods" |

## 语态规范

- **现代趋势**：主动语态优先（Nature推荐）
- **被动语态适用**：强调程序或行为主体不重要时
- **核心原则**：按句子重心选择语态，允许自然切换

**示例对比**：
- 主动：`We collected water samples from 20 wells...`
- 被动：`Water samples were collected from 20 wells...`

## 句型模板

### 研究区描述
```
- "The study area is located in [region], covering approximately [area] km²..."
- "The region is characterized by [climate type] climate with mean annual precipitation of [value] mm..."
- "Geologically, the area is underlain by [formation/lithology]..."
```

### 采样描述
```
- "A total of [n] samples were collected from [location] between [date] and [date]..."
- "Sampling was conducted at [frequency] intervals during [period]..."
- "Each sample was filtered through [size] μm membrane and preserved at [temperature]..."
```

### 分析方法
```
- "[Parameter] was measured using [instrument] (Model, Manufacturer, Location)..."
- "Analysis followed [standard method] with a detection limit of [value]..."
- "All analyses were performed in triplicate with relative standard deviation < [value]%..."
```

### 模型描述
```
- "A [model type] model was developed using [software] to simulate [process]..."
- "The model domain was discretized into [n] cells with a resolution of [size]..."
- "Boundary conditions were specified as [type] along [boundary]..."
```

### 校准验证
```
- "The model was calibrated against observed [variable] data from [period]..."
- "Model performance was evaluated using NSE, RMSE, and PBIAS..."
- "Validation was performed using an independent dataset from [period]..."
```

## 核心规范

| 规范项 | 要求 |
|--------|------|
| 时态 | 过去时为主 |
| 可重复性 | 关键参数/步骤无遗漏 |
| 对应性 | Methods与Results完全对应 |
| 完整性 | 模型评估方式与预测、模拟或解释目的匹配 |

## 严格禁止

- ❌ 结果夹杂（如"我们发现..."）
- ❌ 主观评价（如"成功地..."）
- ❌ 信息遗漏（关键参数、仪器型号）
- ❌ 统计方法缺失（无检验类型、显著性水平）

## 润色检查清单

### 基本检查
- [ ] 研究区描述完整（经纬度、气候、地质、水文）
- [ ] 采样信息完整（时间、频率、数量、方法）
- [ ] 仪器设备规范标注（型号、厂商、地点）
- [ ] 统计方法完整（检验类型、α水平、软件版本）
- [ ] 时态正确（过去时为主）
- [ ] 语态选择与表达重心一致

### 模型任务特别检查
- [ ] 控制方程列出
- [ ] 边界条件定义
- [ ] 所有符号解释
- [ ] 预测/模拟模型的校准与验证设计明确
- [ ] 解释性/空间模型的诊断和推断边界明确
- [ ] 指标与研究目的匹配，不机械套用NSE或R²阈值
- [ ] 必要的稳健性或敏感性分析已报告

## 常见问题修正

| 问题 | 原始 | 修正 |
|------|------|------|
| 信息缺失 | "Water samples were analyzed" | "Water samples were analyzed for major ions using ion chromatography (Dionex ICS-2100) with detection limits of 0.01 mg/L" |
| 缺少验证 | 研究目的需要验证但材料未交代 | 提示补充真实验证设计或结果；不编造独立数据、检验或性能数值 |
| 时态错误 | "We collect samples monthly" | "We collected samples monthly" |
| 符号未定义 | "K ranges from 10⁻⁶ to 10⁻³" | "Hydraulic conductivity (K) ranges from 10⁻⁶ to 10⁻³ m/s" |
| 结果混入 | "The model performed well" | 移至Results或删除 |
