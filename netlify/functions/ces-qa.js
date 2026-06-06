const DEFAULT_API_BASE = "https://api.deepseek.com";
const PROVIDER_DEEPSEEK = "deepseek v4 pro模型+本地数据集回答";
const PROVIDER_LOCAL = "本地数据集回答";

function headers() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Content-Type": "application/json; charset=utf-8",
  };
}

function normalizeDeepSeekUrl(base) {
  const clean = String(base || DEFAULT_API_BASE).replace(/\/+$/, "");
  return clean.endsWith("/chat/completions") ? clean : `${clean}/chat/completions`;
}

function json(statusCode, body) {
  return { statusCode, headers: headers(), body: JSON.stringify(body) };
}

function localAnswer(question, message) {
  return [
    "DeepSeek 当前不可用，以下回答基于浏览器内置本地 CES 数据集。",
    "",
    `问题：${question}`,
    "",
    "说明：云端静态部署不运行本地 Python 机器学习模型；页面会使用浏览器内置 CES 分类树和关键词数据兜底。",
    `DeepSeek 错误：${message}`,
  ].join("\n");
}

exports.handler = async function handler(event) {
  if (event.httpMethod === "OPTIONS") return { statusCode: 204, headers: headers(), body: "" };
  if (event.httpMethod !== "POST") return json(405, { ok: false, message: "只支持 POST" });

  let data;
  try {
    data = JSON.parse(event.body || "{}");
  } catch (error) {
    return json(400, { ok: false, message: "请求体不是 JSON" });
  }

  const question = String(data.question || "").trim();
  const apiKey = String(data.api_key || "").trim();
  if (!question) return json(400, { ok: false, message: "问题为空" });
  if (!apiKey) {
    return json(200, {
      ok: true,
      provider: PROVIDER_LOCAL,
      fallback: true,
      answer: localAnswer(question, "缺少 DeepSeek API Key"),
    });
  }

  try {
    const response = await fetch(normalizeDeepSeekUrl(data.api_base), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: String(data.model || "deepseek-chat").trim(),
        messages: [
          { role: "system", content: "你是城市文化生态系统服务（CES）专家。用中文简短回答，控制在300字内。" },
          { role: "user", content: question },
        ],
        temperature: 0.2,
        max_tokens: 800,
      }),
    });
    if (!response.ok) {
      return json(200, {
        ok: true,
        provider: PROVIDER_LOCAL,
        fallback: true,
        answer: localAnswer(question, `DeepSeek HTTP ${response.status}`),
      });
    }
    const raw = await response.json();
    const answer = raw && raw.choices && raw.choices[0] && raw.choices[0].message ? raw.choices[0].message.content : "";
    return json(200, {
      ok: true,
      provider: PROVIDER_DEEPSEEK,
      fallback: false,
      answer: answer.slice(0, 600),
    });
  } catch (error) {
    return json(200, {
      ok: true,
      provider: PROVIDER_LOCAL,
      fallback: true,
      answer: localAnswer(question, String(error && error.message ? error.message : error)),
    });
  }
};

