"use client";

import { useEffect, useState } from "react";

import { AudioPlayer } from "@/components/AudioPlayer";
import { ScriptToggle } from "@/components/ScriptToggle";
import { StarRating } from "@/components/StarRating";
import { ApiError, base64ToWavUrl, textToSpeech } from "@/lib/api";
import { TTS_SCRIPTS, type ScriptKey } from "@/lib/models";

interface Result {
  url: string;
  script: ScriptKey;
}

export default function TextToSpeechPage() {
  const [script, setScript] = useState<ScriptKey>("latin");
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<Result | null>(null);

  const meta = TTS_SCRIPTS[script];

  useEffect(() => {
    return () => {
      if (result) URL.revokeObjectURL(result.url);
    };
  }, [result]);

  const onGenerate = async () => {
    const clean = text.trim();
    setError(null);
    if (!clean) {
      setError("Please enter Balochi text first.");
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      const data = await textToSpeech(clean, script);
      const url = base64ToWavUrl(data.audio_base64, data.mime_type);
      setResult({ url, script });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const onClear = () => {
    setText("");
    setResult(null);
    setError(null);
  };

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-extrabold tracking-tight">
          Balochi Text to Speech
        </h1>
        <p className="mt-3 max-w-xl text-sm leading-relaxed text-muted">
          Type Balochi text in Latin or Arabic script and generate
          natural-sounding speech in Balochi.
        </p>
      </header>

      <section className="rounded-2xl border border-border-soft bg-surface p-6">
        <h2 className="text-lg font-bold">Enter your text</h2>
        <p className="mb-5 mt-1 text-sm text-muted">
          Switch the script, then type your Balochi text below.
        </p>

        <ScriptToggle scripts={TTS_SCRIPTS} value={script} onChange={setScript} />

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={6}
          dir={meta.direction}
          placeholder={meta.placeholder}
          className={`w-full resize-y rounded-xl border border-border-soft bg-background p-4 text-lg outline-none transition focus:border-brand ${meta.fontClass}`}
          style={{ textAlign: meta.align }}
        />

        {error ? (
          <p className="mt-3 rounded-lg bg-red-500/10 px-4 py-2 text-sm text-red-500">
            {error}
          </p>
        ) : null}

        <div className="mt-4 flex gap-3">
          <button
            type="button"
            onClick={onGenerate}
            disabled={loading}
            className="flex-1 rounded-xl bg-gradient-to-br from-brand to-brand-dark px-5 py-3 text-sm font-bold text-white shadow-lg shadow-brand/30 transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Generating…" : "Generate Speech"}
          </button>
          <button
            type="button"
            onClick={onClear}
            className="rounded-xl bg-gradient-to-br from-emerald-500 to-emerald-600 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-500/30 transition hover:scale-[1.01]"
          >
            Clear
          </button>
        </div>
      </section>

      {result ? (
        <section className="rounded-2xl border border-border-soft bg-surface p-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold">Result</h2>
            <span className="text-xs font-semibold text-muted">
              {TTS_SCRIPTS[result.script].label} script
            </span>
          </div>

          <div className="mt-4">
            <AudioPlayer
              key={result.url}
              src={result.url}
              downloadName={`bakhteyar_voice_${result.script}.wav`}
            />
          </div>

          <StarRating />
        </section>
      ) : null}
    </div>
  );
}
