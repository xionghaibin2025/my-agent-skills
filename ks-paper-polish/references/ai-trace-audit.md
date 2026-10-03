# AI 痕迹审计

审计模式：定稿前逐句核查全文，输出命中表，不直接改稿；用户同时要求改写时按 `de-ai-style.md` 的方法改。怎么写、怎么改在 `de-ai-style.md`，本文件只管怎么查、怎么判、怎么报。

审稿人说"有 AI 痕迹"时，指的通常不是某个词，而是三件事：句子不承载可被证伪的信息（空话）、对自己工作的评价代替了结果（宣传）、段落与句式整齐到看不出作者在想什么（机械）。逐词替换同义词一件也解决不了。

## 判定标准：删掉这句，读者损失什么

对每个候选句问一次：删掉后，读者是否失去一条可被数据证伪的信息、一个必要的条件，或一次真实的推断转折？

- 失去 → 无问题。表达生硬另按 `language.md` 处理。
- 不失去，且句子在陈述本研究的价值、重要性、前景或首创性 → 宣传。
- 不失去，也不宣传，只是把已说过的内容换一种说法，或给某段补一句"意义" → 空话。

空话删除。宣传改成研究实际做了什么、测到什么；只有当它替代的是一条真实推断时才改写保留，不是换个谦虚的形容词。

## 高发区，按此顺序扫

1. Abstract 末两句、Conclusion 全段：宣传与空洞总结最集中。
2. Introduction 首段与末段：模板开头、重要性堆叠、贡献自述。
3. Discussion 各小节的首句与末句：机械总结、意义回声。
4. Results 每段末句：给每个结果补一句解释。
5. 节与节之间的过渡句、元话语。
6. 最后整篇通读一遍，只看结构与节奏是否同构。

## 分类与信号句

| 类 | 名称 | 信号句 | 处理 |
|---|---|---|---|
| A1 | 模板开头 | With the rapid development of / In recent years, X has attracted increasing attention / plays a crucial (vital, key) role / is of great significance | 换成本研究要解决的具体问题及其已知状态 |
| A2 | 前景与价值自述 | provides valuable insights / offers a new perspective / lays a solid foundation / paves the way for / holds great promise / has broad application prospects | 删除；确有具体用途时写谁能用它做什么 |
| A3 | 贡献自述 | The main contribution of this study is / This study is the first to / we propose a novel framework / a comprehensive analysis of | 直接写做了什么、得到什么；`first`、`novel` 须给出具体对照对象 |
| A4 | 空洞总结 | Taken together / Collectively, these results / These findings further confirm / highlight the importance of | 冗余则删，否则写出它指向的那一条判断（同 `defensive-writing.md` D9） |
| A5 | 意义回声 | 每个结果后追加一句"这说明该方法有效""该因素重要" | 删除；真实推断并入该段的论证句 |
| A6 | 抽象名词堆叠与拟人化 | framework / mechanism / strategy 连续出现而无动作主体；the analysis reveals, the comparison carries information | 还原成谁对什么做了什么 |
| A7 | 机械衔接 | moreover, furthermore, additionally, notably, importantly 高频出现 | 用数据或过程建立衔接 |
| A8 | 同义反复 | 同一判断在一段内换三种说法出现；或同一结果在不同节近乎同句重报 | 只留信息量最大的一处；跨节时在论证所需处保留，其余处用节号指代 |
| A9 | 整齐排比 | 每段都是三项并列；每节都是"背景—方法—结果—意义"四句 | 按内容轻重重排，允许段落不等长 |
| A10 | 元话语与过程汇报 | In this section, we first / To this end / It is worth noting that / we performed a series of analyses | 删除；分析步骤属于 Methods。影响可信度的质控事实（核对范围、结果）在 Methods 保留为一句陈述，删去过程叙述 |
| A11 | 节奏同构 | 连续短句、句长相近、每段句数相同 | 按命题关系合并或拆分，见 `de-ai-style.md` |
| A12 | 无依据的补全 | 新增的因果、机制或统一解释，在来源与早期草稿里找不到依据 | 核对来源；核不到标为待核验，不改写成确定表述 |
| A13 | 跨节复述卖点 | 全文核心主张（通常即标题主张）以近似措辞出现在 `writing-defaults.md` 规定位置之外，如 Related Work、Methods 开头、Results 段首或段末、各小节末句。规定位置之间近乎同句复述也计入；小节首句陈述本节自己的判断不算；本节判断与标题主张相同时，小节标题或首句已陈述即可，正文再述计入 A13 | 按 `writing-defaults.md` 的出现位置保留，其余处用术语指代或直接给该节证据 |
| A14 | 主张强度超出证据 | 未检出差异写成 the same / equally；只检验了部分类别却写 every / all；关联写成 follow / control；单一样带或样区推出通则；复述本文结果时扩大范围或改变方向 | 按 `claim-calibration.md` 校准到证据所支持的强度与范围 |

A2、A3、A14 与 `defensive-writing.md` 的 D8（褒义词补偿证据）是同一问题的两面：过度声称与过度防御常同时出现，两份清单一起跑。同一句同时命中 A 类与 D 类时，只按主类别计一次，另一类写在处理建议里。翻译腔与 ESL 搭配归 `language.md`，不计入本审计。

## 前后呼应核对

审稿人说"机械、没有逻辑"时，常指各部分之间对不上：

- Introduction 提出的每个缺口，Discussion 有一处回应；没有回应的缺口要么删，要么说明本文为什么不回答它。
- Abstract 与 Conclusion 的每条主张，正文有一个段落给出对应证据，范围一致。
- Results 的每个主要发现，Discussion 要么解释、要么明确说不解释；不能只挑有利结果谈。
- 正文引用图表处的说法与图表实际内容一致（逐图逐数核对归 `ks-evidence-chain`）。

这项核对查的是主张有证据、缺口有交代，不要求每项内容都回扣主线。反方向同样要查闭合过度：每个动机恰好对应一个方法，每个方法都配一段理论依据，每项分析都证实核心主张，每节末句都回扣同一卖点。闭合过整时，核对是否略去了不支持主张的结果、事后补配的理由或实际做过的经验选择；有则恢复，并在命中表中列为 A9 或 A13。

## 做法

分节处理，一次一节，按句切分后逐句判定，不抽样。AI 痕迹分布不均，抽样会漏掉集中成片的段落。

派给其他模型做时，任务书附本文件与 `defensive-writing.md`，写死四条：只标不改；每条给行号或可定位的原句；同时标出过度声称；不给 AI 生成概率与检测器分数。不同模型对同一节的命中差异较大，Abstract、Conclusion 和 Discussion 首末值得跨厂商各跑一遍，取并集后由编排者逐条判定，不直接采纳。

## 输出

命中表：位置 | 原句 | 类别 | 判定（空话 / 宣传 / 机械 / 过度声称 / 无问题） | 处理建议。

另附两项：按类别的全文命中计数（用于判断是哪种毛病，不是分数）；前后呼应核对中对不上或闭合过度的条目。

不输出 AI 生成概率、检测器分数，也不在只检查的任务里附完整改写稿。
