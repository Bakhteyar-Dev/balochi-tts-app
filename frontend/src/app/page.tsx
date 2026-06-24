import Link from "next/link";

import { LogoMark } from "@/components/Logo";

const TOOLS = [
  {
    href: "/translation",
    icon: "🌐",
    title: "Text Translation",
    description:
      "Translate English into Balochi in Latin or Arabic script using fine-tuned neural models.",
    cta: "Open Translation",
  },
  {
    href: "/tts",
    icon: "🔊",
    title: "Text to Speech",
    description:
      "Turn Balochi text into natural-sounding speech, with support for both scripts.",
    cta: "Open Text to Speech",
  },
];

const STEPS = [
  {
    title: "Pick a tool",
    body: "Choose Translation or Text to Speech from the sidebar.",
  },
  {
    title: "Choose the script",
    body: "Switch between Balochi-Latin and Balochi-Arabic with one tap.",
  },
  {
    title: "Type your text",
    body: "Enter English to translate, or Balochi to synthesize into speech.",
  },
  {
    title: "Get the result",
    body: "Read the translation or play and download the generated audio.",
  },
];

const ROADMAP = [
  {
    icon: "🎙️",
    title: "Speech to Text (ASR)",
    body: "Automatic speech recognition for both Latin and Arabic Balochi scripts.",
  },
  {
    icon: "📄",
    title: "OCR",
    body: "Extract Balochi text from images and scanned documents.",
  },
  {
    icon: "🗂️",
    title: "Building Datasets",
    body: "Open, high-quality datasets to push Balochi language AI forward.",
  },
];

export default function Home() {
  return (
    <div className="space-y-14">
      <section>
        <div className="mb-5 inline-flex items-center gap-3">
          <LogoMark className="h-12 w-12" />
          <span className="rounded-full border border-border-soft bg-surface px-3 py-1 text-xs font-semibold text-muted">
            Balochi Language Tools
          </span>
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl">
          Bakhteyar<span className="text-brand">-AI</span>
        </h1>
        <p className="mt-4 max-w-xl text-base leading-relaxed text-muted">
          A growing suite of AI tools for the Balochi language. Translate
          English to Balochi and generate natural speech — in both Latin and
          Arabic script.
        </p>
        <div className="mt-7 flex flex-wrap gap-3">
          <Link
            href="/translation"
            className="rounded-xl bg-gradient-to-br from-brand to-brand-dark px-5 py-3 text-sm font-bold text-white shadow-lg shadow-brand/30 transition hover:scale-[1.02]"
          >
            Start translating →
          </Link>
          <Link
            href="/tts"
            className="rounded-xl border border-border-soft bg-surface px-5 py-3 text-sm font-bold transition hover:border-brand/50"
          >
            Try Text to Speech
          </Link>
        </div>
      </section>

      <section className="grid gap-5 sm:grid-cols-2">
        {TOOLS.map((tool) => (
          <Link
            key={tool.href}
            href={tool.href}
            className="group rounded-2xl border border-border-soft bg-surface p-6 transition hover:-translate-y-1 hover:border-brand/50 hover:shadow-xl hover:shadow-brand/10"
          >
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-surface-soft text-2xl">
              {tool.icon}
            </div>
            <h3 className="text-lg font-bold">{tool.title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted">
              {tool.description}
            </p>
            <span className="mt-4 inline-block text-sm font-semibold text-brand">
              {tool.cta} →
            </span>
          </Link>
        ))}
      </section>

      <section>
        <h2 className="text-2xl font-bold tracking-tight">How to use the app</h2>
        <p className="mt-2 text-sm text-muted">
          Four simple steps to get from text to translation or speech.
        </p>
        <ol className="mt-6 grid gap-4 sm:grid-cols-2">
          {STEPS.map((step, index) => (
            <li
              key={step.title}
              className="flex gap-4 rounded-2xl border border-border-soft bg-surface p-5"
            >
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-brand to-brand-dark text-sm font-bold text-white">
                {index + 1}
              </span>
              <div>
                <h3 className="font-semibold">{step.title}</h3>
                <p className="mt-1 text-sm text-muted">{step.body}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section>
        <div className="flex items-center gap-3">
          <h2 className="text-2xl font-bold tracking-tight">Coming soon</h2>
          <span className="rounded-full bg-surface-soft px-3 py-1 text-xs font-bold uppercase text-brand">
            Roadmap
          </span>
        </div>
        <p className="mt-2 text-sm text-muted">
          We are actively building more Balochi language tools.
        </p>
        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          {ROADMAP.map((item) => (
            <div
              key={item.title}
              className="rounded-2xl border border-dashed border-border-soft bg-surface/60 p-5"
            >
              <div className="mb-3 text-2xl">{item.icon}</div>
              <h3 className="font-semibold">{item.title}</h3>
              <p className="mt-1 text-sm text-muted">{item.body}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="border-t border-border-soft pt-6 text-center text-sm text-muted">
        © {new Date().getFullYear()} Bakhteyar-AI. All rights reserved.
      </footer>
    </div>
  );
}
