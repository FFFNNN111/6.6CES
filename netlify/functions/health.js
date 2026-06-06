function headers() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Content-Type": "application/json; charset=utf-8",
  };
}

exports.handler = async function handler(event) {
  if (event.httpMethod === "OPTIONS") return { statusCode: 204, headers: headers(), body: "" };
  return {
    statusCode: 200,
    headers: headers(),
    body: JSON.stringify({
      ok: true,
      runtime: "netlify",
      checks: {
        frontend: true,
        browser_dataset: true,
        python_model: false,
      },
      note: "Netlify 静态部署使用浏览器本地 CES 数据兜底，不运行 Python 机器学习模型。",
    }),
  };
};

