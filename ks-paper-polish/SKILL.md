---
name: ks-paper-polish
description: 润色、改写或审查地球科学与水文地质学论文草稿，处理主次不清、论述松散、工程化表达、防御性写作、AI 腔及 ESL 问题。适用于段落、章节、全文和基于明确素材撰写单个章节；按授权调整表达或结构，保持数据与科学含义可追溯。不用于从零设计整篇论文、文献检索、期刊推荐、双语摘要对照校对（见 ks-abstract-review）或定稿溯源与投稿裁决（见 ks-evidence-chain）。
---

# KS Paper Polish

目标是帮助作者把自己的科学观点表达得更清楚、更自然、更有说服力，而不是替作者换一个观点，也不是把严谨写成保守。

## 首要原则：忠实于科学含义

语言修改不得静默改变以下内容：

- 数值、方向、显著性、样本范围和时空尺度；
- 相关、预测、解释和因果关系的层级；
- `may`、`likely`、`expected`、`zone-level`、`wet-season`、`one-sided` 等实质性限定；
- 作者明确提出且有证据支持的核心判断。

纯语言修改可以直接执行。超出授权的科学含义变化须提出供作者判断；已授权实质性修订时可实施，并单独说明主张、证据或范围的变化。复核修改处及其上下文的科学含义，不能只检查语法，也不能把结构压缩误解为逐句保留原稿。

项目 AGENTS.md 里的项目事实（目标期刊、边界清单、项目禁用词表、护栏脚本）优先于本 skill 的默认约定；冲突时按前者执行并说明。通用写作规范以本 skill 的 `references/writing-defaults.md` 与 `references/defensive-writing.md` 为准，项目文件不复制。

## 主张强度：证据校准，而非自动降调

严谨不等于增加 `may`、`could`、`appears`。根据证据选择动词：

- 直接观测或明确统计结果：`show`, `demonstrate`, `reveal`, `establish`；
- 多项独立证据支持的解释：`indicate`, `support`；
- 单一间接证据或存在合理替代解释：`suggest`, `may reflect`；
- 无法区分因果方向时，不得从 association 改成 cause/control/drive。

作者的核心贡献有充分证据时应明确陈述，不得为了安全反复弱化。需要判断主张强度或调整 hedging 时，读取 `references/claim-calibration.md`。

## 任务模式与权限

- **轻度润色**：修复语法、搭配、时态、指代和冗余，不调整论证结构。用户未说明时默认采用。
- **深度语言精修**：允许拆句、合并重复、调整段内顺序和去 AI 腔，但保持科学含义。全文精修或降低 AI 痕迹通常采用此模式。
- **实质性修订**：允许改变主张、论证顺序、章节结构或删减论据。只有用户明确授权时执行。
- **质量检查**：只报告问题和建议，不修改文件，除非用户同时要求修改。
- **防御性写作审计**：按 `references/defensive-writing.md` 的审计模式输出命中表、保留的必要限定清单和重复限定统计；不打分。

## 工作流程

按任务需要执行，不要求每次走完整流程。

1. 确认材料、目标和修改权限。短段落直接处理局部问题；用户要求解决“散、主次不清、主线被淹没”时，已授权为此调整结构与篇幅，但不等于授权另造核心主张。
2. 全文精修、结构诊断或上述主线问题，先读 `references/argument-spine.md`，辨认当前主张、关键证据及反证，再决定哪里值得展开。只有单个章节时依据可见材料判断，不虚构全文主线。
3. 在授权内先处理遮挡主线的重复与旁支，再校准主张和必要限定，最后处理句子。主线不清时说明具体歧义，并继续能安全完成的修改；不靠增加过渡句或总结句掩盖实质缺口。
4. 通用语言修改读 `references/language.md`；撰写章节或全文精修读 `references/writing-defaults.md` 与对应章节文件；全文或去 AI 腔任务再读 `references/de-ai-style.md` 和 `references/defensive-writing.md`。
5. 复核主张与证据的关系、修改处科学含义、引用、必要限定和行文连贯性。只有用户要求或实际节奏问题需要时才统计句长；涉及期刊格式要求时核对目标期刊官方指南。

## 章节路由

| 任务 | 读取 |
|---|---|
| Title | `references/title.md` |
| Abstract | `references/abstract.md` |
| Introduction | `references/introduction.md` |
| Methods | `references/methods.md` |
| Results | `references/results.md` |
| Discussion | `references/discussion.md` + `references/claim-calibration.md` |
| Conclusion | `references/conclusion.md` + `references/claim-calibration.md` |
| 撰写章节、全文精修 | `references/writing-defaults.md` + 对应章节文件 |
| 全文精修、主次不清、论述松散、结构修订 | `references/argument-spine.md` |
| 防御性写作审计 | `references/defensive-writing.md` 审计模式 |
| 全文投稿前检查 | `references/checklist.md` + `references/de-ai-style.md` + `references/defensive-writing.md` |

只加载当前任务需要的参考文件，不机械套用所有章节模板。

## 叙述与 AI 痕迹

正文默认使用连贯段落，但无序列表、结构化摘要、编号结论是否允许，应服从论文类型和目标期刊要求。不得把避免 AI 腔等同于简单删除某些词。还要检查抽象名词堆叠、概念拟人化、机械总结句、同义反复、整齐排比和连续短句。详见 `references/de-ai-style.md`。

## Results 与 Discussion 边界

Results 以报告发现为主，可简要解释统计量或数据模式的直接含义；未经验证的机制、因果推断和文献比较移至 Discussion。不要因为看见 `indicate` 或 `show` 就机械删除整个解释句。

Discussion 围绕核心发现解释其意义，按证据需要讨论机制、文献差异及推断边界，不为每个结果补齐这些项目。局限性集中说明，局部保留防止误读所需的最短限定。

## 模型类型判断

只有预测、模拟或过程模型才机械检查校准/验证。解释性回归、空间统计、Geodetector、GWR/MGWR 等方法，应根据研究目的检查诊断、残差结构、稳健性、敏感性和推断边界，不得强行要求训练集/验证集或 NSE。

## 输出方式

- 短段落：可使用原文、修改、说明三栏。
- 长章节或全文：先提供可直接使用的修订稿，再简述主要改动；不要逐句生成冗长对照。
- 可能改变含义的修改：单独列出原文、修改、原因和风险。
- 仅检查任务：按严重程度报告可操作问题，不输出虚构评分或没有依据的百分比。
- 主线诊断先指出最影响读者理解的问题，并给出具体位置和处理方向。内部判断无需转写成逐段标签、评分表或流程报告；用户要求完整审计时再展开。

## 最终验证

- 数据、统计量、引用和结论方向未改变；
- 核心观点没有被不必要的 hedging 削弱；
- 主次清楚；压缩没有隐藏反证、负结果、必要方法或实质限定；
- 必要限制集中说明，局部限定足以防止误读；
- 无明显 AI 式抽象包装或非母语搭配；
- 章节要求与目标期刊一致，而非机械服从本 skill 的默认范围；
- 用户提供的禁用词表优先，参考文献原始题名不得擅自改写。
