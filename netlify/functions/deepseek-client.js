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

exports.handler = async function handler(event) {
  if (event.httpMethod === "OPTIONS") return { statusCode: 204, headers: headers(), body: "" };
  if (event.httpMethod !== "POST") return json(405, { ok: false, message: "只支持 POST" });

  let data;
  try {
    data = JSON.parse(event.body || "{}");
  } catch (error) {
    return json(400, { ok: false, message: "请求体不是 JSON" });
  }

  const apiKey = String(data.api_key || "").trim();
  const messages = data.messages;
  if (!apiKey) return json(400, { ok: false, provider: PROVIDER_LOCAL, message: "缺少 DeepSeek API Key" });
  if (!Array.isArray(messages) || !messages.length) {
    return json(400, { ok: false, provider: PROVIDER_LOCAL, message: "messages 不能为空" });
  }

  const payload = {
    model: String(data.model || "deepseek-chat").trim(),
    messages,
    temperature: Number.isFinite(Number(data.temperature)) ? Number(data.temperature) : 0.2,
    max_tokens: Number.isFinite(Number(data.max_tokens)) ? Number(data.max_tokens) : 1000,
  };

  try {
    const response = await fetch(normalizeDeepSeekUrl(data.api_base), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(payload),
    });
    if (!response.ok) return json(200, { ok: false, provider: PROVIDER_LOCAL, message: `DeepSeek HTTP ${response.status}` });

    const raw = await response.json();
    const content = raw && raw.choices && raw.choices[0] && raw.choices[0].message ? raw.choices[0].message.content : "";
    return json(200, {
      ok: true,
      provider: PROVIDER_DEEPSEEK,
      model: payload.model,
      url: normalizeDeepSeekUrl(data.api_base),
      content,
    });
  } catch (error) {
    return json(200, { ok: false, provider: PROVIDER_LOCAL, message: String(error && error.message ? error.message : error) });
  }
};

