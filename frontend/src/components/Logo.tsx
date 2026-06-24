export function LogoMark({ className = "" }: { className?: string }) {
  return (
    <span
      className={`inline-flex items-center justify-center rounded-xl bg-gradient-to-br from-brand to-brand-dark shadow-lg shadow-brand/30 ${className}`}
    >
      <svg
        width="22"
        height="22"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <rect x="3" y="9" width="3" height="6" rx="1.5" fill="white" opacity="0.55" />
        <rect x="8" y="5" width="3" height="14" rx="1.5" fill="white" />
        <rect x="13" y="2" width="3" height="20" rx="1.5" fill="white" opacity="0.85" />
        <rect x="18" y="7" width="3" height="10" rx="1.5" fill="white" opacity="0.55" />
      </svg>
    </span>
  );
}

export function Wordmark({ suffix }: { suffix?: string }) {
  return (
    <span className="text-lg font-bold tracking-tight">
      Bakhteyar<span className="text-brand">-AI</span>
      {suffix ? <span className="font-semibold"> {suffix}</span> : null}
    </span>
  );
}
