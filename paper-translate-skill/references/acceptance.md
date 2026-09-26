# 统一验收与报告

脚本跑完、文件生成、甚至译文写完都不是成功。交付前必须核对 `验收.json` 与实际文件，按以下分面报告；降级原样保留，不得升级。

## 八个分面

| 分面 | 必查事实 | 取值来源 |
|---|---|---|
| `overall` | `complete / degraded / failed / 待用户` | 其余分面汇总 |
| `identity` | 双语 MD 头部 DOI/标题与源 PDF（或 paper-fetch 规范身份）一致 | merge_verify 注入的 front matter |
| `coverage` | 英文引用块:中文段落配对率、章节覆盖（摘要→结论/方法主体） | merge_verify 统计 |
| `figure` | 图号一一对应、断链 = 0、每图有对照验收记录 | merge_verify + 渲染报告附表 |
| `formula` | `$$` 公式数、"待确认"标记数 | merge_verify 统计 |
| `refs` | 保留文献条数 vs 原文（完整保留或如实声明节选） | merge_verify + 宿主计数 |
| `asset` | 补充材料归档状态与缺失清单 | paper-fetch acceptance / 归档清单复用（入口 A）/ 未获取（入口 B 委托失败）或用户未要求 |
| `output` | 交付文件与说明文件一一对应、路径有效 | 目录核对 |

判定规则：

- 任一分面为 degraded/failed 时 `overall` 不得是 complete。
- 常见 degraded 来源：待确认公式 >0、补充材料未获取、某图坐标覆盖而非自动定位、文献节选。
- `coverage` 配对率 <98% 或断链 >0：不算降级，直接打回修复（failure-handling），修复前不得交付。

## merge_verify 输出核对

`验收.json` 之外还要人工确认三件事（脚本测不到）：

1. 抽 1–2 段译文与源 PDF 原文逐句对照，翻译无串段、无漏句；
2. 截图在译文中的插入位置与原文章节流一致；
3. front matter 的底本路径、DOI 与实际使用文件一致。

## 最终报告

单篇：

```
<论文名>：overall=<结论>
  产物：<双语MD路径>（配对率 x/x，公式 N 处[待确认 M]，文献 N 条）
  截图：N 张全部对照验收通过 / 其中 K 张为坐标覆盖
  补充材料：已归档 M 个文件 / 未获取（原因）
  降级项：<列表，无则省略>
```

批量：附 `进度.json` 汇总表（原始 index → 论文 → 终态），汇总 complete/degraded/failed/待用户 数量；未完成项列出卡住的阶段与原因。

报告后如需继续（重译、补图、补材料），按预设 4 修复续跑，不整篇重做。
