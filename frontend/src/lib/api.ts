export interface SignToTextResult {
  glosses: string[];
  urdu: string;
  english: string;
  confidence: number;
  notes?: string | null;
  latency_ms: number;
  backend: string;
  adapter?: string | null;
}

export interface SignClause {
  source: string;
  glosses: string[];
  duration_ms: number;
}

export interface TextToSignResult {
  clauses: SignClause[];
  missing_vocab: string[];
  latency_ms: number;
  backend: string;
}

export interface HealthReport {
  status: string;
  backend: string;
  model: string;
  adapter?: string | null;
  device?: string | null;
}

const BASE = "/api";

export async function health(): Promise<HealthReport> {
  const r = await fetch(`${BASE}/health`);
  if (!r.ok) throw new Error(`health ${r.status}`);
  return r.json();
}

export async function signToText(
  clip: Blob,
  langHint = "ur"
): Promise<SignToTextResult> {
  const form = new FormData();
  form.append("clip", clip, "clip.webm");
  const r = await fetch(`${BASE}/sign-to-text?lang_hint=${langHint}`, {
    method: "POST",
    body: form,
  });
  if (!r.ok) throw new Error(`sign-to-text ${r.status}: ${await r.text()}`);
  return r.json();
}

export async function textToSign(
  text: string,
  sourceLang: "ur" | "en" = "ur"
): Promise<TextToSignResult> {
  const r = await fetch(`${BASE}/text-to-sign`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, source_lang: sourceLang }),
  });
  if (!r.ok) throw new Error(`text-to-sign ${r.status}: ${await r.text()}`);
  return r.json();
}

export async function vocabulary(): Promise<{ count: number; signs: string[] }> {
  const r = await fetch(`${BASE}/vocabulary`);
  return r.json();
}
