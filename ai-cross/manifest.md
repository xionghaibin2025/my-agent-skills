# 能力清单 manifest
盘点日期: 2026-09-26 ｜ 宿主: Kimi Code CLI（无内部通道，全部走外部命令）

| 通道 | 模型/档位 | 强项 | 相对成本 | 额度归属 | 冒烟结果 |
|---|---|---|---|---|---|
| 当前宿主 | Moonshot Kimi（当前会话模型，默认 k3-256k） | 主线程执行与独立核验 | 已有 | Kimi Code 订阅 | ✅ 当前会话即冒烟 |
| cc_switch→Moonshot Kimi / Kimi Code | kimi-for-coding-highspeed / kimi-for-coding / k3-256k | **ZCode(GLM) 做宿主时的交叉验证方**；工具型任务可用 | 低/中/高 | Kimi Code 订阅 | ✅ 2026-09-26 三档全部经 claude CLI 实测应答正确 |
| cc_switch→default | glm-5-turbo / glm-5.3 | GLM 低档抽取 / 常规实现与高档审查；工具型任务可用 | 低/高 | GLM Coding Plan | ✅ 2026-09-23 claude CLI 全链路：turbo 6.8s / 5.3 4.7s |
| cc_switch→Zhipu GLM Coding Plan / GLM-5.3 + Vision MCP | glm-5-turbo / glm-5.3 | 同上 | 低/高 | GLM Coding Plan | ✅ 2026-09-23 与 default 同 key 同端点 |
| cc_switch→Zhipu GLM Coding Plan / GLM-5.3-Flash | glm-5.3-flash 全档 | 低档批量任务的备选 | 低 | GLM Coding Plan | ✅ 2026-09-23 实测应答正确 |
| 裸 API 直调→GLM 端点（key 存 `GLM_CODING_KEY`） | glm-5-turbo / glm-5.3 | 纯文本批量任务的更省通道 | 低/高 | GLM Coding Plan | ✅ 2026-09-23 服务端真身一致 |
| 裸 API 直调→Kimi 端点（key 存 `KIMI_API_KEY`） | k3-256k 等 | 纯文本任务；OpenAI 格式 `/coding/v1/chat/completions` 亦可用 | 低/高 | Kimi Code 订阅 | ✅ 2026-09-26 |
| Codex CLI | — | — | — | — | ❌ 用户已退订（2026-09-23 申报）；CLI 未安装 |
| Antigravity（Gemini） | — | — | — | Google 账号登录 | ❌ 不可派发：桌面 IDE，其 `antigravity-ide` CLI 仅为 IDE 启动器，无无头模式 |

## 厂商 × 档位矩阵（路由查这张表）

| 厂商 | 低档 | 中档 | 高档 |
|---|---|---|---|
| Moonshot（宿主或 cc_switch→Kimi Code） | kimi-for-coding-highspeed | kimi-for-coding | k3-256k |
| 智谱（cc_switch→default 或裸 API） | glm-5-turbo / glm-5.3-flash | glm-5.3 | glm-5.3 |

**宿主配对规则**：宿主是 Kimi Code → 交叉验证派 GLM；宿主是 ZCode/GLM → 交叉验证派 Kimi。两个方向均已实测可用。

## 源与强度解锁

当前可用独立厂商数：2（Moonshot + 智谱 GLM），**双向可派发** → 分层省额度 ✅ ｜ 跨厂商交叉验证 ✅（无论宿主是哪边）｜ 全力模式未请求。

- 纯文本任务：`cc_switch.py exec --tools ""` 或裸 API 直调。
- 工具型任务：`cc_switch.py exec`（claude CLI 2.1.280 原生版，`~/.local/bin/claude.exe`，SHA256 与 Anthropic 签名已验证）。

## 派发命令模板

```bash
# GLM（Kimi Code 做宿主时的交叉验证方）
python references/cc_switch.py exec --provider "default" --tier sonnet --task-file task.txt --usage
# Kimi（ZCode/GLM 做宿主时的交叉验证方）
python references/cc_switch.py exec --provider "Moonshot Kimi / Kimi Code" --tier opus --task-file task.txt --usage
# 纯文本最省模式（禁用全部工具）加 --tools ""
```

注意：Git Bash 中需 `export PATH="$HOME/.local/bin:$PATH"` 让 `cc_switch.py` 找到 claude（已实测）。

## ⚠️ 关键架构事实（2026-09-26 查明）

**claude CLI 2.1.280 的配置优先级：`~/.claude/settings.json` 的 env > 进程环境变量。** settings.json 里的 `ANTHROPIC_BASE_URL` 曾把 cc_switch 注入的 Kimi 端点劫持到 GLM，报 1211「模型不存在」（该错误来自 GLM，不是 Kimi）。已于 2026-09-26 将 settings.json 清空为中性载体（仅保留 zai-mcp 用的 `Z_AI_API_KEY`/`Z_AI_MODE`），备份在 `~/.claude/settings.json.bak-aicross-20260926`。**今后任何工具往 settings.json 写回 ANTHROPIC_BASE_URL，cc_switch 的非 GLM 派发都会被静默劫持——复发时先查这里。**

**Kimi 端点（api.kimi.com/coding）的怪癖**：裸 HTTP Anthropic 路径（/v1/messages）对**任意模型名都回显 200**（`nonexistent-xyz` 也"OK"），服务端真身校验在该路径失效；官方真实模型 ID 以 `~/.kimi-code/config.toml` 为准（`k3-256k` / `kimi-for-coding` / `kimi-for-coding-highspeed`）。诊断 Kimi 通道故障时，裸 curl 的 200 不能作为可用性证据，必须走 claude CLI 路径实测。

## 模型漂移备注

- 2026-09-26 新增 Kimi 档位（经 claude CLI 全链路实测）：`kimi-for-coding-highspeed`（低/高速）、`kimi-for-coding`（中/K2.7 Code）、`k3-256k`（高/K3 旗舰，官方客户端当前默认）。
- 2026-09-23 实测（GLM 端点直打，比对响应体 model 字段）：`glm-5-turbo` ✅、`glm-5.3` ✅；`glm-5.3[1m]`、`glm-5.3[1M]` HTTP 400 不存在（1211）；`glm-5.3-flash` ✅ 存在且含于套餐；`glm-5.3-flashx` 不在套餐内（429/1311）；`glm-5-flash` 不存在。
- 2026-08-25 实测：`glm-5.2` 被服务端静默迁移为 `glm-5.3`，不得作为配置值。
- GLM 冒烟细节：`glm-5.3` 在 max_tokens=16 下返回空文本（思考占满输出预算），属正常现象。

## 维护记录

- 2026-09-26：修复 ZCode 会话盲验 glm-5.3 超时事件（ZCode 会话 `sess_c5f4c22c` 在 180s 处被 cc_switch 杀掉）。**根因定案：glm-5.3 深思考跑长报告类任务实测需 200-250s（复现：16.7k output 用时 241s），默认 180s 超时偏紧属误杀**；debug 日志证实 claude CLI 全程只访问目标端点、无境外遥测请求，与网络/代理无关。修复：`cc_switch.py` 默认 `--timeout` 180→300，超时提示改写（长任务优先 `--timeout 400` 重试），并为子进程追加 `DISABLE_TELEMETRY`/`DISABLE_ERROR_REPORTING`/`DISABLE_AUTOUPDATER`/`DISABLE_NON_ESSENTIAL_MODEL_CALLS` 防挂起保险。修复后冒烟 8s 正常。已同步至 ZCode 侧副本 `~/.zcode/skills/ai-cross/`（该副本与主副本 `~/.agents/skills/ai-cross-main/` 是**两份独立拷贝**，改动需双向同步）。
- 2026-09-26：新增 Kimi Code 通道（key 存用户级环境变量 `KIMI_API_KEY` + cc-switch provider「Moonshot Kimi / Kimi Code」，db 备份 `cc-switch.db.bak-20260926`）；查明并修复 settings.json env 劫持进程环境变量的问题（见「关键架构事实」）。
- 2026-09-23：claude CLI 经 npm 全局安装反复损坏（静默空转、解包残缺），最终改用官方下载服务器手动安装原生二进制。**根因当日查明：火绒 HIPS 有专门针对 Claude Code 的行为拦截规则（`Software:OS/Claude.A`），node 解包 claude.exe 时被内核层强杀。用户当日卸载火绒后 npm 恢复正常。今后若重装安全软件，npm 装包静默失败时优先排查同类拦截。**
- 2026-09-23：cc-switch db 备份 `cc-switch.db.bak-20260923`（含旧失效 key）、`cc-switch.db.bak-20260923-2`；修复 cc-switch 里 `ANTHROPIC_MODEL`/`FABLE` 的 `[1m]` 变体与 `Z_AI_API_KEY` 旧 key。
- claude.exe 首次运行需一次性初始化，首次 `claude -p` 可能超过 180s；之后单次纯文本调用约 5–8s。
