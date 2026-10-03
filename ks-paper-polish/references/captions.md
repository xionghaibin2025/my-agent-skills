# 图名、图注、表名、表注

图名说明画的是什么，图注说明怎么读。发现、机制、辩护和制图记录写在别处。撰写、润色图表题注，以及随绘图脚本生成题注时都按本文件；目标期刊指南有具体要求时以指南为准。

## 图名

- 一个名词短语，写对象加变量或对比，通常 3–12 个词，不超过 15 个词。
- 不写成结论句、问句或"主题: 结论"。结论属于 Results。期刊惯用陈述式图名（如 Nature 系）时跟随期刊，仍限一句，强度按 `claim-calibration.md`。
- 不用 `Plot showing`、`Results of`、`Illustration of` 这类空壳开头；直接写内容。
- 术语、缩写、类别名与正文一致。图名不重复印在图面上。
- `Fig.` 或 `Figure`、图名后用句号还是冒号、面板标号样式按目标期刊；期刊图注不设独立图名时，首句承担图名的作用。

| 原始 | 修正 |
|---|---|
| `Why the original sampling design left regional transition area poorly determined` | `Sampling design and precision of the transition-area estimates` |
| `Organic carbon at the verified stable reference sites: the comparison returns no summary-independent estimate` | `Organic-carbon contrasts by summary statistic and carbon-provenance subset` |
| `Which part of a second map's information improves which estimation target` | `Standard-error ratios of the sampling designs by estimation target` |

## 图注

默认形态是"图名 + 面板清单"，面板用名词短语、分号并列：

`Figure 5. Screened nitrate reference conditions and robustness: (a) candidate NO₃⁻ distributions; (b) bootstrap uncertainty; (c) threshold sensitivity.`

单面板图可以只有图名。多面板图注通常 30–60 个词，单句不超过 25 个词。不写 `Panel (a) shows ...`，不在一句里同时交代三个面板的内容、顺序和解释。

在面板清单之外，只加读图必需的信息：

- 符号、颜色、线型、填充与空心、显著性标记的含义，参考线和阴影带是什么；
- 误差线或区间的类型（SE、95% CI、IQR）、样本量、单位、坐标变换；
- 影响读图的约定：比值或差值的方向、阈值、被画出但未计入统计的样本；
- 图面和图注中出现的非通用缩写在图注内给出全称；类别或分组的定义较长时写 `defined in Section 2.4`，不在图注展开；
- 非本研究数据的来源，重绘图的原始出处与修改方式，期刊强制的地图声明。

以下内容移走或删除：

| 内容 | 例 | 去处 |
|---|---|---|
| 结果解释、机制、综合判断 | `Verification therefore removes ...; it does not create the imbalance` | Results / Discussion |
| 防御句，说明没画、没做什么 | `The figure does not re-adjudicate any label, and no annual strip is drawn because ...` | 删除；真实边界在 Methods 或 Limitations 写一次 |
| 方法细节 | 投影参数、网格北与真北的夹角、模型公式推导 | Methods / 补充方法 |
| 制图记录 | `Sources: <路径>`、seed、软件版本、dpi、文件标识符 | 归档图注或 README |
| 内部记录 | `the adjustments the Abstract names`、superseded、companion paper、审稿轮次、编者注、TODO、内部路径与内部文件名 | 删除 |
| 对图面排版的描述 | `every ratio is printed to three decimals`、`both named on the axis` | 删除 |
| 正文已报告的数字 | 逐个复述各组估计值 | 只留读图必需的数字 |

期刊要求图注可独立读懂时，保留上面的读图信息即可满足，不靠加解释句。用户给出过认可的定稿图注时，以它的长度和形态为基准。

## 一致性

缩短不能引入错误。改完逐条对照图面和正文：

- 每个面板都有描述；叠加图层不写成独立面板；图注承诺的内容确实画出（定稿时的逐图核对归 `ks-evidence-chain`）。
- 图注里的数字、样本量、倍数与正文和源表一致。常见错位：图注沿用旧版本数字；图注写全样本而某面板只用子集；图注样本量含已剔除样本。
- 阈值用语全文统一，明确 `>` 或 `≥`；`at most 0.05` 这类界限按实际值核对。
- 统计用语按技术含义使用：共享样本的嵌套估计不称 `independent`，与多个因素混杂的分层变量不称 `negative control`，子集不称 `group`。图上画 95% CI 而判定用 90% CI 时写明。
- 格式：`×`、`−`、下标（`K₂O`）、`1.5 × IQR`、数字与单位间空格，与正文一致。
- 正文的 `Fig. 4a` 指向确实画了该内容的面板；每个图表都被正文引用，首次引用顺序与编号一致。
- 图注存在多份副本（随图归档版、正文图注块）时，改一处同步另一处。归档版可保留来源与渲染参数，投稿版不带。

## 图面文字

图内用短标签，解释放图注。图下方的灰色小字说明并入图注或删除。数据来源长句不放图面中央。

## 表名与表注

表名同图名：名词短语，不写 `Table summarizing ...`，不带结论。表注置于表下，只解释本表独有的分母、处理规则、缩写、统计量、显著性标记和来源；通用方法写一次，其他位置短引用。表注描述必须与单元格实际内容一致，例如单元格是主效应与交互项时，不能注成四种组合的原始得分。补充表同样适用；补充材料的表题列表与正文引用编号逐一对应，不跳号。
