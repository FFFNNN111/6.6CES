# -*- coding: utf-8 -*-
"""CES 网页版后端：网页入口、DeepSeek 代理、本地模型兜底。"""

from __future__ import annotations

import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
from typing import Any

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS


ROOT = pathlib.Path(__file__).resolve().parent
APP_ROOT = ROOT.parent
FRONTEND_DIR = APP_ROOT / "启动项"
FRONTEND_FILE = FRONTEND_DIR / "CES情感分析.html"
MODEL_DIR = APP_ROOT / "机器学习模型"
DATA_DIR = APP_ROOT / "训练数据"

for module_dir in (MODEL_DIR, DATA_DIR):
    module_path = str(module_dir)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from ces_model import CESModelUnavailable, SERVICE as CES_MODEL_SERVICE  # noqa: E402
from ces_taxonomy import CES_TAXONOMY, CES_TRAINING_STATS  # noqa: E402


DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat").strip()
DEEPSEEK_URL = os.environ.get("DEEPSEEK_URL", "https://api.deepseek.com").strip()
DEEPSEEK_TIMEOUT = float(os.environ.get("DEEPSEEK_TIMEOUT", "12"))
DEEPSEEK_RETRIES = int(os.environ.get("DEEPSEEK_RETRIES", "3"))
PROVIDER_DEEPSEEK_LOCAL = "deepseek v4 pro模型+本地数据集回答"
PROVIDER_LOCAL = "本地数据集回答"

PRELOADED_DATASET = CES_MODEL_SERVICE.load()

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
CORS(app)


class DeepSeekUnavailable(RuntimeError):
    """DeepSeek 不可用。"""


def _json_error(message: str, status: int = 400):
    return jsonify({"ok": False, "message": message}), status


def _safe_error(error: Exception) -> str:
    text = str(error)
    if len(text) > 180:
        text = text[:180] + "..."
    return text.replace(DEEPSEEK_KEY, "***") if DEEPSEEK_KEY else text


def _read_json_body() -> dict[str, Any]:
    data = request.get_json(force=True, silent=True)
    return data if isinstance(data, dict) else {}


def _normalize_deepseek_url(base_url: str) -> str:
    url = (base_url or "https://api.deepseek.com").strip().rstrip("/")
    if url.endswith("/chat/completions"):
        return url
    return url + "/chat/completions"


def _deepseek_should_retry(status_code: int | None) -> bool:
    return status_code is None or status_code == 429 or status_code >= 500


def _call_deepseek(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 1000,
    api_key: str | None = None,
    api_base: str | None = None,
    model: str | None = None,
    temperature: float = 0.2,
    retries: int | None = None,
) -> str:
    key = (api_key if api_key is not None else DEEPSEEK_KEY).strip()
    if not key:
        raise DeepSeekUnavailable("未配置 DEEPSEEK_API_KEY")

    payload = {
        "model": (model or DEEPSEEK_MODEL or "deepseek-chat").strip(),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    endpoint = _normalize_deepseek_url(api_base or DEEPSEEK_URL)
    attempts = max(1, retries if retries is not None else DEEPSEEK_RETRIES)
    last_error: Exception | None = None

    for attempt in range(attempts):
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=DEEPSEEK_TIMEOUT) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as exc:
            last_error = DeepSeekUnavailable(f"DeepSeek HTTP {exc.code}")
            if exc.code in (401, 403) or not _deepseek_should_retry(exc.code) or attempt == attempts - 1:
                raise last_error from exc
        except Exception as exc:
            last_error = DeepSeekUnavailable(_safe_error(exc))
            if attempt == attempts - 1:
                raise last_error from exc
        time.sleep(0.35 * (attempt + 1))
    else:
        raise DeepSeekUnavailable(_safe_error(last_error or DeepSeekUnavailable("DeepSeek 连接失败")))

    try:
        return raw["choices"][0]["message"]["content"]
    except Exception as exc:
        raise DeepSeekUnavailable("DeepSeek 返回结构异常") from exc


def _parse_deepseek_json(raw: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise DeepSeekUnavailable("DeepSeek 未返回严格 JSON") from exc
    if not isinstance(parsed, dict):
        raise DeepSeekUnavailable("DeepSeek JSON 不是对象")
    return parsed


def _bounded_prob(value: Any) -> float | None:
    if isinstance(value, (int, float)) and 0 <= float(value) <= 1:
        return float(value)
    return None


def _deepseek_sentiment(text: str, context: dict[str, Any]) -> dict[str, Any]:
    context_lines = []
    for key, label in (
        ("province", "省份"),
        ("month", "月份"),
        ("parkType", "公园类型"),
        ("culture", "文化线索"),
        ("customDictionary", "自定义词典"),
    ):
        value = (context.get(key) or "").strip() if isinstance(context.get(key), str) else context.get(key)
        if value:
            context_lines.append(f"{label}：{value}")

    system_prompt = (
        "你只判断公园评论的情感倾向和分句情感，不做 CES 分类。"
        "必须只输出严格 JSON，不能输出 Markdown。"
        "JSON 字段为 sentiment、positive_prob、negative_prob、sentence_analysis、reasons。"
        "sentiment 只能是 0、1、2，分别表示消极、中性、积极。"
    )
    user_prompt = "评论：\n" + text
    if context_lines:
        user_prompt += "\n\n语境：\n" + "\n".join(context_lines)

    parsed = _parse_deepseek_json(_call_deepseek(system_prompt, user_prompt, 1000))
    sentiment = parsed.get("sentiment")
    positive_prob = _bounded_prob(parsed.get("positive_prob"))
    negative_prob = _bounded_prob(parsed.get("negative_prob"))
    if sentiment not in (0, 1, 2):
        raise DeepSeekUnavailable("DeepSeek 情感标签不合法")
    if positive_prob is None or negative_prob is None:
        raise DeepSeekUnavailable("DeepSeek 情感概率不合法")

    sentence_rows = parsed.get("sentence_analysis", [])
    if not isinstance(sentence_rows, list):
        sentence_rows = []
    safe_sentences = []
    for item in sentence_rows:
        if not isinstance(item, dict):
            continue
        row_sentiment = item.get("sentiment")
        if row_sentiment not in (0, 1, 2):
            row_sentiment = sentiment
        safe_sentences.append(
            {
                "sentence": str(item.get("sentence", ""))[:300],
                "sentiment": row_sentiment,
            }
        )

    reasons = parsed.get("reasons", [])
    if not isinstance(reasons, list):
        reasons = []

    return {
        "sentiment": sentiment,
        "positive_prob": positive_prob,
        "negative_prob": negative_prob,
        "sentence_analysis": safe_sentences,
        "reasons": [str(item)[:300] for item in reasons if str(item).strip()][:5],
    }


def _apply_deepseek_fallback(local_result: dict[str, Any], error: Exception) -> dict[str, Any]:
    local_result["ok"] = True
    local_result["fallback"] = True
    local_result["provider"] = PROVIDER_LOCAL
    local_result["deepseek"] = {
        "ok": False,
        "fallback": True,
        "message": _safe_error(error),
    }
    confidence = local_result.get("model", {}).get("confidence")
    local_result["sentiment_item"] = {
        "sentiment": None,
        "positive_prob": None,
        "negative_prob": None,
        "confidence": confidence,
        "note": "本地无情感模型，未输出情感倾向；DeepSeek 当前不可用。",
    }
    local_result.setdefault("llm_perception", {})["sentence_analysis"] = []
    reasons = local_result.get("reasons", [])
    if isinstance(reasons, list):
        local_result["reasons"] = reasons + ["DeepSeek 不可用，本次只返回本地 CES 分类结果。"]
    return local_result


def _apply_local_only(local_result: dict[str, Any]) -> dict[str, Any]:
    local_result["ok"] = True
    local_result["fallback"] = True
    local_result["provider"] = PROVIDER_LOCAL
    local_result["deepseek"] = {
        "ok": None,
        "fallback": True,
        "message": "前端先获取本地 CES 分类，情感结果等待 DeepSeek 补充。",
    }
    confidence = local_result.get("model", {}).get("confidence")
    local_result["sentiment_item"] = {
        "sentiment": None,
        "positive_prob": None,
        "negative_prob": None,
        "confidence": confidence,
        "note": "已返回本地 CES 分类；情感结果等待 DeepSeek 补充。",
    }
    local_result.setdefault("llm_perception", {})["sentence_analysis"] = []
    return local_result


def _apply_deepseek_sentiment(local_result: dict[str, Any], sentiment: dict[str, Any]) -> dict[str, Any]:
    confidence = max(sentiment["positive_prob"], sentiment["negative_prob"])
    local_result["ok"] = True
    local_result["fallback"] = False
    local_result["provider"] = PROVIDER_DEEPSEEK_LOCAL
    local_result["deepseek"] = {"ok": True, "fallback": False, "model": DEEPSEEK_MODEL}
    local_result["sentiment_item"] = {
        "sentiment": sentiment["sentiment"],
        "positive_prob": sentiment["positive_prob"],
        "negative_prob": sentiment["negative_prob"],
        "confidence": confidence,
        "note": "情感由 DeepSeek 输出；CES 分类由本地模型输出。",
    }
    local_result.setdefault("llm_perception", {})["sentence_analysis"] = sentiment["sentence_analysis"]
    reasons = local_result.get("reasons", [])
    if not isinstance(reasons, list):
        reasons = []
    local_result["reasons"] = reasons + sentiment["reasons"]
    return local_result


def _top_categories(limit: int = 5) -> list[dict[str, Any]]:
    rows = CES_TRAINING_STATS.get("counts_by_category", [])
    return sorted(rows, key=lambda item: item.get("sample_count", 0), reverse=True)[:limit]


def _matched_taxonomy(question: str, limit: int = 3) -> list[dict[str, Any]]:
    matched = []
    for category in CES_TAXONOMY:
        hits = []
        for subcategory in category.get("subcategories", []):
            name = subcategory.get("name", "")
            keywords = subcategory.get("keywords", [])
            if name and name in question:
                hits.append(name)
            hits.extend([kw for kw in keywords if kw and kw in question])
        if category.get("category", "") in question or hits:
            matched.append(
                {
                    "category": category.get("category", ""),
                    "code": category.get("code", ""),
                    "hits": sorted(set(hits), key=lambda item: (-len(item), item))[:8],
                    "subcategories": [item.get("name", "") for item in category.get("subcategories", [])],
                }
            )
    return matched[:limit]


def _local_database_answer(question: str, error_message: str) -> dict[str, Any]:
    stats = CES_TRAINING_STATS or {}
    model_stats = stats.get("model", {})
    main_metrics = model_stats.get("main", {})
    sub_metrics = model_stats.get("sub", {})
    top_categories = _top_categories()
    matched = _matched_taxonomy(question)

    lines = [
        "DeepSeek 当前不可用，以下回答只基于本地 CES 数据库和本地机器学习模型。",
        "",
        "本地数据概况：",
        f"- 评论样本：{stats.get('sample_count', 0)} 条",
        f"- 一级类别：{stats.get('category_count', len(CES_TAXONOMY))} 类",
        f"- 二级子类：{stats.get('subcategory_count', 0)} 类",
        f"- 触发词：{stats.get('keyword_count', 0)} 个",
        f"- 分句命中明细：{stats.get('sentence_hit_count', 0)} 条",
    ]

    if main_metrics or sub_metrics:
        lines.extend(
            [
                "",
                "本地模型验证结果：",
                f"- 一级类别 micro F1：{main_metrics.get('micro_f1', 0):.4f}",
                f"- 二级子类 micro F1：{sub_metrics.get('micro_f1', 0):.4f}",
            ]
        )

    if matched:
        lines.extend(["", "问题中命中的本地 CES 类别："])
        for item in matched:
            hit_text = "、".join(item["hits"]) if item["hits"] else "类别名称命中"
            sub_text = "、".join(item["subcategories"][:5])
            lines.append(f"- {item['code']} {item['category']}：命中 {hit_text}；包含子类 {sub_text}")
    else:
        lines.extend(["", "本地样本最多的 CES 类别："])
        for item in top_categories:
            lines.append(
                f"- {item.get('code')} {item.get('category')}：{item.get('sample_count', 0)} 条评论样本，"
                f"{item.get('sentence_hit_count', 0)} 条分句命中"
            )

    lines.extend(
        [
            "",
            "说明：本地数据库回答不调用外部 API，不生成新引用，只用于断网或 DeepSeek 不可用时继续完成 CES 分析。",
            f"DeepSeek 错误：{error_message}",
        ]
    )

    sources = [
        "训练数据/ces_taxonomy.py",
        "训练数据/ces_training_data.json",
        "机器学习模型/models/ces_text_classifier.joblib",
        "机器学习模型/models/ces_label_schema.json",
    ]
    return {"answer": "\n".join(lines), "sources": sources}


@app.route("/")
def index():
    if not FRONTEND_FILE.exists():
        return "CES情感分析.html 不存在", 500
    html = FRONTEND_FILE.read_text(encoding="utf-8")
    return html, 200, {"Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store"}


@app.route("/api/health", methods=["GET"])
def health():
    model_info = CES_MODEL_SERVICE.info()
    checks = {
        "frontend": FRONTEND_FILE.exists(),
        "taxonomy": bool(CES_TAXONOMY),
        "training_stats": bool(CES_TRAINING_STATS),
        "model": model_info.get("main_label_count") == 12 and model_info.get("sub_label_count") == 51,
        "training_data_file": (DATA_DIR / "ces_training_data.json").exists(),
    }
    return jsonify(
        {
            "ok": all(checks.values()),
            "checks": checks,
            "dataset": PRELOADED_DATASET,
            "model": {
                "dataset_id": model_info.get("dataset_id"),
                "main_label_count": model_info.get("main_label_count"),
                "sub_label_count": model_info.get("sub_label_count"),
                "metrics": model_info.get("metrics", {}),
            },
        }
    )


@app.route("/api/deepseek-health", methods=["GET"])
def deepseek_health():
    if not DEEPSEEK_KEY:
        return jsonify({"ok": False, "configured": False, "message": "未配置 DEEPSEEK_API_KEY"})
    try:
        raw = _call_deepseek("只输出 JSON。", '请只回复 {"ok":true}', 50)
        parsed = _parse_deepseek_json(raw)
        return jsonify(
            {
                "ok": bool(parsed.get("ok")),
                "configured": True,
                "model": DEEPSEEK_MODEL,
                "url": _normalize_deepseek_url(DEEPSEEK_URL),
            }
        )
    except Exception as exc:
        return jsonify({"ok": False, "configured": True, "message": _safe_error(exc)})


@app.route("/api/text-analysis", methods=["POST"])
def text_analysis():
    data = _read_json_body()
    text = (data.get("text") or "").strip()
    if not text:
        return _json_error("文本为空", 400)

    context = data.get("context") if isinstance(data.get("context"), dict) else {}
    dataset_id = data.get("dataset") or context.get("model_dataset")
    try:
        local_result = CES_MODEL_SERVICE.predict(text, dataset_id)
    except CESModelUnavailable as exc:
        return _json_error(str(exc), 500)
    except Exception as exc:
        return _json_error(str(exc), 500)

    if data.get("skip_deepseek"):
        return jsonify(_apply_local_only(local_result))

    try:
        sentiment = _deepseek_sentiment(text, context)
        return jsonify(_apply_deepseek_sentiment(local_result, sentiment))
    except Exception as exc:
        return jsonify(_apply_deepseek_fallback(local_result, exc))


@app.route("/api/ces-taxonomy", methods=["GET"])
def ces_taxonomy():
    return jsonify({"ok": True, "taxonomy": CES_TAXONOMY})


@app.route("/api/ces-training-stats", methods=["GET"])
def ces_training_stats():
    return jsonify({"ok": True, "stats": CES_TRAINING_STATS})


@app.route("/api/ces-model-info", methods=["GET"])
def ces_model_info():
    try:
        return jsonify({"ok": True, "model": CES_MODEL_SERVICE.info(request.args.get("dataset"))})
    except CESModelUnavailable as exc:
        return _json_error(str(exc), 500)


@app.route("/api/deepseek-client", methods=["POST"])
def deepseek_client():
    data = _read_json_body()
    api_key = (data.get("api_key") or "").strip()
    api_base = (data.get("api_base") or DEEPSEEK_URL).strip()
    model = (data.get("model") or DEEPSEEK_MODEL or "deepseek-chat").strip()
    messages = data.get("messages")
    if not api_key:
        return _json_error("缺少 DeepSeek API Key", 400)
    if not isinstance(messages, list) or not messages:
        return _json_error("messages 不能为空", 400)

    system_prompt = ""
    user_parts = []
    for message in messages:
        if not isinstance(message, dict):
            continue
        role = message.get("role")
        content = str(message.get("content") or "")
        if role == "system":
            system_prompt = content
        elif role == "user":
            user_parts.append(content)
    user_prompt = "\n\n".join(user_parts).strip()
    if not user_prompt:
        return _json_error("user message 不能为空", 400)

    try:
        answer = _call_deepseek(
            system_prompt or "请按用户要求回答。",
            user_prompt,
            int(data.get("max_tokens") or 1000),
            api_key=api_key,
            api_base=api_base,
            model=model,
            temperature=float(data.get("temperature") or 0.2),
            retries=int(data.get("retries") or DEEPSEEK_RETRIES),
        )
        return jsonify(
            {
                "ok": True,
                "provider": PROVIDER_DEEPSEEK_LOCAL,
                "model": model,
                "url": _normalize_deepseek_url(api_base),
                "content": answer,
            }
        )
    except Exception as exc:
        message = _safe_error(exc)
        if api_key:
            message = message.replace(api_key, "***")
        return jsonify({"ok": False, "provider": PROVIDER_LOCAL, "message": message})


@app.route("/api/ces-qa", methods=["POST"])
def ces_qa():
    data = _read_json_body()
    question = (data.get("question") or "").strip()
    if not question:
        return _json_error("问题为空", 400)

    api_key = (data.get("api_key") or "").strip()
    api_base = (data.get("api_base") or DEEPSEEK_URL).strip()
    model = (data.get("model") or DEEPSEEK_MODEL or "deepseek-chat").strip()
    system_prompt = "你是城市文化生态系统服务（CES）专家。用中文简短回答，控制在300字内。"
    try:
        answer = _call_deepseek(system_prompt, question, 800, api_key=api_key or None, api_base=api_base, model=model)
        return jsonify(
            {
                "ok": True,
                "provider": PROVIDER_DEEPSEEK_LOCAL,
                "fallback": False,
                "model": model,
                "url": _normalize_deepseek_url(api_base),
                "answer": answer[:600],
            }
        )
    except Exception as exc:
        message = _safe_error(exc)
        if api_key:
            message = message.replace(api_key, "***")
        local = _local_database_answer(question, message)
        return jsonify(
            {
                "ok": True,
                "provider": PROVIDER_LOCAL,
                "fallback": True,
                "answer": local["answer"],
                "sources": local["sources"],
            }
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8088"))
    print(f"CES ready at http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
