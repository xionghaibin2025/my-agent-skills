# 方法来源

本技能的做法参考了以下开源技能，内容经改写后使用，未复制原文。

| 来源 | 许可 | 借鉴的内容 |
|---|---|---|
| [Rimagination/easyplot](https://github.com/Rimagination/easyplot) `references/aesthetic-distillation.md` | MIT | 证据阶梯与子图角色、主图加辅图排版、跨子图编码一致、配色先定角色、参考图风格提取步骤、数据加示意图组图、默认排除的做法 |
| Anthropic Claude Science `figure-composer`、`figure-style` | Apache-2.0 | 从一句主张出发安排子图，渲染后逐子图查看，已合格部分不再修改，按样本量选分组图画法 |
| [Haojae/scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill) | MIT | 先剖析数据再选图，同一数据按不同主张选不同图 |
| [trae1ounG/paper-plot-skills](https://github.com/trae1ounG/paper-plot-skills) | 未声明 | 参考图配说明卡与可运行脚本（只借鉴做法） |
| [Dsadd4/AgentFigureGallery](https://github.com/Dsadd4/AgentFigureGallery) | MIT | 记录用户选中与排除的方案并在后续任务中使用 |

`assets/palettes.json` 的色值取自 EasyPlot 色带目录所记录的上游来源（Okabe–Ito、Paul Tol、ColorBrewer、viridis、Scientific Colour Maps、ggsci），各色带的许可列在该文件中。`scripts/cvd_preview.py` 的色觉模拟采用 Machado, Oliveira & Fernandes (2009) *A physiologically-based model for simulation of color vision deficiency*（IEEE TVCG 15(6)）的完全缺失矩阵。
