"use client";

import { useRef, useState } from "react";

interface AudioPlayerProps {
  src: string;
  downloadName: string;
}

const BAR_COUNT = 40;
const BAR_HEIGHTS = Array.from({ length: BAR_COUNT }, (_, i) =>
  Math.round(30 + 70 * Math.abs(Math.sin(i * 0.7) * Math.cos(i * 0.3))),
);

function formatTime(seconds: number): string {
  if (!Number.isFinite(seconds)) return "0:00";
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, "0")}`;
}

export function AudioPlayer({ src, downloadName }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);
  const [current, setCurrent] = useState(0);
  const [duration, setDuration] = useState(0);

  const progress = duration > 0 ? current / duration : 0;

  const toggle = () => {
    const audio = audioRef.current;
    if (!audio) return;
    if (audio.paused) {
      void audio.play();
    } else {
      audio.pause();
    }
  };

  return (
    <div className="rounded-2xl border border-border-soft bg-surface-soft p-4">
      <div className="flex items-center gap-4">
        <button
          type="button"
          onClick={toggle}
          className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-brand to-brand-dark text-white shadow-lg shadow-brand/30 transition hover:scale-105"
          aria-label={playing ? "Pause" : "Play"}
        >
          {playing ? (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <rect x="6" y="5" width="4" height="14" rx="1" />
              <rect x="14" y="5" width="4" height="14" rx="1" />
            </svg>
          ) : (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z" />
            </svg>
          )}
        </button>

        <div className="flex h-12 flex-1 items-center gap-[3px]" aria-hidden="true">
          {BAR_HEIGHTS.map((height, index) => {
            const reached = index / BAR_COUNT <= progress;
            return (
              <span
                key={index}
                className={`flex-1 origin-center rounded-full transition-colors ${
                  reached ? "bg-brand" : "bg-border-soft"
                }`}
                style={{
                  height: `${height}%`,
                  animation:
                    playing && reached
                      ? `bv-bar 1s ease-in-out ${index * 0.04}s infinite`
                      : undefined,
                }}
              />
            );
          })}
        </div>

        <span className="w-20 shrink-0 text-right text-xs tabular-nums text-muted">
          {formatTime(current)} / {formatTime(duration)}
        </span>
      </div>

      <div className="mt-3 flex justify-end">
        <a
          href={src}
          download={downloadName}
          className="inline-flex items-center gap-2 rounded-lg border border-border-soft px-3 py-1.5 text-xs font-semibold text-foreground transition hover:border-brand/50"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 3v12m0 0l-4-4m4 4l4-4M5 21h14" />
          </svg>
          Download WAV
        </a>
      </div>

      <audio
        ref={audioRef}
        src={src}
        onPlay={() => setPlaying(true)}
        onPause={() => setPlaying(false)}
        onEnded={() => setPlaying(false)}
        onTimeUpdate={(e) => setCurrent(e.currentTarget.currentTime)}
        onLoadedMetadata={(e) => setDuration(e.currentTarget.duration)}
        className="hidden"
      />
    </div>
  );
}
