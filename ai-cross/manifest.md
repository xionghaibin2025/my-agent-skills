# 能力清单 manifest
盘点日期: 2026-09-23 ｜ 宿主: Kimi Code CLI（无内部通道，全部走外部命令）

| 通道 | 模型/档位 | 强项 | 相对成本 | 额度归属 | 冒烟结果 |
|---|---|---|---|---|---|
| 当前宿主 | Moonshot Kimi（当前会话模型） | 主线程执行与独立核验 | 已有 | Kimi API 订阅 | ✅ 当前会话即冒烟 |
| cc_switch→default | glm-5-turbo / glm-5.3 | GLM 低档抽取 / 常规实现与高档审查；**工具型任务可用**（读文件/跑代码） | 低/高 | GLM Coding Plan | ✅ 2026-09-23 claude CLI 全链路：turbo 6.8s / 5.3 4.7s，应答正确 |
| cc_switch→Zhipu GLM Coding Plan / GLM-5.3 + Vision MCP | glm-5-turbo / glm-5.3 | 同上 | 低/高 | GLM Coding Plan | ✅ 2026-09-23 key 已同步更新（与 default 同 key 同端点） |
| 裸 API 直调→GLM 端点（key 存用户级环境变量 `GLM_CODING_KEY`） | glm-5-turbo / glm-5.3 | 纯文本批量任务的更省通道 | 低/高 | GLM Coding Plan | ✅ 2026-09-23 直打端点，服务端真身一致 |
| ~/.claude/settings.json env→GLM 端点 | glm-5-turbo / glm-5.3 | claude CLI 直接使用的默认配置 | 低/高 | GLM Coding Plan | ✅ 2026-09-23 token 已更新、[1M] 变体已清理 |
| Codex CLI | — | — | — | — | ❌ 用户已退订（2026-09-23 申报）；CLI 未安装 |
| Antigravity（Gemini） | — | — | — | Google 账号登录 | ❌ 不可派发：桌面 IDE，其 `antigravity-ide` CLI 仅为 IDE 启动器，无无头模式 |

## 厂商 × 档位矩阵（路由查这张表）

| 厂商 | 低档 | 中档 | 高档 |
|---|---|---|---|
| Moonshot（当前宿主） | — | — | 当前会话模型 |
| 智谱（cc_switch→default 或裸 API） | glm-5-turbo | glm-5.3 | glm-5.3 |

## 源与强度解锁

当前可用独立厂商数：2（Moonshot 宿主 + 智谱 GLM）→ 分层省额度 ✅ ｜ 跨厂商交叉验证 ✅ ｜ 全力模式未请求。

- 纯文本任务：走裸 API 直调（`GLM_CODING_KEY` 按进程注入）或 `cc_switch.py exec --tools ""`。
- 工具型任务（GLM 需读文件/跑代码）：走 `cc_switch.py exec`（claude CLI 2.1.280 原生版已装于 `~/.local/bin/claude.exe`，SHA256 与 Anthropic 签名均已验证）。

## 派发命令模板

```bash
# 工具型/标准派发（key 由脚本从 cc-switch db 读取注入，不进上下文）
python references/cc_switch.py exec --provider "default" --tier haiku --task-file task.txt --usage
# 纯文本最省模式（禁用全部工具）
python references/cc_switch.py exec --provider "default" --tier sonnet --task "..." --tools "" --usage
```

注意：Git Bash 中需 `export PATH="$HOME/.local/bin:$PATH"` 让 `cc_switch.py` 找到 claude（已实测）。

## 模型漂移备注

- 2026-09-23 实测（直打端点比对响应体 model 字段）：`glm-5-turbo` ✅、`glm-5.3` ✅ 服务端真身一致；`glm-5.3[1m]`、`glm-5.3[1M]` 均 HTTP 400 模型不存在（1211）——cc-switch 与 settings.json 中的 `[1m]/[1M]` 变体已全部改回 `glm-5.3`。
- 2026-08-25 实测：`glm-5.2` 被服务端静默迁移为 `glm-5.3`，不得作为配置值。
- 冒烟细节：`glm-5.3` 在 max_tokens=16 下返回空文本（思考占满输出预算），属正常现象；身份校验以响应体 model 字段为准。

## 维护记录

- 2026-09-23：claude CLI 经 npm 全局安装反复损坏（静默空转、解包残缺），最终改用官方下载服务器手动安装原生二进制；npm 全局残留已由 npm uninstall 清理。
- 2026-09-23：cc-switch db 修改前已备份至 `~/.cc-switch/cc-switch.db.bak-20260923`（含旧失效 key，用户确认无需保留后可删）。
- claude.exe 首次运行需一次性初始化，首次 `claude -p` 调用可能超过 180s；初始化完成后单次纯文本调用约 5–7s。
