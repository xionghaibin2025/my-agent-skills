#!/usr/bin/env python3
"""
ai-cross 的 cc-switch 只读桥。两种模式：

  list                    只读列出 cc-switch 里配置的 provider（endpoint / 档位→模型映射 / 是否有 key）。
                          token 一律不输出，仅给出 has_token 标志。供主 agent 建 manifest 与路由表。

  exec --provider NAME    把该 provider 的 endpoint+token 按【进程内】注入并派发一个任务。

  exec --endpoint URL --key-env ENVVAR --model ID
                          不经 cc-switch 的自定义 Anthropic 兼容端点模式（如 DeepSeek、小米 MiMo）。
                          key 从用户级环境变量 ENVVAR 读取注入，绝不打印；--model 必填。
                          其余参数（--tools/--add-dir/--full-perms/--usage/--timeout）与 provider 模式相同。
       [--tier haiku|sonnet|opus] [--model ID] (--task "..." | --task-file PATH)
       [--tools "Read,Grep,Glob"] [--add-dir "D1,D2"] [--full-perms] [--usage]
                          任务含引号/花括号/换行时务必用 --task-file，避免跨 shell 引号被拆碎。
                          --tools：只读护栏，默认 Read,Grep,Glob；纯文本任务传 "" 禁用全部工具最省。
                          --add-dir：授权子会话访问工作目录之外的路径（文件类工具默认只放行 cwd）。
                          --full-perms：附加 --dangerously-skip-permissions，跳过权限询问——无人值守 -p
                          会话里没人能点批准，Bash 类命令不加此项会卡死在 requires approval。
                          仅用于可信本机任务（如只读取证）；--tools 白名单护栏仍然生效。
                          --usage：额外在 stderr 打印本次 token 用量与耗时（stdout 仍只有模型回答）。
                          token 只在本脚本子进程内读取、注入子进程环境，绝不打印、绝不进主 agent 上下文。
                          仅支持 app_type=claude（Anthropic 兼容端点，载体 claude CLI）；codex/gemini 官方订阅
                          直接用其自身 CLI，不经此桥。

只读打开 db，绝不修改 cc-switch 数据，绝不使用其全局切换机制。
"""
import sqlite3, os, json, sys, subprocess, argparse, shutil

DB = os.path.expanduser("~/.cc-switch/cc-switch.db")

def _conn():
    if not os.path.exists(DB):
        print(json.dumps({
            "error": "未找到 cc-switch 数据库",
            "path": DB,
            "hint": "本机可能没装 cc-switch。这不影响使用——回退到手动申报即可（见 setup.md 第 1 步）。",
        }, ensure_ascii=False))
        sys.exit(2)
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con

def _providers(con):
    ep = {}
    for r in con.execute("SELECT provider_id, url FROM provider_endpoints"):
        ep.setdefault(r["provider_id"], []).append(r["url"])
    out = []
    for r in con.execute("SELECT id, app_type, name, category, settings_config FROM providers"):
        try:
            cfg = json.loads(r["settings_config"])
        except Exception:
            cfg = {}
        env = cfg.get("env", {}) if isinstance(cfg, dict) else {}
        tier = {
            "haiku": env.get("ANTHROPIC_DEFAULT_HAIKU_MODEL"),
            "sonnet": env.get("ANTHROPIC_DEFAULT_SONNET_MODEL"),
            "opus": env.get("ANTHROPIC_DEFAULT_OPUS_MODEL"),
        }
        out.append({
            "id": r["id"], "app_type": r["app_type"], "name": r["name"],
            "category": r["category"],
            "endpoint": env.get("ANTHROPIC_BASE_URL") or (ep.get(r["id"], [None])[0]),
            "tier_models": {k: v for k, v in tier.items() if v},
            "default_model": cfg.get("model") if isinstance(cfg, dict) else None,
            "has_token": bool(env.get("ANTHROPIC_AUTH_TOKEN") or env.get("ANTHROPIC_API_KEY")),
        })
    return out

def cmd_list(args):
    con = _conn()
    provs = _providers(con)
    con.close()
    # 只输出非敏感字段；token 从不出现
    if not args.human:
        print(json.dumps(provs, ensure_ascii=False, indent=2))
        return
    usable = [p for p in provs if p["has_token"] and p["endpoint"]]
    print(f"cc-switch 中共 {len(provs)} 个 provider，其中 {len(usable)} 个可直接派发：\n")
    for p in usable:
        tiers = " / ".join(f"{k}={v}" for k, v in p["tier_models"].items()) or "(无档位映射)"
        print(f"  [{p['app_type']}] {p['name']}")
        print(f"      端点: {p['endpoint']}")
        print(f"      档位: {tiers}")
    skipped = [p for p in provs if p not in usable]
    if skipped:
        print(f"\n跳过 {len(skipped)} 个（官方订阅入口或未填 key）：" +
              ", ".join(f"{p['name']}[{p['app_type']}]" for p in skipped))
    print("\n提示: 官方订阅(Claude/Codex/Gemini Official)走各自 CLI，不经本桥。")

def _resolve_task(args):
    if args.task_file:
        with open(args.task_file, "r", encoding="utf-8") as f:
            return f.read()
    return args.task

def cmd_exec(args):
    task = _resolve_task(args)
    if not task or not task.strip():
        print("任务为空：需提供 --task 或 --task-file", file=sys.stderr); sys.exit(7)
    if not args.endpoint and not args.provider:
        print("必须提供 --provider（cc-switch 里的名字）或 --endpoint（自定义端点 URL）。",
              file=sys.stderr); sys.exit(2)
    if args.endpoint:
        # 自定义端点模式：不经 cc-switch db，key 从用户级环境变量读取注入。
        base = args.endpoint
        key_env = args.key_env or "ANTHROPIC_AUTH_TOKEN"
        token = os.environ.get(key_env, "")
        provider_name = args.provider or args.endpoint
        if not token:
            print(f"环境变量 {key_env} 未设置（当前进程读不到）。\n"
                  f"提示: 用 setx 写入后需重开 shell 才生效；本会话内可先 export 临时注入。",
                  file=sys.stderr); sys.exit(4)
        env_cfg = {}
    else:
        con = _conn()
        row = None
        for r in con.execute("SELECT app_type, settings_config FROM providers WHERE name=?", (args.provider,)):
            row = r
            break
        con.close()
        if not row:
            print(f"未找到 provider: {args.provider}\n"
                  f"提示: 先跑 `cc_switch.py list --human` 看可用名字（需与 cc-switch 里的名字完全一致）。",
                  file=sys.stderr); sys.exit(2)
        if row["app_type"] != "claude":
            print(f"app_type={row['app_type']} 暂不支持经此桥派发（仅 claude/Anthropic 端点）。\n"
                  f"提示: codex/gemini 官方订阅请直接用各自 CLI，见 channels.md。",
                  file=sys.stderr); sys.exit(3)
        env_cfg = json.loads(row["settings_config"]).get("env", {})
        base = env_cfg.get("ANTHROPIC_BASE_URL")
        token = env_cfg.get("ANTHROPIC_AUTH_TOKEN") or env_cfg.get("ANTHROPIC_API_KEY")
        provider_name = args.provider
    if not (base and token):
        print(f"provider「{provider_name}」缺 endpoint 或 token（很可能是在 cc-switch 里建了条目但没填 key）。\n"
              f"提示: 去 cc-switch 补上 API key 后重试，或走 setup.md 分支 B 手动配置。",
              file=sys.stderr); sys.exit(4)

    if args.model:
        model = args.model
    else:
        model = env_cfg.get(f"ANTHROPIC_DEFAULT_{args.tier.upper()}_MODEL")
    if not model:
        if args.endpoint:
            print("自定义端点模式没有档位映射，必须用 --model 直接指定模型 ID。",
                  file=sys.stderr); sys.exit(5)
        avail = ", ".join(k for k in ("haiku", "sonnet", "opus")
                          if env_cfg.get(f"ANTHROPIC_DEFAULT_{k.upper()}_MODEL")) or "无"
        print(f"provider「{provider_name}」没有 {args.tier} 档的模型映射。可用档位: {avail}\n"
              f"提示: 用 --model 直接指定模型 ID，或在 cc-switch 里补齐档位映射。",
              file=sys.stderr); sys.exit(5)

    child = dict(os.environ)
    child["ANTHROPIC_BASE_URL"] = base
    child["ANTHROPIC_AUTH_TOKEN"] = token
    child.pop("ANTHROPIC_API_KEY", None)
    # 防挂起加固：派发场景不需要 claude CLI 的遥测/崩溃上报/自动更新/非必要模型调用。
    # 这些后台请求在代理切换、断境外网等网络异常时会把整个子进程挂住直到超时
    # （2026-09-26 ZCode 会话超时事件后的加固；实测 debug 日志未见这些域名，属保险措施）。
    child.setdefault("DISABLE_TELEMETRY", "1")
    child.setdefault("DISABLE_ERROR_REPORTING", "1")
    child.setdefault("DISABLE_AUTOUPDATER", "1")
    child.setdefault("DISABLE_NON_ESSENTIAL_MODEL_CALLS", "1")
    child.setdefault("CLAUDE_CODE_DISABLE_NONESSENTIAL_MODEL_CALLS", "1")
    # token 只在 child 环境里，绝不打印
    # 注意：绝不能用 shell=True + 列表参数——Windows 下多行任务文本会在换行处被截断
    claude_bin = shutil.which("claude")
    if not claude_bin:
        print("找不到 claude CLI", file=sys.stderr); sys.exit(6)
    # 始终用 --output-format json：这是唯一能可靠拿到 is_error/api_error_status 的形式。
    # 否则 API 报错（400 模型不存在 / 529 过载）会 exit 0 并把错误文本伪装成正常回答塞进 stdout。
    # 下游拿到的仍是纯答案（我们只吐 data["result"]），输出契约不变。
    cmd = [claude_bin, "-p", "--model", model, "--output-format", "json"]
    # 只读护栏：--tools 作用在工具注册层（连 --permission-mode bypassPermissions 都压不过它），
    # 是 codex `-s read-only` 的等效物。--permission-mode 没有只读档，别用它。
    # 空串 = 禁用全部工具（纯文本任务最省）。
    cmd += ["--tools", args.tools]
    # 目录授权（2026-09-27 Kimi K3 核验派发 R2 根因之一）：claude CLI 文件类工具默认只放行会话
    # 工作目录，Glob/Read 碰工作目录外的盘符一律 "haven't granted yet"。--add-dir 逐目录放行。
    if args.add_dir:
        dirs = [d.strip().strip('"') for d in args.add_dir.split(",") if d.strip()]
        if dirs:
            cmd += ["--add-dir"] + dirs
    # 全权限（R2 根因之二）：-p 无人值守会话的 permission prompt 无人应答，Bash 类命令全部
    # "requires approval" 后被拒。--dangerously-skip-permissions 跳过询问；--tools 注册层
    # 白名单仍然压着它（未注册的工具依旧不可用），护栏语义不变。
    if args.full_perms:
        cmd += ["--dangerously-skip-permissions"]
    # task 走 stdin，不进 argv：--tools 是 variadic，位置参数会被它吞掉；
    # 且 Windows 下多行 prompt 经 argv 会在第一个换行处截断。
    try:
        res = subprocess.run(
            cmd, env=child, capture_output=True, text=True, input=task,
            encoding="utf-8", errors="replace", timeout=args.timeout,
        )
    except subprocess.TimeoutExpired:
        print(f"[超时] provider={provider_name} model={model} 超过 {args.timeout}s 未返回。\n"
              f"提示: 先排除最常见原因——深思考模型(glm-5.3等)跑长报告类任务实测常需 200-300s，\n"
              f"      默认超时可能偏紧，优先用 --timeout 400 重试。\n"
              f"      也可能是端点过载(529)、模型 ID 无效(400 被 CLI 反复重试)、或网络异常(代理切换中)\n"
              f"      导致 claude CLI 后台请求挂起。别默认当成过载——先直接打端点看响应体再判断。",
              file=sys.stderr)
        sys.exit(9)

    # 无论是否 --usage，都解析 json 并先检查 is_error（这一步是 400/529 伪装成答案的唯一拦截点）。
    try:
        data = json.loads(res.stdout)
    except (json.JSONDecodeError, TypeError):
        data = None
    if data is not None:
        if data.get("is_error") or data.get("api_error_status"):
            sys.stderr.write(
                f"[API 错误] provider={provider_name} model={model} "
                f"status={data.get('api_error_status')}\n{(data.get('result') or '')[:300]}\n"
            )
            sys.exit(8)
        sys.stdout.write(data.get("result", ""))
        if args.usage:
            u = data.get("usage", {}) or {}
            fresh = u.get("input_tokens", 0)
            cc = u.get("cache_creation_input_tokens", 0)
            cr = u.get("cache_read_input_tokens", 0)
            # input 总量 = 新增 + 缓存写 + 缓存读；其中 cache_read 计费远低于 fresh。
            # 注意：total_cost_usd 按 Anthropic 官方价计算，接第三方端点时无意义，故不输出。
            sys.stderr.write(
                f"\n[usage] provider={provider_name} model={model} "
                f"input={fresh + cc + cr} fresh={fresh} cache_create={cc} cache_read={cr} "
                f"output={u.get('output_tokens', 0)} "
                f"turns={data.get('num_turns', '?')} ms={data.get('duration_ms', '?')}\n"
            )
        sys.exit(0)

    # json 解析失败：多半是 CLI 自身失败（非模型层）。保持 stdout 干净，别把 blob 当答案吐出。
    sys.stderr.write(f"[调用失败] provider={provider_name} model={model} "
                     f"exit={res.returncode}\n{(res.stderr or res.stdout or '')[:300]}\n")
    sys.exit(res.returncode if res.returncode != 0 else 1)

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list")
    l.add_argument("--human", action="store_true", help="人类可读摘要（默认输出 JSON）")
    e = sub.add_parser("exec")
    e.add_argument("--provider",
                   help="cc-switch 里的 provider 名。自定义端点模式下可选（仅作显示名）。")
    e.add_argument("--endpoint",
                   help="自定义 Anthropic 兼容端点 URL（如 https://api.deepseek.com/anthropic），"
                        "不经 cc-switch db。与 --key-env、--model 配合使用。")
    e.add_argument("--key-env", dest="key_env", default="",
                   help="存放 API key 的用户级环境变量名（如 DEEPSEEK_API_KEY），仅 --endpoint 模式使用。")
    e.add_argument("--tier", default="haiku", choices=["haiku", "sonnet", "opus"])
    e.add_argument("--model")
    e.add_argument("--task")
    e.add_argument("--task-file", dest="task_file")
    e.add_argument("--tools", default="Read,Grep,Glob",
                   help='派发子进程可用的工具白名单（只读护栏）。默认 Read,Grep,Glob；'
                        '纯文本任务传 "" 禁用全部工具最省。')
    e.add_argument("--add-dir", dest="add_dir", default="",
                   help='逗号分隔的额外授权目录，如 "D:\\program files(science),C:\\Program Files"。'
                        "解决子会话访问工作目录之外路径被拒的问题；含空格路径整体无需加引号。")
    e.add_argument("--full-perms", dest="full_perms", action="store_true",
                   help="附加 --dangerously-skip-permissions：无人值守会话中 Bash 命令的审批无人应答会卡死，"
                        "可信本机任务（如只读取证）加此项放行。默认关闭。")
    e.add_argument("--usage", action="store_true", help="在 stderr 打印 token 用量与耗时")
    e.add_argument("--timeout", type=int, default=300,
                   help="子进程超时秒数，默认 300。深思考模型(glm-5.3等)长报告实测 200-300s，"
                        "180s 偏紧曾造成误杀（2026-09-26 ZCode 事件）。")
    a = p.parse_args()
    if a.cmd == "list":
        cmd_list(a)
    else:
        cmd_exec(a)

if __name__ == "__main__":
    main()
