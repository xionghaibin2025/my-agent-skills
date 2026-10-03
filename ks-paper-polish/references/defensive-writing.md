# 防御性写作：放置规则与投稿前审计

本文件是防御性写作的唯一正本。项目 AGENTS.md 只写本项目须交代的边界清单并指向本文件；`ks-evidence-chain` 的定稿核对按本文件的审计模式跑一遍。审计分类法参考 Worigin0314/academic-defensive-writing-auditor（MIT），信号句按地学论文改写。

优先陈述发现及其依据，在需要防止误读处给出范围。不要把“主张—证据—边界”套成每段必备结构。预想反对、堆叠免责声明再给出被削弱的主张，会让作者的担心遮挡研究结果。

科学限定改变读者对证据的解释，要保留；防御性措辞主要回答想象中的批评，要改掉。区分标准见「必要性判定」。

## 写作时：每条边界只完整解释一次

| 位置 | 写什么 |
|---|---|
| Methods | 设计、数据、分析边界，变量筛选方法 |
| Results | 结果及其直接统计含义；不为方法选择辩护 |
| Discussion | 真正影响解释范围的限制，集中在 Limitations 段：影响方向与可行的验证办法 |
| Abstract / Conclusion | 只保留会改变核心结论适用范围的最短限定 |
| Data Availability | 只写访问条件，不把数据权限写成科学局限 |
| 图注 | 说明图示内容及正确解读所需的样本范围、排除条件和符号；不附与图无关的辩护 |

同一限制在其他章节确需提及时，用最短的范围限定，不重复原因和补救方案。

三个常见来源：

- 审稿答复进正文。审稿或内审指出的弱点，处理方式是改数据、改结论方向或改措辞，不在原句后追加免责句；答复写进 response letter。
- 核验替代。核验不了的内容补证或删除，不用限定句留在正文里。
- 写作时预答审稿人。批判用于审查环节；写作环节预答想象中的审稿人，产物就是防御性写作。

## 投稿前审计

### 分类与信号句

| 类 | 名称 | 地学论文里的信号句 | 处理 |
|---|---|---|---|
| D1 | 预答审稿人 | It should be noted that / We emphasize that / One might argue / A potential concern is / To avoid misunderstanding | 直接陈述技术事实 |
| D2 | 反复声明不主张 | we do not claim / should not be interpreted (construed, taken) as / does not establish / is not intended to / is not (an) independent (direct) evidence / cannot be attributed / merely (purely) exploratory (descriptive) / beyond the scope | 直接陈述有支持的主张，合并重复边界，保留有独立含义的否定 |
| D3 | 限定堆叠 | 一个主张周围同时出现 although / while / only / may / potentially / to some extent 中的多个 | 去掉重复弱化，保留各自改变推断的条件 |
| D4 | 为弱结果开脱 | is likely due to limited sample size / is expected given / remains encouraging despite / given the complexity of the system | 先报结果；只有诊断或证据支持时才解释 |
| D5 | 为缺失的工作辩护 | was not included because / further research is needed to（每段一次）/ due to data availability / such a comparison would be unfair | 实质缺失在 Limitations 写一次；否则只描述做了什么 |
| D6 | 把控制说成公平 | for a fair comparison / to ensure comparability / we believe this is sufficient | 直接写控制了什么变量 |
| D7 | 反复标注初步性 | preliminary / exploratory / indicative / within the study area 在多处出现 | 只在技术上必要处使用 |
| D8 | 褒义词补偿证据 | robust / reliable / comprehensive / promising / novel / strong evidence 没有对应依据 | 用已有测量值、方法事实或具名性质说明；不能为替换形容词补造数字 |
| D9 | AI 式总结句 | Taken together / Collectively, these results demonstrate / These findings further validate / provide a solid foundation for | 冗余则删；否则改成数据支持的那一条推断 |
| D10 | 绝对化辩护 | cannot be fully excluded / is impossible / no method can / there is no need | 写出支持该说法的具体条件 |

D2 可作检索句型表，命中后按下列必要性判定处理，不能仅凭位置或词形删除。反证、负结果和限定推断的事实不是防御性内容。D8 是反方向：过度声称与过度防御常同时出现，两边都查。

### 必要性判定

对每个命中的句子问五个问题：

1. 删掉它，读者对证据的解释会不会被误导？
2. 它报告的是有证据的条件、不确定性或限制吗？
3. 它的主要目的是不是回答想象中的批评？
4. 能不能改写成「评估了什么、观察到什么、什么在范围外」的正面陈述？
5. 同一限定前面是否已经出现过？

判为四档：必要限定 / 防御 / 混合 / 无问题。必要限定保留，语义等价时可改成正面陈述；纯辩护删除或改写，需完整解释的真实限制移至合适位置；混合句去掉辩护措辞并保留事实与条件。

### 改写规则

- 事实先行，解释在后。
- 语义等价时正面陈述范围；「支持 X 但不能证明 Y」若区分了真实的证据层级，应保留或简化。研究对象范围不能替代代表性、因果识别或外推限制。
- 合并重复限定；独立影响推断的条件均须保留，避免强行压成一条后丢失范围。
- 形容词可换成材料中已有的测量值或具体事实。缺少依据时提出补证问题，不新增样本、方法、性能、机制或保障措施来使句子更有力。
- 写控制了什么，不写「公平」。
- 没有证据不解释弱结果。
- 不把主张提升到证据之外；不删除会改变读者判断的限制。
- 不增加技术信息的句子优先删除。

### 例句

以下均为示意，不是研究证据。每行仅使用原句提供的信息；实际改写调用其他材料时，先核对其来源和适用条件。无法据原句完成的改写明确列为待补证，不提供虚构成句。

| 原句 | 改后 | 说明 |
|---|---|---|
| It should be noted that these results should not be interpreted as evidence of a causal link between elevation and salinity. | These results do not establish a causal link between elevation and salinity. | 删除提醒语，保留因果识别限制；不补造相关方向、系数或未做检验的事实 |
| Although the improvement is modest, the result is still encouraging: R² increased from 0.71 to 0.76. | R² increased from 0.71 to 0.76. | D4，使用原句已有数值，不增加方法或归因 |
| Due to limited sample size, further research with more samples is needed to confirm these findings. | 先核对样本量及其对推断的具体影响，再决定限定内容和位置；原句不足以生成具体范围句。 | D5，不从样本少直接推出只能推断某些区域 |
| For a fair comparison, all models were trained on the same 343 samples. | All models were trained on the same 343 samples. | D6 |
| Our results provide robust evidence for the strong control of groundwater depth on salinization. | 核对实际结果和因果依据后改写；原句不足以确定解释率、因素排名或控制关系。 | D8，不能用虚构的具体性替代空泛评价 |
| Taken together, these findings highlight the importance of hydrogeological setting. | 若前文已表达同一判断且本句无新增推断，则删除；否则明确它指向的有依据的判断。 | D9，先检查上下文 |
| We do not claim that the sample is representative of the regional population. | The sample's representativeness for the regional population has not been established. | 保留代表性尚未建立的含义，不能仅改成研究地点或时间范围 |

### 输出

审计模式只出三样东西：命中表（位置、原句、类别、判定、处理、改写；只标不改的任务不填改写）；保留的必要限定清单；重复限定统计（同一限制出现在哪几处）。不打分，不逐句写审稿人会怎么想。

派给其他模型审计时，任务书附本文件，并要求同时标出过度声称与过度防御。
