#!/usr/bin/env python3
"""ai-cross 冒烟：claude CLI + GLM 端点（key 从用户级环境变量 GLM_CODING_KEY 按进程注入，不打印）。"""
import json, os, subprocess, sys, winreg

def get_user_env(name):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as k:
        return winreg.QueryValueEx(k, name)[0]

token = os.environ.get("GLM_CODING_KEY") or get_user_env("GLM_CODING_KEY")
claude = os.path.expanduser(r"~\.local\bin\claude.exe")

for model in ["glm-5-turbo", "glm-5.3"]:
    env = dict(os.environ)
    env["ANTHROPIC_BASE_URL"] = "https://open.bigmodel.cn/api/anthropic"
    env["ANTHROPIC_AUTH_TOKEN"] = token
    env.pop("ANTHROPIC_API_KEY", None)
    cmd = [claude, "-p", "--model", model, "--output-format", "json", "--tools", ""]
    try:
        res = subprocess.run(cmd, env=env, capture_output=True, text=True,
                             input="只回复两个字：正常", encoding="utf-8",
                             errors="replace", timeout=180)
    except subprocess.TimeoutExpired:
        print(f"{model}: TIMEOUT"); continue
    try:
        data = json.loads(res.stdout)
    except Exception:
        print(f"{model}: 调用失败 exit={res.returncode} {(res.stderr or res.stdout)[:200]}"); continue
    if data.get("is_error") or data.get("api_error_status"):
        print(f"{model}: API 错误 status={data.get('api_error_status')} {(data.get('result') or '')[:150]}")
    else:
        u = data.get("usage", {}) or {}
        models = list((data.get("modelUsage") or {}).keys())
        print(f"{model}: OK result={data.get('result')!r} "
              f"in={u.get('input_tokens')} out={u.get('output_tokens')} "
              f"cache_read={u.get('cache_read_input_tokens')} "
              f"turns={data.get('num_turns')} ms={data.get('duration_ms')} modelUsage={models}")
