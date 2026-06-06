# -*- coding: utf-8 -*-
"""本地 CES 机器学习模型加载与预测。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import sklearn


# === sklearn 版本兼容补丁 ===
import sklearn.linear_model._sgd_fast  # noqa: E402
if not hasattr(sklearn.linear_model._sgd_fast, "Log"):

    class _LossFunction:
        def __init__(self, *args, **kwargs):
            pass

    class _FakeLog(_LossFunction):
        """填补 sklearn 1.0→1.8 中移除的 Log loss，让旧模型可反序列化。"""

    sklearn.linear_model._sgd_fast.Log = _FakeLog
# === 兼容补丁结束 ===


def _sklearn_uses_log_loss_name() -> bool:
    parts = sklearn.__version__.split(".")
    major = int(parts[0]) if parts and parts[0].isdigit() else 0
    minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
    return major > 1 or (major == 1 and minor >= 1)


ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "models"
MODEL_FILE = MODELS_DIR / "ces_text_classifier.joblib"
SCHEMA_FILE = MODELS_DIR / "ces_label_schema.json"
INDEX_FILE = MODELS_DIR / "ces_model_index.json"


class CESModelUnavailable(RuntimeError):
    """本地模型不可用。"""


class CESModelService:
    def __init__(self) -> None:
        self._artifacts: dict[str, dict[str, Any]] = {}
        self._schemas: dict[str, dict[str, Any]] = {}

    def index(self) -> dict[str, Any]:
        if INDEX_FILE.exists():
            return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        return {
            "default_dataset": "unsplit_20260523",
            "models": [
                {
                    "dataset_id": "unsplit_20260523",
                    "dataset_name": "未拆分 CES 指标评论分句分类结果",
                    "model_file": "ces_text_classifier.joblib",
                    "schema_file": "ces_label_schema.json",
                    "report_file": "ces_model_report.md",
                }
            ],
        }

    def _paths(self, dataset_id: str | None = None) -> tuple[str, Path, Path]:
        index = self.index()
        selected = dataset_id or index.get("default_dataset") or "unsplit_20260523"
        for item in index.get("models", []):
            if item.get("dataset_id") == selected:
                return selected, MODELS_DIR / item["model_file"], MODELS_DIR / item["schema_file"]
        raise CESModelUnavailable(f"未知模型数据集：{selected}")

    def load(self, dataset_id: str | None = None) -> str:
        selected, model_file, schema_file = self._paths(dataset_id)
        if not model_file.exists():
            raise CESModelUnavailable(f"模型文件不存在：{model_file}")
        if not schema_file.exists():
            raise CESModelUnavailable(f"标签文件不存在：{schema_file}")
        artifact = joblib.load(model_file)
        # sklearn 新旧版本对同一个逻辑回归损失函数的名称不同。
        try:
            _pipe = artifact.get("pipeline")
            if _pipe is not None:
                _final = _pipe.steps[-1][1] if hasattr(_pipe, "steps") else None
                if _final is not None and hasattr(_final, "estimators_"):
                    for _est in _final.estimators_:
                        if not hasattr(_est, "loss"):
                            continue
                        if _sklearn_uses_log_loss_name() and _est.loss == "log":
                            _est.loss = "log_loss"
                        elif not _sklearn_uses_log_loss_name() and _est.loss == "log_loss":
                            _est.loss = "log"
        except Exception:
            pass
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        if "pipeline" not in artifact or "schema" not in artifact:
            raise CESModelUnavailable("模型文件结构错误")
        if len(schema.get("main_labels", [])) != 12 or len(schema.get("sub_labels", [])) != 51:
            raise CESModelUnavailable("模型标签数量错误")
        self._artifacts[selected] = artifact
        self._schemas[selected] = schema
        return selected

    def artifact(self, dataset_id: str | None = None) -> tuple[str, dict[str, Any]]:
        selected = dataset_id or self.index().get("default_dataset") or "unsplit_20260523"
        if selected not in self._artifacts:
            selected = self.load(selected)
        return selected, self._artifacts[selected]

    def schema(self, dataset_id: str | None = None) -> tuple[str, dict[str, Any]]:
        selected = dataset_id or self.index().get("default_dataset") or "unsplit_20260523"
        if selected not in self._schemas:
            selected = self.load(selected)
        return selected, self._schemas[selected]

    def info(self, dataset_id: str | None = None) -> dict[str, Any]:
        selected, schema = self.schema(dataset_id)
        models = self.index().get("models", [])
        return {
            "dataset_id": selected,
            "model_id": schema.get("model_id"),
            "model_type": schema.get("model_type"),
            "generated_at": schema.get("generated_at"),
            "dataset": schema.get("dataset"),
            "label_count": len(schema.get("labels", [])),
            "main_label_count": len(schema.get("main_labels", [])),
            "sub_label_count": len(schema.get("sub_labels", [])),
            "metrics": schema.get("metrics", {}),
            "available_models": models,
        }

    def predict(self, text: str, dataset_id: str | None = None) -> dict[str, Any]:
        text = (text or "").strip()
        if not text:
            raise ValueError("文本为空")
        selected, artifact = self.artifact(dataset_id)
        _selected, schema = self.schema(selected)
        pipeline = artifact["pipeline"]
        probabilities = pipeline.predict_proba([text])[0]
        labels = schema["labels"]
        thresholds = schema["thresholds"]
        keyword_map = artifact.get("keyword_map", {})

        main_count = len(schema["main_labels"])
        main_results: list[dict[str, Any]] = []
        sub_results: list[dict[str, Any]] = []
        matched_keywords: list[str] = []

        for index, label in enumerate(labels):
            probability = float(probabilities[index])
            threshold = float(thresholds[label["id"]])
            is_active = probability >= threshold
            keywords = [kw for kw in keyword_map.get(label["id"], []) if kw in text]
            matched_keywords.extend(keywords)
            base = {
                "id": label["id"],
                "code": label["code"],
                "name": label["name"],
                "probability": probability,
                "threshold": threshold,
                "active": bool(is_active),
                "keywords": keywords,
                "mention_count": len(keywords),
            }
            if index < main_count:
                if is_active:
                    main_results.append(
                        {
                            **base,
                            "category": label["name"],
                            "perception_frequency": probability,
                            "frequency": probability,
                        }
                    )
            elif is_active:
                sub_results.append(
                    {
                        **base,
                        "category": label["category"],
                        "subcategory": label["name"],
                    }
                )

        main_results.sort(key=lambda item: item["probability"], reverse=True)
        sub_results.sort(key=lambda item: item["probability"], reverse=True)
        matched_keywords = sorted(set(matched_keywords), key=lambda kw: (-len(kw), kw))
        all_probabilities = np.asarray(probabilities, dtype=float)
        active_ratio = len(main_results) / max(1, main_count)
        confidence = float(all_probabilities.max()) if all_probabilities.size else 0.0

        return {
            "text": text,
            "provider": "本地 CES 机器学习模型",
            "model": {
                "dataset_id": selected,
                "id": schema.get("model_id"),
                "type": schema.get("model_type"),
                "confidence": confidence,
            },
            "sentiment_item": {
                "sentiment": None,
                "positive_prob": None,
                "negative_prob": None,
                "confidence": confidence,
                "note": "当前本地模型只训练 CES 多标签分类，不训练情感倾向。",
            },
            "perception_frequency": active_ratio,
            "ces": {
                "active_dimensions": main_results,
                "active_subcategories": sub_results,
                "matched_keywords": matched_keywords,
                "all_probabilities": [
                    {
                        "id": label["id"],
                        "level": label["level"],
                        "code": label["code"],
                        "name": label["name"],
                        "category": label.get("category", label["name"]),
                        "probability": float(probabilities[index]),
                        "threshold": float(thresholds[label["id"]]),
                        "active": bool(float(probabilities[index]) >= float(thresholds[label["id"]])),
                    }
                    for index, label in enumerate(labels)
                ],
            },
            "llm_perception": {"sentence_analysis": []},
            "reasons": [
                f"本地机器学习模型预测出 {len(main_results)} 个一级 CES 类别、{len(sub_results)} 个二级子类。",
                "规则词典仅用于显示原文命中词，不参与模型分类。",
            ],
        }


SERVICE = CESModelService()
