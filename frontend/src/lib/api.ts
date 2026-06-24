import type { ScriptKey } from "./models";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api";

export class ApiError extends Error {}

interface TranslateResponse {
  text: string;
  script: ScriptKey;
  label: string;
  direction: string;
}

interface TtsResponse {
  audio_base64: string;
  mime_type: string;
  script: ScriptKey;
  label: string;
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch {
    throw new ApiError(
      "Could not reach the server. Make sure the backend is running.",
    );
  }

  let data: unknown = null;
  try {
    data = await response.json();
  } catch {
    /* response had no JSON body */
  }

  if (!response.ok) {
    const detail =
      data && typeof data === "object" && "detail" in data
        ? String((data as { detail: unknown }).detail)
        : `Request failed (${response.status})`;
    throw new ApiError(detail);
  }

  return data as T;
}

export function translate(text: string, script: ScriptKey) {
  return postJson<TranslateResponse>("/translate/", { text, script });
}

export function textToSpeech(text: string, script: ScriptKey) {
  return postJson<TtsResponse>("/tts/", { text, script });
}

export function base64ToWavUrl(base64: string, mimeType = "audio/wav"): string {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) {
    bytes[i] = binary.charCodeAt(i);
  }
  const blob = new Blob([bytes], { type: mimeType });
  return URL.createObjectURL(blob);
}
