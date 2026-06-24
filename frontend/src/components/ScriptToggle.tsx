"use client";

import type { ScriptKey, ScriptMeta } from "@/lib/models";

interface ScriptToggleProps {
  scripts: Record<ScriptKey, ScriptMeta>;
  value: ScriptKey;
  onChange: (value: ScriptKey) => void;
}

export function ScriptToggle({ scripts, value, onChange }: ScriptToggleProps) {
  const keys = Object.keys(scripts) as ScriptKey[];

  return (
    <div className="mx-auto mb-6 flex w-full max-w-xs gap-1 rounded-full border border-border-soft bg-surface-soft p-1">
      {keys.map((key) => {
        const active = key === value;
        return (
          <button
            key={key}
            type="button"
            onClick={() => onChange(key)}
            className={`flex-1 rounded-full px-4 py-2 text-sm font-bold transition ${
              active
                ? "bg-gradient-to-br from-brand to-brand-dark text-white shadow-md shadow-brand/30"
                : "text-muted hover:text-foreground"
            }`}
          >
            {scripts[key].buttonLabel}
          </button>
        );
      })}
    </div>
  );
}
