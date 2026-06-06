# -*- coding: utf-8 -*-
"""用环境变量中的 DeepSeek key 做一次实连检查，不打印 key。"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = APP_ROOT / "后端代理"
sys.path.insert(0, str(BACKEND_DIR))

import proxy  # noqa: E402


def main() -> None:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("请先设置环境变量 DEEPSEEK_API_KEY")
    client = proxy.app.test_client()
    resp = client.post(
        "/api/deepseek-client",
        json={
            "api_key": api_key,
            "api_base": os.environ.get("DEEPSEEK_URL", "https://api.deepseek.com"),
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "只输出 JSON。"},
                {"role": "user", "content": '请只回复 {"ok":true}'},
            ],
            "max_tokens": 50,
            "retries": 2,
        },
    )
    data = resp.get_json() or {}
    print(
        json.dumps(
            {
                "status": resp.status_code,
                "ok": data.get("ok"),
                "provider": data.get("provider"),
                "message": data.get("message"),
                "content": data.get("content"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if not data.get("ok"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
