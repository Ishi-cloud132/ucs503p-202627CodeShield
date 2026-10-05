const DEFAULT_API_URL = "http://127.0.0.1:8000/ml/scan";

export async function scanWithCodeShieldML(code, apiUrl = DEFAULT_API_URL) {
  const response = await fetch(apiUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });

  if (!response.ok) {
    throw new Error(`CodeShield scan failed with status ${response.status}`);
  }

  return response.json();
}