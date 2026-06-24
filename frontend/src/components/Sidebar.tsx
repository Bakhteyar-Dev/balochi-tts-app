"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

import { LogoMark, Wordmark } from "./Logo";
import { useTheme } from "./ThemeProvider";

interface NavItem {
  href: string;
  label: string;
  icon: string;
  soon?: boolean;
}

const NAV_ITEMS: NavItem[] = [
  { href: "/", label: "Home", icon: "🏠" },
  { href: "/translation", label: "Translation", icon: "🌐" },
  { href: "/tts", label: "Text to Speech", icon: "🔊" },
];

const SOON_ITEMS: NavItem[] = [
  { href: "#", label: "Speech to Text (ASR)", icon: "🎙️", soon: true },
  { href: "#", label: "OCR", icon: "📄", soon: true },
  { href: "#", label: "Datasets", icon: "🗂️", soon: true },
];

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  return (
    <button
      type="button"
      onClick={toggleTheme}
      className="flex w-full items-center justify-between rounded-xl border border-border-soft bg-surface px-4 py-2.5 text-sm font-medium text-foreground transition hover:border-brand/50"
      aria-label="Toggle dark mode"
    >
      <span suppressHydrationWarning>
        {theme === "dark" ? "Dark mode" : "Light mode"}
      </span>
      <span aria-hidden="true" suppressHydrationWarning>
        {theme === "dark" ? "🌙" : "☀️"}
      </span>
    </button>
  );
}

function NavLinks({ onNavigate }: { onNavigate?: () => void }) {
  const pathname = usePathname();

  return (
    <nav className="flex flex-col gap-2">
      {NAV_ITEMS.map((item) => {
        const active =
          item.href === "/"
            ? pathname === "/"
            : pathname.startsWith(item.href);
        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={onNavigate}
            className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold transition ${
              active
                ? "bg-gradient-to-br from-brand to-brand-dark text-white shadow-lg shadow-brand/30"
                : "text-foreground hover:bg-surface-soft"
            }`}
          >
            <span aria-hidden="true">{item.icon}</span>
            {item.label}
          </Link>
        );
      })}

      <p className="mt-5 px-4 text-xs font-semibold uppercase tracking-wider text-muted">
        Coming soon
      </p>
      {SOON_ITEMS.map((item) => (
        <div
          key={item.label}
          className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-muted/80"
          aria-disabled="true"
        >
          <span aria-hidden="true">{item.icon}</span>
          <span className="flex-1">{item.label}</span>
          <span className="rounded-full bg-surface-soft px-2 py-0.5 text-[10px] font-bold uppercase text-brand">
            Soon
          </span>
        </div>
      ))}
    </nav>
  );
}

function SidebarBody({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <div className="flex h-full flex-col">
      <div className="mb-8 flex items-center gap-3">
        <LogoMark className="h-10 w-10" />
        <div>
          <div className="text-base font-extrabold">Bakhteyar-AI</div>
          <div className="text-xs text-muted">Balochi Language Tools</div>
        </div>
      </div>

      <NavLinks onNavigate={onNavigate} />

      <div className="mt-auto pt-6">
        <ThemeToggle />
        <p className="mt-4 text-center text-xs text-muted">
          © {new Date().getFullYear()} Bakhteyar-AI.
          <br />
          All rights reserved.
        </p>
      </div>
    </div>
  );
}

export function Sidebar() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Mobile top bar */}
      <header className="sticky top-0 z-30 flex items-center justify-between border-b border-border-soft bg-surface/80 px-4 py-3 backdrop-blur md:hidden">
        <div className="flex items-center gap-2">
          <LogoMark className="h-8 w-8" />
          <Wordmark />
        </div>
        <button
          type="button"
          onClick={() => setOpen(true)}
          className="rounded-lg border border-border-soft p-2"
          aria-label="Open menu"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="4" y1="7" x2="20" y2="7" />
            <line x1="4" y1="12" x2="20" y2="12" />
            <line x1="4" y1="17" x2="20" y2="17" />
          </svg>
        </button>
      </header>

      {/* Mobile drawer */}
      {open ? (
        <div className="fixed inset-0 z-40 md:hidden">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setOpen(false)}
            aria-hidden="true"
          />
          <aside className="absolute left-0 top-0 h-full w-72 max-w-[80%] border-r border-border-soft bg-surface p-5">
            <SidebarBody onNavigate={() => setOpen(false)} />
          </aside>
        </div>
      ) : null}

      {/* Desktop sidebar */}
      <aside className="sticky top-0 hidden h-screen w-72 shrink-0 border-r border-border-soft bg-surface p-6 md:block">
        <SidebarBody />
      </aside>
    </>
  );
}
