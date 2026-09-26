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
| D2 | 反复声明不主张 | we do not claim / should not be interpreted (construed, taken) as / does not establish / is not intended to / is not (an) independent (direct) evidence / cannot be attributed / merely (purely) exploratory (descriptive) / beyond the scope | 正说被支持的主张，范围只限定一次 |
| D3 | 限定堆叠 | 一个主张周围同时出现 although / while / only / may / potentially / to some extent 中的多个 | 留最强的被支持主张，一条实质限制移到应在的位置 |
| D4 | 为弱结果开脱 | is likely due to limited sample size / is expected given / remains encouraging despite / given the complexity of the system | 先报结果；只有诊断或证据支持时才解释 |
| D5 | 为缺失的工作辩护 | was not included because / further research is needed to（每段一次）/ due to data availability / such a comparison would be unfair | 实质缺失在 Limitations 写一次；否则只描述做了什么 |
| D6 | 把控制说成公平 | for a fair comparison / to ensure comparability / we believe this is sufficient | 直接写控制了什么变量 |
| D7 | 反复标注初步性 | preliminary / exploratory / indicative / within the study area 在多处出现 | 只在技术上必要处使用 |
| D8 | 褒义词补偿证据 | robust / reliable / comprehensive / promising / novel / strong evidence 后面没有数字 | 换成测量值、方法事实或具名性质 |
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

判为四档：必要限定 / 防御 / 混合 / 无问题。必要限定原样保留或改成正面陈述；防御句删除、改写或移入 Limitations；混合句拆成事实句加一条限定。

### 改写规则

- 事实先行，解释在后。
- 范围用正面陈述：Under the evaluated conditions, X。不用「支持 X 但不能证明 Y」。
- 合并重复限定；独立影响推断的条件均须保留，避免强行压成一条后丢失范围。
- 形容词换成测量值。
- 写控制了什么，不写「公平」。
- 没有证据不解释弱结果。
- 不把主张提升到证据之外；不删除会改变读者判断的限制。
- 不增加技术信息的句子优先删除。

### 例句

| 原句 | 改后 | 说明 |
|---|---|---|
| It should be noted that these results should not be interpreted as evidence of a causal link between elevation and salinity. | Salinity decreases with elevation (ρ = −0.70); the causal pathway was not tested. | D1 与 D2，正说加一次范围 |
| Although the improvement is modest, the result is still encouraging given the heterogeneity of the study area. | Spatial block cross-validation increased R² from 0.71 to 0.76. | D4，只报结果 |
| Due to limited sample size, further research with more samples is needed to confirm these findings. | 若样本量确实改变结论范围，在 Limitations 写一次：The 43-profile dataset limits inference to the sampled zones. | D5，写一次 |
| For a fair comparison, all models were trained on the same 343 samples. | All models were trained on the same 343 samples. | D6 |
| Our results provide robust evidence for the strong control of groundwater depth on salinization. | Groundwater depth explained 56% of the variance in EC, the largest share among the tested factors. | D8 |
| Taken together, these findings highlight the importance of hydrogeological setting. | 删除，上一句已给出数据。 | D9 |
| Confidence intervals are wide because only 18 wells were sampled. | The 18-well dataset yields wide confidence intervals. | 必要限定，保留并改成正面陈述 |

### 输出

审计模式只出三样东西：命中表（位置、原句、类别、判定、处理、改写）；保留的必要限定清单；重复限定统计（同一限制出现在哪几处）。不打分，不逐句写审稿人会怎么想。

派给其他模型审计时，任务书附本文件，并要求同时标出过度声称与过度防御。
