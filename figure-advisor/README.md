# figure-advisor

科研配图方案顾问。根据数据的分布形状，把几种候选画法按最终尺寸实际渲染出来并排比较，再推荐表达方式、配色和组图排版。

## 功能

- **选图**：统计每组样本量、偏度、零值、离群值等形状特征，给出 2–4 种候选画法，渲染成一张对比图，附推荐理由
- **配色**：图型选定后，从 32 套精选色带中按用途选 3–4 套，套在实际图上对比，并生成色盲模拟与灰度视图
- **组图**：按整张图的主张安排子图角色，给出 2–3 种排版对比；建立全文统一的配色表
- **审图**：同时读图件和绘图代码，按主次、编码、配色、对齐、字号的顺序提出修改意见，附改后版本
- **参考图库**（可选）：为收藏的图写说明卡，记录每次选中和排除的方案，之后的推荐会参考这些记录

支持 R（ggplot2）和 Python（matplotlib），沿用项目已有的语言。不做统计检验，已有的分析结果原样使用。

仅供星球会员个人使用，请勿转发。

## 安装

把 `figure-advisor` 文件夹放到 agent 的技能目录：

| Agent | 目录 |
|---|---|
| Claude Code | `~/.claude/skills/figure-advisor`（Windows：`%USERPROFILE%\.claude\skills\figure-advisor`） |
| Codex | `~/.codex/skills/figure-advisor` |

放在项目的 `.claude/skills/` 下则只对该项目生效。

## 环境

- [uv](https://docs.astral.sh/uv/)：运行内置脚本，首次运行时自动安装所需的 Python 包
- R ≥ 4.3（ggplot2、patchwork）或 Python ≥ 3.10（matplotlib），按绘图语言二选一
- agent 需要能执行命令和查看图片；比较候选方案依赖看图

## 用法示例

- 「data.csv 里按 site 比较 Cd 含量，帮我看用什么图」
- 「这张图的配色给几套方案对比一下」
- 「Figure 3 有地图、SHAP、散点和机制示意图四个子图，帮我排版」
- 「审一下 fig2.png，绘图代码是 plot_fig2.R」

## 参考图库（可选）

图库是自己的一个文件夹，收藏的图直接放进去即可，文件名不限。设置环境变量 `FIGURE_LIBRARY` 指向它：

```powershell
# Windows，设置后重开终端生效
setx FIGURE_LIBRARY "D:\美图收集"
```

```bash
# macOS / Linux，写入 ~/.zshrc 或 ~/.bashrc
export FIGURE_LIBRARY="$HOME/美图收集"
```

也可以在项目的 AGENTS.md 或 CLAUDE.md 中写明图库路径，或在对话中直接告诉 agent。未配置时这部分功能自动跳过。

图库内的 `卡片/` 目录和 `偏好记录.md` 由 agent 按需创建：只在要求整理时写说明卡；只在明确选中或排除某个方案时记录，理由尽量用原话。收藏的图片仅供个人参考，不要随技能一起转发。

## 说明

- 内置脚本在本机运行；首次运行时 uv 需要联网下载依赖。
- 形状特征的阈值（如偏度大于 1）用于筛选候选画法，不是统计判断。
- 期刊尺寸在定稿时按目标期刊的官方作者指南核对；候选图默认按双栏 180 mm 或单栏 88 mm 渲染。
- 借鉴的方法与来源见 `references/sources.md`，第三方许可见 `THIRD_PARTY_NOTICES.md`。
