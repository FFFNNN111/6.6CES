# -*- coding: utf-8 -*-
"""使用环境变量中的 DeepSeek key 检查完整文本分析链路。"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = APP_ROOT / "后端代理"
sys.path.insert(0, str(BACKEND_DIR))

if not os.environ.get("DEEPSEEK_API_KEY", "").strip():
    raise RuntimeError("请先设置环境变量 DEEPSEEK_API_KEY")
os.environ["DEEPSEEK_URL"] = os.environ.get("DEEPSEEK_URL", "https://api.deepseek.com")
os.environ["DEEPSEEK_RETRIES"] = "2"
os.environ["DEEPSEEK_TIMEOUT"] = "25"

import proxy  # noqa: E402


def main() -> None:
    client = proxy.app.test_client()
    resp = client.post(
        "/api/text-analysis",
        json={
            "text": "公园风景优美，步道舒服，但是厕所维护较差。",
            "context": {"province": "广东省"},
        },
    )
    data = resp.get_json() or {}
    result = {
        "status": resp.status_code,
        "ok": data.get("ok"),
        "fallback": data.get("fallback"),
        "provider": data.get("provider"),
        "deepseek": data.get("deepseek"),
        "sentiment": data.get("sentiment_item"),
        "ces_count": len((data.get("ces") or {}).get("active_dimensions") or []),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if resp.status_code != 200:
        raise SystemExit(1)
    if not data.get("ok"):
        raise SystemExit(1)
    if data.get("provider") != "deepseek v4 pro模型+本地数据集回答":
        raise SystemExit(1)
    if not (data.get("ces") or {}).get("active_dimensions"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
