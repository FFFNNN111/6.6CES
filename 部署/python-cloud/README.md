# CES Python 云后端部署

## 部署目标

把整个 `5.24ces软件` 文件夹部署到支持 Python 的云平台。公网访问入口由 Python 后端提供，首页仍然读取：

```text
启动项/CES情感分析.html
```

## 必填环境变量

```text
DEEPSEEK_API_KEY=你的 DeepSeek API Key
```

可选环境变量：

```text
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_TIMEOUT=12
PORT=8088
```

## 安装命令

```bash
pip install -r 后端代理/requirements-proxy.txt
```

## 启动命令

```bash
gunicorn --chdir 后端代理 proxy:app --bind 0.0.0.0:$PORT --timeout 120
```

Windows 本地调试仍可直接运行：

```powershell
..\.venv\Scripts\python.exe 后端代理\proxy.py
```

## 上线后检查

```text
/api/health
/api/deepseek-health
/api/text-analysis
/api/ces-qa
```

`/api/health` 必须显示本地模型、分类树和训练数据都可用。DeepSeek 连接失败时，`/api/text-analysis` 仍会返回本地 CES 分类，但不会伪造情感结果。
