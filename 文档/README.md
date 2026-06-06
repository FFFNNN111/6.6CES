# CES 网页版分析软件

## 项目简介

这是一个用于分析公园评论中文化生态系统服务（CES）感知的网页工具。手机或电脑打开网址后，可以输入评论文本，查看本地模型识别出的 CES 类别、子类、关键词和模型置信度。

当前页面已改回之前的卡片式页面风格。DeepSeek 现在按主要后端处理，负责补充情感和问答；本地 CES 分类优先由 Python 机器学习模型完成。本地服务不可用时，浏览器会改用 `ces_browser_dataset.js` 内置本地 CES 分类树和关键词数据兜底，不再直接报错。

## 本地运行

推荐双击：

```text
启动项/ces启动项.bat
```

启动脚本会等待后端和本地模型就绪后再打开浏览器，避免页面提前打开后出现 `Failed to fetch`。

当前也已安装用户登录自启动：

```text
启动项/ces_backend_daemon.ps1
```

Windows 登录后会自动启动本地后端，所以直接打开下面这个 HTML 也能使用：

```text
启动项/CES情感分析.html
```

或在 `5.25ces软件` 目录下运行：

```powershell
..\.venv\Scripts\python.exe 后端代理\proxy.py
```

浏览器访问：

```text
http://127.0.0.1:8088
```

手机访问时，双击启动脚本后，窗口会显示同一 Wi-Fi 下的手机访问网址，格式为：

```text
http://电脑局域网IP:8088
```

本地启动项仍保留为：

```text
启动项/CES情感分析.html
```

如果直接打开这个 HTML，它会连接本机 `http://127.0.0.1:8088` 后端。

如果本机服务没有连接，页面会自动使用浏览器内置本地数据集兜底。DeepSeek 有响应时，页面会显示 `deepseek v4 pro模型+本地数据集回答`，不会再提示本地服务断开。DeepSeek 不可用时显示 `本地数据集回答`。浏览器兜底模式只输出 CES 关键词分类，不输出情感概率，也不运行 Python 机器学习模型。

## DeepSeek 配置

DeepSeek 地址默认是：

```text
https://api.deepseek.com
```

页面会自动请求：

```text
https://api.deepseek.com/chat/completions
```

DeepSeek API Key 由用户在页面里自助填写。点击“保存 DeepSeek 设置”后，Key 只保存在当前浏览器本机。

启动脚本只设置 DeepSeek 地址、重试次数和超时时间，不再写入固定 Key。未填写 Key 或 DeepSeek 连接失败时，页面会使用本地 CES 数据集。

自启动安装脚本：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File 启动项\install_html_direct_backend.ps1
```

自启动卸载脚本：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File 启动项\uninstall_html_direct_backend.ps1
```

## 云端部署

部署整个 `5.25ces软件` 文件夹到支持 Python 的云平台。

部署说明和模板在：

```text
部署/python-cloud
```

安装命令：

```bash
pip install -r 后端代理/requirements-proxy.txt
```

启动命令：

```bash
gunicorn --chdir 后端代理 proxy:app --bind 0.0.0.0:$PORT --timeout 120
```

旧的 `部署/vercel-deploy` 方案已删除，因为它不能可靠承载当前 Python 本地模型。

## 测试方法

编译检查：

```powershell
..\.venv\Scripts\python.exe -m py_compile 后端代理\proxy.py 机器学习模型\ces_model.py 训练数据\ces_taxonomy.py 部署\tests\runtime_smoke_test.py 部署\tests\deepseek_live_test.py 部署\tests\deepseek_text_analysis_live_test.py 部署\tests\browser_fallback_static_test.py
```

运行冒烟测试：

```powershell
..\.venv\Scripts\python.exe 部署\tests\runtime_smoke_test.py
```

主要检查：

- 首页可通过 HTTP 打开；
- `/api/health` 显示本地模型、训练数据和分类树可用；
- `/api/text-analysis` 能返回本地 CES 分类；
- DeepSeek 不可用时仍能兜底；
- `/api/ces-qa` 能返回 DeepSeek 或本地数据库答案。

DeepSeek 实连测试：

```powershell
..\.venv\Scripts\python.exe 部署\tests\deepseek_live_test.py
```

DeepSeek 完整文本分析实连测试：

```powershell
..\.venv\Scripts\python.exe 部署\tests\deepseek_text_analysis_live_test.py
```

浏览器本地数据集兜底测试：

```powershell
..\.venv\Scripts\python.exe 部署\tests\browser_fallback_static_test.py
```

重新生成浏览器本地兜底数据：

```powershell
..\.venv\Scripts\python.exe 训练脚本\generate_browser_dataset.py
```

## 已完成功能

- 网页入口统一为 `启动项/CES情感分析.html`。
- 页面已改回之前的卡片式页面风格。
- 启动脚本会等待本地服务就绪后再打开网页，减少 `Failed to fetch`。
- 已安装当前用户登录自启动，让 `CES情感分析.html` 直接打开时可以连接本地后端。
- 新增 `启动项/ces_browser_dataset.js`，本地服务不可用时浏览器直接用本地 CES 分类树和关键词兜底。
- 新增 `训练脚本/generate_browser_dataset.py`，用于从本地分类树重新生成浏览器兜底数据。
- 后端能从 `机器学习模型` 和 `训练数据` 正确加载本地模型与数据。
- 默认加载未拆分模型：12 个一级 CES 类别、51 个二级子类。
- 已瘦身：目录从约 319.15MB 减到约 211.83MB。
- 已删除旧 Vercel 方案、临时测试文件、Python 缓存和非默认 GPT 拆分模型。
- 模型索引只保留默认 `unsplit_20260523`。
- DeepSeek key 改为由用户在页面自助填写。
- DeepSeek 被视为主要后端；前端请求优先走本地代理，失败后才尝试浏览器直连。
- DeepSeek 不可用时，本地 CES 模型及时兜底。
- 后端不可用时，浏览器本地数据集及时兜底。
- 新增 `/api/health` 和 `/api/deepseek-health`。
- 新增 Python 云后端部署模板。
- 已确认 `机器学习模型`、`训练脚本`、`训练数据` 中没有完全重复文件；当前继续保留默认未拆分模型和运行必需训练数据。

## 待办事项

- 公网发布前确认是否允许浏览器本地保存用户自行填写的 DeepSeek key。

## 搜索记录

- 本次任务为现有 CES 软件网页化和后端兜底改造，未进行外部方案搜索。
