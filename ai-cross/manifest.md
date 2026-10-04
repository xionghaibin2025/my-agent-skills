# 能力清单 manifest
盘点日期: 2026-10-04 ｜ 宿主: Kimi Code CLI（无内部通道，全部走外部命令）

| 通道 | 模型/档位 | 强项 | 相对成本 | 额度归属 | 冒烟结果 |
|---|---|---|---|---|---|
| 当前宿主 | Moonshot Kimi（当前会话模型，默认 k3-256k） | 主线程执行与独立核验 | 已有 | Kimi Code 订阅 | ✅ 当前会话即冒烟 |
| cc_switch→Moonshot Kimi / Kimi Code | kimi-for-coding-highspeed / kimi-for-coding / k3-256k | **ZCode(GLM) 做宿主时的交叉验证方**；工具型任务可用 | 低/中/高 | Kimi Code 订阅 | ✅ 2026-09-26 三档全部经 claude CLI 实测应答正确 |
| cc_switch→default | glm-5-turbo / glm-5.3 | GLM 低档抽取 / 常规实现与高档审查；工具型任务可用 | 低/高 | GLM Coding Plan | ✅ 2026-09-23 claude CLI 全链路：turbo 6.8s / 5.3 4.7s |
| cc_switch→Zhipu GLM Coding Plan / GLM-5.3 + Vision MCP | glm-5-turbo / glm-5.3 | 同上 | 低/高 | GLM Coding Plan | ✅ 2026-09-23 与 default 同 key 同端点 |
| cc_switch→Zhipu GLM Coding Plan / GLM-5.3-Flash | glm-5.3-flash 全档 | 低档批量任务的备选 | 低 | GLM Coding Plan | ✅ 2026-09-23 实测应答正确 |
| 裸 API 直调→GLM 端点（key 存 `GLM_CODING_KEY`） | glm-5-turbo / glm-5.3 | 纯文本批量任务的更省通道 | 低/高 | GLM Coding Plan | ✅ 2026-09-23 服务端真身一致 |
| 裸 API 直调→Kimi 端点（key 存 `KIMI_API_KEY`） | k3-256k 等 | 纯文本任务；OpenAI 格式 `/coding/v1/chat/completions` 亦可用 | 低/高 | Kimi Code 订阅 | ✅ 2026-09-26 |
| cc_switch 自定义端点→DeepSeek（key 存 `DEEPSEEK_API_KEY`） | deepseek-flash / deepseek-v4-pro | 跨厂商交叉验证新成员；flash 支持图片输入 | 低/高 | DeepSeek 按量 API | ✅ 2026-10-04 端点枚举 + 真身比对 + claude CLI 全链路（4.4s） |
| cc_switch 自定义端点→小米 MiMo（key 存 `MIMO_API_KEY`） | mimo-v2.6-flash / mimo-v2.6-pro | 跨厂商交叉验证新成员 | 低/高 | 小米 MiMo 平台（额度形态以控制台为准） | ✅ 2026-10-04 端点枚举 + 真身比对 + claude CLI 全链路（8.8s） |
| 裸 API 直调→DeepSeek / MiMo（OpenAI 兼容） | 同上 | 纯文本任务最省通道（地板 ~11 token） | 低/高 | 同上 | ✅ 2026-10-04 `GET /v1/models` 枚举成功 |
| Codex CLI | — | — | — | — | ❌ 用户已退订（2026-09-23 申报）；CLI 未安装 |
| Antigravity（Gemini） | — | — | — | Google 账号登录 | ❌ 不可派发：桌面 IDE，其 `antigravity-ide` CLI 仅为 IDE 启动器，无无头模式 |

## 厂商 × 档位矩阵（路由查这张表）

| 厂商 | 低档 | 中档 | 高档 |
|---|---|---|---|
| Moonshot（宿主或 cc_switch→Kimi Code） | kimi-for-coding-highspeed | kimi-for-coding | k3-256k |
| 智谱（cc_switch→default 或裸 API） | glm-5-turbo / glm-5.3-flash | glm-5.3 | glm-5.3 |
| DeepSeek（cc_switch 自定义端点或裸 API） | deepseek-flash | deepseek-flash | deepseek-v4-pro |
| 小米 MiMo（cc_switch 自定义端点或裸 API） | mimo-v2.6-flash | mimo-v2.6-flash | mimo-v2.6-pro |

**宿主配对规则**：宿主是 Kimi Code → 交叉验证首选 GLM，亦可派 DeepSeek / MiMo；宿主是 ZCode/GLM → 交叉验证派 Kimi / DeepSeek / MiMo。Kimi↔GLM 两个方向均已实测可用；DeepSeek、MiMo 已实测可被 Kimi Code 宿主派发。

## 源与强度解锁

当前可用独立厂商数：4（Moonshot + 智谱 GLM + DeepSeek + 小米 MiMo）→ 分层省额度 ✅ ｜ 跨厂商交叉验证 ✅（4 选 2，可组 6 对）｜ 全力模式可用（4 厂商 × 多档）。

- 纯文本任务：`cc_switch.py exec --tools ""` 或裸 API 直调。
- 工具型任务：`cc_switch.py exec`（claude CLI 2.1.280 原生版，`~/.local/bin/claude.exe`，SHA256 与 Anthropic 签名已验证）。

## 派发命令模板

```bash
# GLM（Kimi Code 做宿主时的交叉验证方）
python references/cc_switch.py exec --provider "default" --tier sonnet --task-file task.txt --usage
# Kimi（ZCode/GLM 做宿主时的交叉验证方）
python references/cc_switch.py exec --provider "Moonshot Kimi / Kimi Code" --tier opus --task-file task.txt --usage
# DeepSeek（自定义端点模式，key 存用户级环境变量 DEEPSEEK_API_KEY）
python references/cc_switch.py exec --endpoint https://api.deepseek.com/anthropic \
  --key-env DEEPSEEK_API_KEY --model deepseek-flash --task-file task.txt --usage
# 小米 MiMo（key 存 MIMO_API_KEY）
python references/cc_switch.py exec --endpoint https://api.xiaomimimo.com/anthropic \
  --key-env MIMO_API_KEY --model mimo-v2.6-flash --task-file task.txt --usage
# 纯文本最省模式（禁用全部工具）加 --tools ""
```

**需要子代理亲自跑命令取证时**（2026-09-27 Kimi K3 核验事件后新增，缺一不可）：

```bash
python references/cc_switch.py exec --provider "..." --tier ... --task-file task.txt \
  --tools "Read,Glob,Grep,Bash" \
  --add-dir "D:\要访问的目录,C:\另一个目录" \
  --full-perms --usage --timeout 400
```

- `--tools` 必须显式含 `Bash`（默认白名单只有 Read/Grep/Glob，Bash 根本不注册）；
- `--add-dir` 放行工作目录之外的路径（文件类工具默认只放行 cwd，碰别的盘符一律拒绝）；
- `--full-perms` 跳过权限询问（无人值守 `-p` 会话没人能点批准，Bash 命令会全部卡死在 requires approval）；`--tools` 注册层护栏仍然生效。
- 替代姿势（更省、隔离更好）：**编排者自己采集原始输出落盘 → 子代理只做盲分析**（Read 工作区内证据文件）→ 编排者脚本复核其判定表。纯文本通道即可，无权限问题。

注意：Git Bash 中需 `export PATH="$HOME/.local/bin:$PATH"` 让 `cc_switch.py` 找到 claude（已实测）。

## ⚠️ 关键架构事实（2026-09-26 查明）

**claude CLI 2.1.280 的配置优先级：`~/.claude/settings.json` 的 env > 进程环境变量。** settings.json 里的 `ANTHROPIC_BASE_URL` 曾把 cc_switch 注入的 Kimi 端点劫持到 GLM，报 1211「模型不存在」（该错误来自 GLM，不是 Kimi）。已于 2026-09-26 将 settings.json 清空为中性载体（仅保留 zai-mcp 用的 `Z_AI_API_KEY`/`Z_AI_MODE`），备份在 `~/.claude/settings.json.bak-aicross-20260926`。**今后任何工具往 settings.json 写回 ANTHROPIC_BASE_URL，cc_switch 的非 GLM 派发都会被静默劫持——复发时先查这里。**

**Kimi 端点（api.kimi.com/coding）的怪癖**：裸 HTTP Anthropic 路径（/v1/messages）对**任意模型名都回显 200**（`nonexistent-xyz` 也"OK"），服务端真身校验在该路径失效；官方真实模型 ID 以 `~/.kimi-code/config.toml` 为准（`k3-256k` / `kimi-for-coding` / `kimi-for-coding-highspeed`）。诊断 Kimi 通道故障时，裸 curl 的 200 不能作为可用性证据，必须走 claude CLI 路径实测。

## 模型漂移备注

- 2026-10-04 新增 DeepSeek 与小米 MiMo（各自 `GET /v1/models` 枚举核实）：DeepSeek 当前仅 `deepseek-flash`（V4.1-Flash，支持图片输入）与 `deepseek-v4-pro`，旧 ID `deepseek-chat`/`deepseek-reasoner` 已不在枚举中；MiMo 文本型号 `mimo-v2.6-flash` / `mimo-v2.6-pro` / `mimo-v2.6-pro-ultraspeed`（上一代 `mimo-v2.5`/`mimo-v2.5-pro` 仍在），`mimo-v2.5-asr`/`mimo-v2.5-tts*` 为语音型号勿用于文本派发。两家 Anthropic 端点均如实回显请求 model，无静默降级。

- 2026-09-26 新增 Kimi 档位（经 claude CLI 全链路实测）：`kimi-for-coding-highspeed`（低/高速）、`kimi-for-coding`（中/K2.7 Code）、`k3-256k`（高/K3 旗舰，官方客户端当前默认）。
- 2026-09-23 实测（GLM 端点直打，比对响应体 model 字段）：`glm-5-turbo` ✅、`glm-5.3` ✅；`glm-5.3[1m]`、`glm-5.3[1M]` HTTP 400 不存在（1211）；`glm-5.3-flash` ✅ 存在且含于套餐；`glm-5.3-flashx` 不在套餐内（429/1311）；`glm-5-flash` 不存在。
- 2026-08-25 实测：`glm-5.2` 被服务端静默迁移为 `glm-5.3`，不得作为配置值。
- GLM 冒烟细节：`glm-5.3` 在 max_tokens=16 下返回空文本（思考占满输出预算），属正常现象。

## 维护记录

- 2026-10-04：接入 DeepSeek 与小米 MiMo 两家按量 API。key 经 `setx` 存为用户级环境变量 `DEEPSEEK_API_KEY` / `MIMO_API_KEY`（注意 setx 不作用于已打开的 shell）。`cc_switch.py` 新增**自定义端点模式**（`--endpoint URL --key-env ENVVAR --model ID`，不经 cc-switch db，其余护栏不变），以容纳不在 cc-switch 里的 key。两家均完成：①端点枚举 ②`/v1/messages` 真身比对（响应 model 与请求一致）③claude CLI 全链路冒烟（DeepSeek 4.4s / MiMo 8.8s）。独立厂商数 2→4。另查明本机 `~/.kimi-code`、`~/.zcode`、`~/.claude` 下的三份 `skills/ai-cross/` 实为**同一文件的链接**（cp 报 same file），改一处即处处生效，无同步负担。

- 2026-09-27：修复"取证类派发两次全灭"问题（Kimi K3 核验 Inkscape 安装事件，留痕 `E:\2_AI工作区\agent\zcode\project_杂\.dispatch\2026092*-ccswitch-kimi-k3-verify*.md`）。**根因两层**：① cc_switch 默认 `--tools Read,Grep,Glob` 不含 Bash，子代理无法执行命令（R1）；② 显式加 Bash 后仍全灭——claude CLI 文件类工具默认只放行会话 cwd（Glob/Read 碰 D:\ C:\ 全拒），且 `-p` 无人值守会话的 permission prompt 无人应答，Bash 命令全部卡死在 requires approval（R2）。**修复**：cc_switch.py 新增 `--add-dir`（逐目录放行）与 `--full-perms`（附加 --dangerously-skip-permissions；--tools 注册层护栏仍压得住它）。低档 glm-5-turbo 冒烟一次通过（Bash 访问 D: + Read 访问 cwd 外 C: 文件均成功）。R3 用"编排者采集证据落盘 → K3 盲分析 → 脚本复核判定表"完成闭环，该姿势保留为取证类派发的推荐替代。另查明：`~/.agents/skills/ai-cross-main/` 主副本已不存在，现仅剩 `~/.zcode/skills/ai-cross/` 一份，无双向同步负担。
- 2026-09-26：修复 ZCode 会话盲验 glm-5.3 超时事件（ZCode 会话 `sess_c5f4c22c` 在 180s 处被 cc_switch 杀掉）。**根因定案：glm-5.3 深思考跑长报告类任务实测需 200-250s（复现：16.7k output 用时 241s），默认 180s 超时偏紧属误杀**；debug 日志证实 claude CLI 全程只访问目标端点、无境外遥测请求，与网络/代理无关。修复：`cc_switch.py` 默认 `--timeout` 180→300，超时提示改写（长任务优先 `--timeout 400` 重试），并为子进程追加 `DISABLE_TELEMETRY`/`DISABLE_ERROR_REPORTING`/`DISABLE_AUTOUPDATER`/`DISABLE_NON_ESSENTIAL_MODEL_CALLS` 防挂起保险。修复后冒烟 8s 正常。已同步至 ZCode 侧副本 `~/.zcode/skills/ai-cross/`（该副本与主副本 `~/.agents/skills/ai-cross-main/` 是**两份独立拷贝**，改动需双向同步）。
- 2026-09-26：新增 Kimi Code 通道（key 存用户级环境变量 `KIMI_API_KEY` + cc-switch provider「Moonshot Kimi / Kimi Code」，db 备份 `cc-switch.db.bak-20260926`）；查明并修复 settings.json env 劫持进程环境变量的问题（见「关键架构事实」）。
- 2026-09-23：claude CLI 经 npm 全局安装反复损坏（静默空转、解包残缺），最终改用官方下载服务器手动安装原生二进制。**根因当日查明：火绒 HIPS 有专门针对 Claude Code 的行为拦截规则（`Software:OS/Claude.A`），node 解包 claude.exe 时被内核层强杀。用户当日卸载火绒后 npm 恢复正常。今后若重装安全软件，npm 装包静默失败时优先排查同类拦截。**
- 2026-09-23：cc-switch db 备份 `cc-switch.db.bak-20260923`（含旧失效 key）、`cc-switch.db.bak-20260923-2`；修复 cc-switch 里 `ANTHROPIC_MODEL`/`FABLE` 的 `[1m]` 变体与 `Z_AI_API_KEY` 旧 key。
- claude.exe 首次运行需一次性初始化，首次 `claude -p` 可能超过 180s；之后单次纯文本调用约 5–8s。
- 2026-10-02：ZCode 后台 shell（Bash run_in_background）经 cc_switch 派发 k3-256k 报 `[claude-code:unrecognized_model]`+exit 0xC0000409，同参数前台调用正常（探针实测 4 组全过）。**规避：cc_switch 派发一律前台运行。** 另：要求子代理自跑 geopandas 多轮取证的审查任务 500s 超时，改 R3 姿势（编排者采集证据落盘→子代理纯 Read 盲分析，484s 完成）更稳更快。
- 2026-10-03：cc_switch.py 在 Kimi Code 宿主派发成功但**收尾写 stdout 时报 UnicodeEncodeError（GBK 无法编码 '²'），子代理结果全文丢失**（exit 1、.out 0 字节）。根因：Kimi Code 的 Bash 调用 python 时未带 UTF-8 环境变量，stdout 按 GBK。**规避：Kimi Code 宿主下派发必须前置 `export PYTHONIOENCODING=utf-8 PYTHONUTF8=1`**（该变量组此前已在 ZCode 侧任务书中验证）。重试 488s 成功。另注：Kimi Code 宿主后台 Bash 派发 k3-256k 实测正常（ZCode 的 bg 问题未复现）。
