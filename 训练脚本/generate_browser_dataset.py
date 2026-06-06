# -*- coding: utf-8 -*-
"""从本地 CES 分类树生成浏览器兜底数据。"""

from __future__ import annotations

import json
import sys
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = APP_ROOT / "训练数据"
OUTPUT_FILE = APP_ROOT / "启动项" / "ces_browser_dataset.js"
sys.path.insert(0, str(DATA_DIR))

from ces_taxonomy import CES_TAXONOMY, CES_TRAINING_STATS  # noqa: E402


def main() -> None:
    payload = {
        "taxonomy": CES_TAXONOMY,
        "training_stats": CES_TRAINING_STATS,
        "source": "训练数据/ces_taxonomy.py",
    }
    text = "window.CES_BROWSER_DATASET = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n"
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    print(f"generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
