"use client";

import { useState } from "react";

import { ScriptToggle } from "@/components/ScriptToggle";
import { StarRating } from "@/components/StarRating";
import { ApiError, translate } from "@/lib/api";
import { TRANSLATION_SCRIPTS, type ScriptKey } from "@/lib/models";

interface Result {
  text: string;
  script: ScriptKey;
}

export default function TranslationPage() {
  const [script, setScript] = useState<ScriptKey>("latin");
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<Result | null>(null);

  const meta = TRANSLATION_SCRIPTS[script];

  const onTranslate = async () => {
    const clean = text.trim();
    setError(null);
    if (!clean) {
      setError("Please enter English text first.");
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      const data = await translate(clean, script);
      setResult({ text: data.text, script });
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

  const resultMeta = result ? TRANSLATION_SCRIPTS[result.script] : null;

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-extrabold tracking-tight">
          English to Balochi Translation
        </h1>
        <p className="mt-3 max-w-xl text-sm leading-relaxed text-muted">
          Type English text and translate it into Balochi. Choose whether you
          want the result in Latin or Arabic script.
        </p>
      </header>

      <section className="rounded-2xl border border-border-soft bg-surface p-6">
        <h2 className="text-lg font-bold">Enter your text</h2>
        <p className="mb-5 mt-1 text-sm text-muted">
          Choose the output script, then type your English text below.
        </p>

        <ScriptToggle
          scripts={TRANSLATION_SCRIPTS}
          value={script}
          onChange={setScript}
        />

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={6}
          placeholder={meta.placeholder}
          className="w-full resize-y rounded-xl border border-border-soft bg-background p-4 text-base outline-none transition focus:border-brand"
        />

        {error ? (
          <p className="mt-3 rounded-lg bg-red-500/10 px-4 py-2 text-sm text-red-500">
            {error}
          </p>
        ) : null}

        <div className="mt-4 flex gap-3">
          <button
            type="button"
            onClick={onTranslate}
            disabled={loading}
            className="flex-1 rounded-xl bg-gradient-to-br from-brand to-brand-dark px-5 py-3 text-sm font-bold text-white shadow-lg shadow-brand/30 transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Translating…" : "Translate"}
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

      {result && resultMeta ? (
        <section className="rounded-2xl border border-border-soft bg-surface p-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold">Translation</h2>
            <span className="text-xs font-semibold text-muted">
              {resultMeta.label} script
            </span>
          </div>

          <div
            dir={resultMeta.direction}
            className={`mt-4 min-h-24 rounded-xl border border-border-soft bg-background p-4 text-lg leading-relaxed ${resultMeta.fontClass}`}
            style={{ textAlign: resultMeta.align }}
          >
            {result.text}
          </div>

          <div className="mt-4 flex justify-end">
            <a
              href={`data:text/plain;charset=utf-8,${encodeURIComponent(result.text)}`}
              download={`bakhteyar_translation_${result.script}.txt`}
              className="inline-flex items-center gap-2 rounded-lg border border-border-soft px-3 py-1.5 text-xs font-semibold transition hover:border-brand/50"
            >
              Download as Text
            </a>
          </div>

          <StarRating />
        </section>
      ) : null}
    </div>
  );
}
