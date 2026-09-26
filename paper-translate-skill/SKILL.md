---
name: paper-translate-skill
description: "把论文 PDF 转成双语对照 Markdown，翻译进程中按图注定位渲染提取各 figure 截图，并归档补充材料。用户要求翻译论文、论文转 Markdown/双语对照、提取论文插图、下载论文补充材料、批量翻译多篇文献并归档译文时使用。支持本地 PDF、DOI 或已由 paper-fetch-skill 获取的归档。不承担文献发现与开放式检索，也不做保留排版的译文 PDF（BabelDOC 域）。"
---

# 论文双语翻译技能

把已有论文转成"英文引用块 + 中文译文"的双语对照 Markdown，过程中以渲染法提取每张 figure 截图，并保证补充材料归档。确定性步骤交给 `scripts/` 四个脚本，翻译由宿主完成；获取、身份核验与补充材料下载委托 paper-fetch-skill，不重复实现下载器。

## 核心契约

- 阶段顺序固定：`身份核验 → 资产准备 → 结构提取 → 图渲染 → 截图对照验收 → 分块 → 翻译 → 合并校验 → 验收 → 报告`。阶段必须有序推进；批量任务中各论文独立推进，一篇阻塞不影响其余。
- 只有 BLOCKING 白名单允许暂停问用户：`identity_mismatch`、`source_unusable`、`figure_layout_unresolved`、`overwrite_existing`、`material_output_choice`。其余情况一律自主推进或按 failure-handling 降级。
- 两种入口分工明确：**paper-fetch 已先行获取**时只复用其归档（含补充材料），不再触发下载；**用户自备本地 PDF** 时补充材料才由本技能委托 paper-fetch-skill 补齐。同一 DOI 已有合格双语 MD 直接复用，不重翻译。
- 交付截图一律用渲染法（图注定位 + 300 DPI 渲染 + 去白边）；`extract_image` 的 xref 盘点只作定位参考，不得作为交付件。
- 每张交付截图必须与整页参考图构成对照证据；未对照的截图不得标记为已验收。
- 脚本跑完不等于成功：交付前必须通过 merge_verify 的结构化验收（配对率、断链、公式、文献数）并按 acceptance 分面报告；降级必须原样保留，不得把"缺补充材料""公式待确认"说成完整交付。
- 翻译纪律：术语首现附英文、参考文献不译、公式用 LaTeX 重建且假设处标"待确认"；重建不了的保留原文并说明。
- 预设只补全未指定项：用户明确的输出路径、对照格式、图片命名直接沿用，不重复确认。

## 按需参考

- 开始任务先读状态机、BLOCKING 白名单、本地优先决策树和批量进度规则：[`references/workflow.md`](references/workflow.md)。
- 确定任务形态后读四个预设之一及落盘矩阵、产物命名规则：[`references/presets.md`](references/presets.md)。
- 提取正文、公式与参考文献前读文本底本选择和提取规则：[`references/extraction.md`](references/extraction.md)。
- 截图前读渲染规范、版式自适应规则与对照验收要求：[`references/figures.md`](references/figures.md)。
- 交付前读验收分面、merge_verify 输出核对和最终报告格式：[`references/acceptance.md`](references/acceptance.md)。
- 出现 PDF 异常、图注漏检、翻译块缺失或需重试时读对应决策表：[`references/failure-handling.md`](references/failure-handling.md)。

脚本用法、参数、依赖与输出契约见 [`scripts/代码说明.md`](scripts/代码说明.md)；首次使用脚本前必读。
