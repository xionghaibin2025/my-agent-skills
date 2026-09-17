# 能力清单 manifest
盘点日期: 2026-08-25 ｜ 宿主: Codex

| 通道 | 模型/档位 | 强项 | 相对成本 | 额度归属 | 冒烟结果 |
|---|---|---|---|---|---|
| 当前宿主 | OpenAI Codex | 主线程执行与独立核验 | 已有 | Codex | ✅ 当前会话 |
| cc_switch→default | glm-5-turbo / glm-5.3 | GLM 低档抽取 / 常规实现与高档审查 | 低/高 | GLM Coding Plan | ✅ 2026-08-25，服务端真身一致 |
| cc_switch→Zhipu GLM Coding Plan / GLM-5.3 + Vision MCP | glm-5-turbo / glm-5.3 | GLM 低档抽取 / 常规实现与高档审查 | 低/高 | GLM Coding Plan | ✅ 2026-08-25，服务端真身一致 |

## 厂商 × 档位矩阵（路由查这张表）

| 厂商 | 低档 | 中档 | 高档 |
|---|---|---|---|
| OpenAI（当前宿主） | — | — | 当前会话模型 |
| 智谱（cc_switch→default） | glm-5-turbo | glm-5.3 | glm-5.3 |

## 源与强度解锁

当前任务可用独立厂商数：2（OpenAI 宿主 + 智谱 GLM）→ 分层省额度 ✅ ｜ 跨厂商交叉验证 ✅ ｜ 全力模式未请求。

## 模型漂移备注

- 当前端点实测仅采用精确 ID `glm-5-turbo` 与 `glm-5.3`。
- `glm-5.2` 会被服务端静默迁移为 `glm-5.3`，不得继续作为配置值。
- `glm-5.2[1m]`、`glm-5.3[1m]` 与大写 `[1M]` 变体均返回模型不存在，不用于派发。
