# 论文项目规则模板

两块内容，分别贴到两个位置。示例数字和领域说明按项目替换。

- **块 A** 贴进项目 `AGENTS.md`（`CLAUDE.md` 用一行 `@AGENTS.md` 导入）。Codex 原生读 AGENTS.md；派给其他模型的任务书要把 3.7 原文带上。3.7 与本skill的 `defensive-writing.md` 同源，改一处要同步另一处。
- **块 B** 指向仓库 `global/` 里的全局文件正本，用脚本装到本机。

---

## 块 A：项目 AGENTS.md 写作规范

```markdown
## 沟通风格

**核心态度**: 以国际顶级期刊审稿标准审视所有内容，不迎合、不敷衍。

- 发现逻辑漏洞、论证不足时，直接指出并说明原因
- 宁可提出不同意见引发讨论，也不盲目执行有问题的方案
- 批判用于审查环节。写作环节不预答想象中的审稿人，预答的产物就是防御性写作（见 3.7）

任务完成后只报告：核心改动（1-2 句）、修改前后关键差异（2-3 句）。不要评分系统、详细对比表、多层评价、长引用。

## 3. SCI 论文写作规范

### 3.1 语言风格

- 主动语态为主（"We propose..." / "This study demonstrates..."）
- 单句不超过 25 词
- 精确学术动词：investigate, demonstrate, reveal, quantify, characterize
- 避免模糊表达："some", "many", "very", "a lot of"

**英文禁用词**（AI 痕迹）:
encompass, burgeoning, pivotal, profound, holistic, innovative, transformative, cutting-edge, seamlessly, leverage, harness, unveil, unlock, unleash, delve, embrace, pave, embark, paramount, foster, revolutionize, multifaceted, moreover, furthermore, indeed, consequently, notably, it is worth noting that

**中文禁用词**:
首先、其次、此外、最后、总之、综上所述、有着、无可替代、深入探讨、全方位、多角度、与此同时、不难发现、值得注意的是、毋庸置疑、显而易见、众所周知

### 3.2 叙述式写作原则

正文采用完整议论文段落，禁止一切列举结构：

- 禁止无序列表（- 或 •），所有内容整合为叙述性段落
- 禁止 "Label: content" 式段落开头（"Background: ..." / "Methods: ..." / "Significance: ..."）
- 禁止编号式列举（"threefold" / "Firstly, Secondly" / "(1) (2) (3)" / "three main reasons"）

每个段落以完整句子开头，按 TSEI 组织：Topic sentence → Supporting evidence → Explanation → Implication。Discussion 与 Conclusion 必须是流畅叙述文体。

### 3.3 理论深度

不止说"是什么"，要解释"为什么"和"如何"；与理论框架明确关联；定量数据服务于机理解释，不堆砌。

### 3.4 结构规范

| 部分 | 核心内容 | 篇幅占比 |
|------|----------|----------|
| Introduction | Background → Gap → Objective → Contribution | 15-20% |
| Methods | Study area → Data → Methods → Validation | 25-30% |
| Results | 按逻辑顺序展示，数据先行 | 25-30% |
| Discussion | 解释意义 → 与前人对比 → 局限性 → 展望 | 20-25% |

### 3.5 量化要求

| 类型 | 格式 | 示例 |
|------|------|------|
| 均值±标准差 | mean ± SD (n = X) | 3.77 ± 3.08 mS/cm (n = 343) |
| 相关系数 | *r* = X.XX, *p* < 0.05 | *r* = -0.946, *p* < 0.001 |
| 模型评估 | R² = X.XX, RMSE = X.XX | R² = 0.76 ± 0.04 |
| 检验统计量 | χ² = X.XX, *p* = X.XX | χ² = 25.564, *p* = 0.001 |

### 3.6 格式速查

| 项目 | 规范 | 示例 |
|------|------|------|
| 数字+单位 | 半角空格 | `2.3 dS/m` |
| 变量 | 斜体 | *EC*, *r*, *p*, *q* |
| 单位/缩写 | 正体 | R², RMSE, mg/L |
| 引文 | 作者-年份 | (Zhang et al., 2023) |
| 图表引用 | 括号内 | (Fig. 1), (Table 2) |

### 3.7 限定与防御

论文是观点。不造假、不过度推因果；也不防御性写作、不自曝其短。

- 每条真实的范围边界（数据代表性、方法假设、无法分离的机制）只写一次，位置是 Methods 对应小节或 Discussion 末尾的 Limitations 段。Results、Discussion 其余段、Conclusion、Abstract、图注不再重复。
- 下列句型只允许出现在 Limitations 段：we do not claim / is not intended to / should not be interpreted (construed, taken) as / is not (an) independent (direct) evidence / cannot be attributed / merely (purely) exploratory (descriptive) / beyond the scope。
- 审稿或内审指出的弱点，处理方式是改数据、改结论方向或改措辞，不在原句后追加免责句；答复写进 response letter。
- 图注只写图上有什么，不写图上没有什么。
- 派给其他模型写作时，任务书原样带上本节；派审稿时同时要求标出过度声称与过度防御。

## 质量检查清单

- [ ] 每个核心观点有定量数据支撑
- [ ] 统计描述完整（均值、标准差、样本量、显著性）
- [ ] 图表信息充分且自洽
- [ ] 无 AI 痕迹词汇
- [ ] 无无序列表、无 "Label: content" 段首、无编号式列举
- [ ] 所有段落以完整 Topic Sentence 开头
- [ ] Discussion/Conclusion 采用流畅叙述文体
- [ ] 机制解释有理论深度，不止描述现象
- [ ] 每条范围边界只出现一次（按 3.7 句型表 grep，命中处逐一定位）
- [ ] 无审稿答复式句子进入正文
- [ ] 图注无"未画/不含"类防御内注
- [ ] 摘要 150-250 词，单段无列举
- [ ] 引用格式统一
- [ ] 投稿声明齐全（Data Availability、Conflict of Interest、Author Contributions）
- [ ] 图表文件、图题、正文引用、Supplementary 编号一致
- [ ] 无作者批注、占位符、未完成标记

## 关键提醒

- 数据一致性：引用数据须与来源（学位论文、归档表）一致，不可随意修改
- 图件红线：图注承诺的内容必须画出来；正文引用的统计量必须能从归档数据复算，复算不出的要么补数据要么删除
- 图上任何非本研究数据的线（判别域、端元场、边界曲线）要能溯源并验证；未验证的在图注与 README 标注
- 更新项目记忆文件前先征得用户同意
```

---

## 块 B：全局文件

全局约束的正本在仓库 `global/` 目录（`global/claude/CLAUDE.md`、`global/codex/AGENTS.md`），用 `global/restore.ps1` 装到本机，见 `global/README.md`。学术论文节的划界原则概括如下，正文以正本为准：

- 模型不得自证自己的核心主张；定稿前由未参与生成的审查者做反证式审查。
- 派生数值必须来自实际执行的代码或可信软件；跑不了就标未核验。
- 以上两条约束的是模型对用户的汇报，不是稿件文体；稿件里每条范围边界只在 Methods 或 Limitations 写一次。
