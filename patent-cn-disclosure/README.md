# patent-cn-disclosure

中国发明专利《技术交底书》＋《权利要求草稿》撰写 skill。实体安装于 skills-manager 中央仓库（`C:\Users\Akesu\.skills-manager\skills\patent-cn-disclosure\`，skill_id b8775da7），项目 `.zcode/skills/` 内以 Windows junction 链接部署，ZCode 自动发现。当前版本 **v2.2**。

## 定位与两层结构

- **通用层（本目录）**：撰写流程、交底书模板、权利要求规则、文风与防御性写作规则、自检清单、Word 底层格式模板。跨领域通用，**零领域词汇**。
- **案件层（外接）**：领域知识放案件文件夹（`1_案件材料/`、`2_参考专利/`＋《参考专利索引.md》、`3_参考交底书/`），见 `references/domain-intake.md`。

## 文件清单

| 文件 | 用途 |
|---|---|
| SKILL.md | 入口：触发、交付物、路由表、十条硬规则 |
| references/domain-intake.md | 案件文件夹约定＋参考专利索引＋降级路径（开工必读） |
| references/workflow.md | 案件八步流程（含 Step 6.5 防御性表达审查·默认必做） |
| references/disclosure-template.md | 交底书终态结构模板·A 对齐版（缩略语节/替代方案四章/6.1技术特征关键点/数量上限/文风规则） |
| references/disclosure-template-b.md | 交底书模板·B 自由版（放结构、保安全红线保留层） |
| references/defensive-writing.md | 防御性写作：黑话改名vs定义＋过度防御 D1–D10 中文化＋多模型共识分流审查（提示词/派发/合并/回检） |
| references/claims-guide.md | 权利要求草稿规则（纯数字编号、方法独权句式、从属树、体例硬规则） |
| references/self-check.md | 交付自检 §1–§6（含文风与排版专项：括号密度/破折号/OMML/红字清零） |
| references/docx-format.md | Word 格式规格＋优先级（参考模板＞底层模板＞禁裸pandoc）＋生成管线＋红字两阶段＋Word修订应用 |
| scripts/docx生成/ | 底层模板执行器 generate.js（v5 通用版）＋node_modules(docx@9)＋README |
| assets/交底书骨架.md、交底书骨架_自由版.md、权利要求骨架.md | 起步骨架（A 对齐版／B 自由版／权利要求） |
| NOTICE.md | 衍生与致谢声明＋版本沿革（v2.2 起全量版本记录在此） |

## 使用方法

1. 案件文件夹按 domain-intake §2 建三目录＋《参考专利索引.md》。
2. 说"写交底书"触发；走 workflow 八步（防御性审查默认必做）。
3. Word 用 `node scripts/docx生成/generate.js 〈md〉 [-i 附图目录]` 生成（格式统一，红字两阶段）。

## 版本记录

- **v2.2**（2026-10-07）：三模型交叉审查（ai-cross：GLM5.3／Kimi K3／DeepSeek v4-pro）后的口径统一与精简——修复 5 处规则失同步（红字四类、破折号禁3连、domain-intake Fk 残留、头部字段、本 README 版本号与清单），删 docx-format §0、压缩 generate.js 头注、格式数值归一 docx-format §2、版本记录全量迁 NOTICE。详情见 `NOTICE.md`《版本沿革》。
- v1.0–v2.1 全量版本记录见 `NOTICE.md`《版本沿革》。

## 边界（不做什么）

不执行联网查新检索（接入已有成果）；不产正式申请文件四件套；不做实用新型/外观设计。除 `scripts/docx生成/generate.js` 外不带可执行脚本；附图 PNG 由案件会话自产（黑白线图规范见 docx-format）。

## 维护

改动须同步更新 NOTICE.md 对照关系与任务记录；generate.js 格式常量改动须在 docx-format.md §2 同步并有案件验证依据；上游来源仓库更新不自动跟进。
