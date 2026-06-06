# -*- coding: utf-8 -*-
"""临时启动后端并检查首页、健康检查、分析和问答接口。"""

from __future__ import annotations

import json
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

from werkzeug.serving import make_server


APP_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = APP_ROOT / "后端代理"
sys.path.insert(0, str(BACKEND_DIR))

import proxy  # noqa: E402


def get(path: str, headers: dict | None = None):
    req = urllib.request.Request("http://127.0.0.1:8088" + path, headers=headers or {}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.headers.get("Content-Type", ""), resp.read()


def options(path: str, headers: dict | None = None):
    req = urllib.request.Request("http://127.0.0.1:8088" + path, headers=headers or {}, method="OPTIONS")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.headers


def post(path: str, payload: dict):
    req = urllib.request.Request(
        "http://127.0.0.1:8088" + path,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw": body}
        return exc.code, parsed


def main() -> None:
    server = make_server("127.0.0.1", 8088, proxy.app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(1)
    try:
        index_status, index_type, index_body = get("/")
        health_status, _health_type, health_body = get("/api/health")
        cors_status, cors_headers = options(
            "/api/text-analysis",
            {
                "Origin": "file://",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        deepseek_status, _deepseek_type, deepseek_body = get("/api/deepseek-health")
        analysis_status, analysis = post(
            "/api/text-analysis",
            {"text": "公园风景优美，步道舒服，但是厕所维护较差。", "context": {"province": "广东省"}},
        )
        qa_status, qa = post("/api/ces-qa", {"question": "遮阴和步道舒适度会影响哪些 CES 类别？"})

        index_text = index_body.decode("utf-8", errors="ignore")
        result = {
            "index_status": index_status,
            "index_type": index_type,
            "index_has_app_title": "CES 感知情感分析" in index_text,
            "index_has_self_api_key_input": 'id="deepseekApiKey"' in index_text,
            "index_has_fixed_api_key": bool(re.search(r"sk-[A-Za-z0-9]{20,}", index_text)),
            "index_has_browser_fallback": "ces_browser_dataset.js" in index_text and "browserLocalAnalysis" in index_text,
            "health_status": health_status,
            "health": json.loads(health_body.decode("utf-8")),
            "cors_status": cors_status,
            "cors_origin": cors_headers.get("Access-Control-Allow-Origin"),
            "cors_methods": cors_headers.get("Access-Control-Allow-Methods"),
            "deepseek_status": deepseek_status,
            "deepseek": json.loads(deepseek_body.decode("utf-8")),
            "analysis_status": analysis_status,
            "analysis_ok": analysis.get("ok"),
            "analysis_message": analysis.get("message"),
            "analysis_fallback": analysis.get("fallback"),
            "analysis_provider": analysis.get("provider"),
            "analysis_ces_count": len((analysis.get("ces") or {}).get("active_dimensions") or []),
            "analysis_sentiment_note": (analysis.get("sentiment_item") or {}).get("note"),
            "qa_status": qa_status,
            "qa_ok": qa.get("ok"),
            "qa_fallback": qa.get("fallback"),
            "qa_provider": qa.get("provider"),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

        assert result["index_status"] == 200
        assert result["index_has_app_title"]
        assert result["index_has_self_api_key_input"]
        assert result["index_has_fixed_api_key"] is False
        assert result["index_has_browser_fallback"]
        assert result["health"]["ok"]
        assert result["cors_status"] == 200
        assert result["cors_origin"]
        assert result["analysis_ok"]
        assert result["analysis_fallback"] is True
        assert result["analysis_provider"] == "本地数据集回答"
        assert result["analysis_ces_count"] >= 1
        assert result["qa_ok"]
        assert result["qa_fallback"] is True
        assert result["qa_provider"] == "本地数据集回答"
    finally:
        server.shutdown()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
