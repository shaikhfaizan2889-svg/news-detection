const API_BASE = "/api";

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  model_name: string;
  model_accuracy: number;
}

export interface DetectResult {
  result: "FAKE" | "REAL";
  is_fake: boolean;
  confidence: number;
  text?: string;
  [key: string]: unknown;
}

export interface DetectUrlResult extends DetectResult {
  url: string;
  extracted_text_preview: string;
}

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

export async function detectArticle(text: string): Promise<DetectResult> {
  const res = await fetch(`${API_BASE}/detect`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) throw new Error("Detection failed");
  return res.json();
}

export async function detectFromUrl(url: string): Promise<DetectUrlResult> {
  const res = await fetch(`${API_BASE}/detect-url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || "URL detection failed");
  }
  return res.json();
}

export async function detectBatch(texts: string[]): Promise<DetectResult[]> {
  const res = await fetch(`${API_BASE}/detect-batch`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ texts }),
  });
  if (!res.ok) throw new Error("Batch detection failed");
  return res.json();
}
