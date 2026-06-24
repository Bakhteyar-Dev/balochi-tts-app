"use client";

import { useState } from "react";

const LABELS = ["Poor", "Fair", "Good", "Very Good", "Excellent"];

export function StarRating() {
  const [rating, setRating] = useState<number | null>(null);
  const [hover, setHover] = useState<number | null>(null);

  const display = hover ?? rating ?? 0;

  return (
    <div className="mt-5">
      <p className="mb-2 text-sm font-semibold">Rate this result</p>
      <div className="flex items-center gap-1">
        {[1, 2, 3, 4, 5].map((value) => (
          <button
            key={value}
            type="button"
            onClick={() => setRating(value)}
            onMouseEnter={() => setHover(value)}
            onMouseLeave={() => setHover(null)}
            className="text-2xl leading-none transition"
            aria-label={`${value} stars`}
          >
            <span className={value <= display ? "text-amber-400" : "text-border-soft"}>
              ★
            </span>
          </button>
        ))}
        {rating ? (
          <span className="ml-2 text-sm text-muted">
            Thanks — {LABELS[rating - 1]}!
          </span>
        ) : null}
      </div>
    </div>
  );
}
