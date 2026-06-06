# CES 网页版架构

## 文件职责

- `启动项/CES情感分析.html`：之前的卡片式前端页面，提供 DeepSeek API Key 自助填写，把 DeepSeek 视为主要后端，先取本地 CES 结果，再尝试 DeepSeek。
- `启动项/ces_browser_dataset.js`：由 `训练数据/ces_taxonomy.py` 生成的浏览器本地兜底数据，供本地服务不可用时使用。
- `启动项/ces启动项.bat`：当前推荐本地启动入口，调用同目录 PowerShell 脚本。
- `启动项/启动CES网页版.bat`：旧启动入口，已转到 `ces启动项.bat`。
- `启动项/启动CES网页版.ps1`：设置 DeepSeek 地址、重试和超时，等待后端健康检查通过后再打开网页，并显示手机同 Wi-Fi 访问地址。
- `启动项/ces_backend_daemon.ps1`：后台常驻启动脚本，供 Windows 登录自启动调用。
- `启动项/install_html_direct_backend.ps1`：把后台常驻脚本写入当前用户登录自启动。
- `启动项/uninstall_html_direct_backend.ps1`：移除当前用户登录自启动。
- `后端代理/proxy.py`：Flask 后端，提供网页、本地模型分析、DeepSeek 代理、本地数据问答和健康检查。
- `机器学习模型/ces_model.py`：加载本地 joblib 模型，输出 12 个一级类别和 51 个二级子类的预测结果。
- `机器学习模型/models/`：保存默认未拆分模型、标签文件、模型指标和模型索引；非默认 GPT 拆分模型已删除。
- `训练数据/ces_taxonomy.py`：提供 CES 分类树和训练统计。
- `训练数据/ces_training_data.json`：保存完整本地训练数据。
- `训练脚本/`：从默认未拆分 Excel 数据重新生成训练数据、分类树和模型。
- `训练脚本/generate_browser_dataset.py`：从 `训练数据/ces_taxonomy.py` 生成 `启动项/ces_browser_dataset.js`。
- `部署/python-cloud/`：Python 云后端部署说明和模板。
- `部署/tests/runtime_smoke_test.py`：临时启动 HTTP 服务并检查首页、健康检查、分析和问答接口。
- `部署/tests/deepseek_live_test.py`：通过后端代理实连 DeepSeek。
- `部署/tests/deepseek_text_analysis_live_test.py`：检查完整文本分析链路。
- `部署/tests/browser_fallback_static_test.py`：检查 HTML 已加载浏览器本地数据集，并能用本地关键词命中示例文本。

## 调用关系

- 用户访问 `/` 时，`proxy.py` 读取并返回 `启动项/CES情感分析.html`。
- 用户直接打开 `CES情感分析.html` 时，可以填写 DeepSeek API Key 并检查连接；DeepSeek 有响应时显示 `DeepSeek 后端已连接`。
- 如果本地服务不可达，页面改用 `ces_browser_dataset.js` 里的本地 CES 分类树和关键词数据兜底。
- 前端提交文本到 `/api/text-analysis`，并设置 `skip_deepseek` 先拿本地 CES 分类；该请求失败时进入浏览器本地兜底。
- 前端优先把用户填写的 API Key 传给 `/api/deepseek-client` 本地代理；如果本地代理不可达，再尝试浏览器直连 DeepSeek。
- DeepSeek 成功时，页面标注 `deepseek v4 pro模型+本地数据集回答`。
- DeepSeek 失败时，页面标注 `本地数据集回答`。
- `/api/ces-qa` 可接收用户填写的 API Key，优先调用 DeepSeek；失败时根据 `ces_taxonomy.py` 和本地训练统计返回数据库答案。
- `/api/health` 检查前端文件、分类树、训练统计、本地模型和训练数据文件。
- `/api/deepseek-health` 只检查 DeepSeek 连通性，不泄露 key。

## 关键决定

- 本地 CES 模型永远是分类主来源。
- 本地服务不可用时，浏览器兜底只做关键词分类，不伪造机器学习置信度。
- DeepSeek 只做情感补充和问答，不决定 CES 分类。
- 不再使用前端关键词规则伪造情感概率。
- DeepSeek key 不写入 HTML，由用户在页面填写并保存到本机浏览器。
- Vercel JS 代理已删除，公网部署使用 Python 后端。
- 瘦身后只暴露默认模型 `unsplit_20260523`。
- 已确认 `机器学习模型`、`训练脚本`、`训练数据` 中没有完全重复文件；旧 GPT 拆分模型链路不再作为当前运行链路。
