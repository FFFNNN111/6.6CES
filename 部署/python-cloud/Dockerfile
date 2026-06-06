FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r 后端代理/requirements-proxy.txt

ENV PORT=8088
CMD ["sh", "-c", "gunicorn --chdir 后端代理 proxy:app --bind 0.0.0.0:${PORT} --timeout 120"]
