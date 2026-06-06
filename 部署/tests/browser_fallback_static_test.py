# -*- coding: utf-8 -*-
"""检查双击 HTML 时可用的浏览器本地 CES 数据集兜底。"""

from __future__ import annotations

import json
import re
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[2]
HTML_FILE = APP_ROOT / "启动项" / "CES情感分析.html"
BROWSER_DATASET_FILE = APP_ROOT / "启动项" / "ces_browser_dataset.js"


def main() -> None:
    html = HTML_FILE.read_text(encoding="utf-8")
    js = BROWSER_DATASET_FILE.read_text(encoding="utf-8")
    match = re.match(r"window\.CES_BROWSER_DATASET\s*=\s*(.*);\s*$", js, re.S)
    if not match:
        raise SystemExit("浏览器本地数据集格式不正确")
    data = json.loads(match.group(1))
    taxonomy = data.get("taxonomy") or []
    keywords = []
    for category in taxonomy:
        for subcategory in category.get("subcategories") or []:
            keywords.extend(subcategory.get("keywords") or [])

    sample = "公园风景优美，步道舒服，但是厕所维护较差。"
    hits = [keyword for keyword in keywords if keyword and keyword in sample]
    result = {
        "html_has_dataset_script": "ces_browser_dataset.js" in html,
        "html_has_browser_fallback": "browserLocalAnalysis" in html,
        "taxonomy_count": len(taxonomy),
        "keyword_count": len(set(keywords)),
        "sample_hits": hits,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    assert result["html_has_dataset_script"]
    assert result["html_has_browser_fallback"]
    assert result["taxonomy_count"] >= 12
    assert result["keyword_count"] >= 100
    assert hits


if __name__ == "__main__":
    main()
