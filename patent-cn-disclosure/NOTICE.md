# NOTICE——衍生声明

本 skill（patent-cn-disclosure）由本项目 2026-10-03 会话B调研（GitHub 专利撰写 skill 调研）结论"改造采用"派生制作；v1.1 起吸收两件真实交底书实战经验，v1.2 对齐专利①现行版（金标准），v2.0 增设双版模板，v2.2 完成三模型交叉审查后的口径统一与精简（版本沿革见文末）。依据 MIT 许可证保留原作者版权声明：

## 来源一：handsomestWei/patent-disclosure-skill
- 仓库：https://github.com/handsomestWei/patent-disclosure-skill
- 许可证：MIT © handsomestWei
- 本地存档：`E:\2_AI工作区\agent\zcode\project_项目\20261003_143403_专利skill调研\2_候选仓库存档\patent-disclosure-skill\`（HEAD 5073d3d，2026-09-30）
- 改编来源文件 → 本 skill 对应文件：
  - `skills/patent-disclosure/prompts/invention/disclosure_builder.md`（章节结构、7.9 术语与标题贯穿、7.10 D1与Fk/三段绑定/删除测试、7.5 脱敏）→ `references/disclosure-template.md`
  - `skills/patent-disclosure/prompts/invention/template_reference.md`（模板章节、mermaid 步骤号规则、符号表体例）→ `references/disclosure-template.md` §三
  - `skills/patent-disclosure/prompts/disclosure_self_check.md`（§8.1 逻辑闭环、§8.2 公式一致性、§8.7 法定要件/客体/参数可获得性/防自伤）→ `references/self-check.md`（剔除工具绑定项与实用新型/外观/围栏章节）
  - `skills/patent-application/prompts/claim_strategy.md`（独权取材5.1、从属树四层、歧义处置）→ `references/claims-guide.md`
  - `skills/patent-application/prompts/claims_builder.md`（方法独权句式、步骤同义、所述前置、公式入正文、禁宣传语）→ `references/claims-guide.md`
  - 八步流程思想（intake→扫描→挖点→查新→D1→成文→自检）→ `references/workflow.md`（查新改为外接接入、增加权利要求草稿步）

## 来源二：HuangXinzhe/cn-patent-drafting
- 仓库：https://github.com/HuangXinzhe/cn-patent-drafting
- 许可证：MIT © HuangXinzhe
- 本地存档：`E:\2_AI工作区\agent\zcode\project_项目\20261003_143403_专利skill调研\2_候选仓库存档\cn-patent-drafting\`（HEAD 9be95a9，2026-07-04）
- 改编来源文件 → 本 skill 对应文件：
  - `references/disclosure-and-application.md`（3.6 可选实施方式、六、实施例及可替换方案章节）→ `references/disclosure-template.md` 替代方案章节（v1.0 为§六；v1.1 依用户修订意见前移为§四并合并可选实施方式）
  - 同文件 Drafting Style（事实三分：来源支撑/合理推断/待确认）→ `SKILL.md` 硬规则2、`references/workflow.md` Step 2

## v1.1 新增内容的来源（2026-10-04，任务 20261004_160811）

- **scripts/docx生成/generate.js（v5 通用版）**：演化自专利①案件（20261003_151743）`5_代码\docx生成\generate.js`（v1–v4，本项目自产，格式经用户九轮修订确认）；v5 泛化：CLI 化、图片行驱动、通用红字机制、自动页眉、写后回读核验。node_modules（docx@9.8.1）复制自该案件已验证安装。
- **references/defensive-writing.md**：
  - D1–D10 过度防御审计分类转译自 `C:\Users\Akesu\.skills-manager\skills\ks-paper-polish\references\defensive-writing.md`（本机 skill，其分类参考 Worigin0314/academic-defensive-writing-auditor，MIT）；信号句与判定五问做了中文化与交底书语境适配。
  - 多模型共识分流、改名vs定义决策树、防虚构条款、人工三问、回检验收：改编自专利①案件 `6_验证\防御性表达审查\防御性表达审查方案.md`（本项目自产，2026-10-04 会话成果；提示词模板已占位化去领域词）。
- **references/docx-format.md 与模板终态结构**：格式参数与章节结构来自专利① v0.10 用户确认终态；管线含专利②（20261003_153848 任务）的 postcheck/视觉抽查/双读核验实践。
- 文风规则（括号密度/破折号/自创词/纯数字编号等）：来自用户在专利①会话（sess_76fa75cc）中的逐轮修改意见，归档于任务 20261004_160811 的 `1_问题清单\问题分类清单.md`。

## v1.2 对齐金标准的依据（2026-10-04 晚，任务 20261004_194312）

- 骨架/模板结构口径对齐专利①案件（20261003_151743）现行版 v0.12（`4_交付物`；用户指定的 v0.11 已被该案会话以 v0.12 覆盖并登记事故）。
- generate.js v5.1 两项改进源自专利②案件（20261003_153848）实战：标题 keepNext（该案曾以 python-docx 后处理 23 个标题段，见其 `8_验证\视觉审查结论.md`）；LaTeX 符号映射（该案曾因 \sum/\times 直通英文字面词人工改写）。
- 两子代理对比结论存档于任务 20261004_194312 的 `1_证据\`。

## v2.0 新增内容的来源（2026-10-06，任务 20261006_192306_批注对照与双模板）

- **B版（自由版）**（`assets/交底书骨架_自由版.md`＋`references/disclosure-template-b.md`）：**原创设计**，无上游来源——用户决策（"一版保底、一版发挥 AI 主动性；B 版只保字体字号等形式＋一级标题，放结构保安全红线；每案必问"）。保留层红线清单整理自本 skill 既有规则（v1.1 防御性写作/法定要件/排版硬规则），非新增外部内容。
- 版次选择机制（intake 必问）、self-check〔通用〕/〔A〕标注：原创。
- 同任务产出的《批注对照表》（该任务 `1_批注对照\`）为两案 docx 用户批注的抽取与对照，采纳项已落入 B 版保留层（共同红线）。

## 原创部分（无上游对应）
- `references/domain-intake.md`：案件文件夹外接参考机制（三目录约定、《参考专利索引.md》规范、用途三分类、降级路径）。
- `assets/` 骨架文件、`agents/openai.yaml`、`README.md`。

## 版本沿革（v2.2 起全量版本记录在此；此前自 README 迁入）

- **v2.2**（2026-10-07，三模型交叉审查后精简）：经 ai-cross 三厂商盲验（GLM5.3／Kimi K3／DeepSeek v4-pro，留痕 `project_项目\.dispatch\20261007-*`）定位"轻度臃肿＋规则多处落位失同步"。修复 5 处失同步：①红字四类口径（SKILL 硬规则6／workflow Step 8.3／scripts README 三处补齐【提示】第四类，权威定义在 docx-format §4）；②破折号统一"禁 3 连及以上'—'字符"（defensive-writing §1.1 精确化，对齐 self-check §6 与 B 版保留层既有口径）；③domain-intake 清除 v1.3 遗留 Fk／逐特征比对旧口径（§3 用途枚举、§5 降级表两处）；④头部字段表述统一"申请人/发明人"（self-check §6、disclosure-template 头部两处）；⑤README 版本号 v1.1→v2.2、文件清单补 B 版两文件。瘦身：删 docx-format §0 历史叙事；generate.js 头注压缩（演化史归本节）；scripts README 去数值双源（数值唯一依据 docx-format §2）；README 版本记录全量迁本节。中风险引用化（B 版保留层、workflow 成文纪律段、模板文风段复述等）未动，待使用反馈再定。
- **v2.1**（2026-10-07，用户勾选批注采纳）：批注对照表 R1/R3/R4/R5/R6/R8/R9 采纳、R2/R7 不采纳。落位：**R1** D1 后区别段（两段约 1:1、区别段≤其 2/3）进 1.1 规则＋B版保留层；**R3** 用词替换表（同族/显式留痕/消费/业务，开放清单）进 defensive-writing §1.1＋自检机械项；**R4** 距离单位默认 km（<1km 才用 m）；**R5** 书写者提醒红字化——`【提示：…】`新标记（generate.js 识别＋docx-format 红字第四类＋骨架占位改写）；**R6** 关键点尾注只到章/步骤号一级（防重复堆叠）；**R8** 3.4 前置与主链间过渡句（仅 A 版，纯结构项）；**R9** 附图图元不重叠＋附图多模态视觉核图（docx-format＋workflow Step 8）。R1/R3/R4/R5/R6/R9 六项入共同红线层（A/B 同守）。
- **v2.0**（2026-10-06，任务 20261006_192306_批注对照与双模板）：**双版底层模板**——A 对齐版（原骨架/模板，结构对齐真实案件终态，保底）＋B 自由版（新增 `assets/交底书骨架_自由版.md`＋`references/disclosure-template-b.md`：各章结构由会话自行组织，仅守安全红线层）。格式层（generate.js）两版共用不分叉；**版次在 intake 每案必问**（workflow Step 1）；self-check 逐项标注〔通用〕（红线，两版同守）／〔A〕（结构，仅对齐版）。
- **v1.4**（2026-10-05，用户点名补充）：1.1 现有技术增加**总起引言段**规则（模板规则＋骨架占位＋self-check 核对项三处）——先几句话引入技术话题、再点出现有技术集中在哪些方向，随后各段逐方向展开（对齐两案最新版 v0.12/v1.0 实际结构；该意见源自专利① v0.5→v0.6 轮"1.1加总分引言段"，v1.1 吸收时遗漏，本次补上）。
- **v1.3**（2026-10-05，用户点名删除）：移除"逐特征比对表＋特征一览"机制（骨架/模板/自检/流程/domain-intake 五处；v2.2 复查时发现 domain-intake 两处未清净，已补清）——用户已在案件后续版本删除该两部分，skill 对齐其终态偏好；1.1 的 D1 保持一段话介绍，区别特征承载改为 6.1 纯数字编号＋三段绑定推理。
- **v1.2**（2026-10-04 晚，任务 20261004_194312_专利skill对齐金标准）：对齐专利①现行版（金标准）——①骨架三处结构缺陷修复：章节标题不再携带"（≤6条）（≤2个）"模板提示语、附图说明/参考文献定为三级标题挂七章后、实施例小节带 7.x 节号；②头部信息表字段集对齐真实代理模板（案号/交底书名称/申请人/发明人/撰写人/撰写人电话/E-mail）；③generate.js v5.1：标题段内置 keepNext 防孤行、LaTeX 符号映射扩充（Σ×≤希腊字母等，免人工改写）；④self-check §6 增"标题无提示语残留"等三项结构检查；⑤新增红线：输出件禁止用 python-docx 重存改格式（加固需求提 skill 层）。
- **v1.1**（2026-10-04，任务 20261004_160811_专利skill升级）：吸收两件真实交底书实战经验与防御性写作会话成果——①新增 defensive-writing.md（D1–D10 中文化＋改名vs定义＋多模型共识分流，审查默认必做）；②新增 docx-format.md＋scripts/docx生成（底层格式模板，杜绝两案格式不一致）；③模板对齐用户九轮修订终态（缩略语节、替代方案前移四章、逐式符号说明、数量上限、纯数字编号、图注加粗等）；④self-check 新增 §6 文风与排版专项；⑤workflow 增 Step 6.5 与 Word 修订应用流程。
- **v1.0**（2026-10-03，任务 20261003_150306_专利skill制作）：初版。

## 部署形态（2026-10-07 起）

实体安装于 skills-manager 中央仓库 `C:\Users\Akesu\.skills-manager\skills\patent-cn-disclosure\`（经 `skills-manager-cli.exe skills install --local` 登记，skill_id b8775da7-e652-4582-8653-8877a4ae0245，source_type=local；中央仓库 git 自动备份，node_modules 经 .gitignore 排除不入库）；项目 `.zcode\skills\patent-cn-disclosure` 为指向实体的 Windows junction（tag 0xA0000003）。迁移时校验：430 文件/14,060,551 字节一致、18 个正文文件 SHA256 全同、`require('docx')` 经链接实测可用。原项目实体目录改名保留为 `patent-cn-disclosure._bak_20261007`（验收后可删）。

## 对照方法
验收时逐文件比对：本表"改编来源文件 → 对应文件"左列源文件在上述本地存档中真实存在；本 skill 对应文件的关键规则（方法独权句式、三段绑定、删除测试、替代方案章节名等）应能在源文件中找到同义原文。比对记录见任务 20261003_150306 的 `1_设计\来源映射.md`。
