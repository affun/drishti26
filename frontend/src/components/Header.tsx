"use client";

import { Menu } from "lucide-react";

type HeaderProps = {
  onMenuClick: () => void;
};

export default function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="glass sticky top-0 z-20 flex items-center justify-between px-4 py-4 sm:px-6 lg:px-8 lg:py-5">
      {/* Left */}
      <div className="flex items-center gap-3">
        {/* Mobile menu */}
        <button
          onClick={onMenuClick}
          className="rounded-lg border border-[var(--border)] p-2 text-[var(--secondary)] transition hover:bg-[var(--surface-elevated)] hover:text-[var(--foreground)] lg:hidden"
          aria-label="Open navigation"
        >
          <Menu size={18} />
        </button>

        <div>
          <p className="mb-1 text-xs uppercase tracking-[0.2em] text-[var(--muted)]">
            Monitoring
          </p>

          <h2 className="text-xl font-semibold tracking-tight sm:text-2xl">
            Live Monitor
          </h2>
        </div>
      </div>

      {/* Right */}
      <div className="hidden items-center gap-6 sm:flex">
        {/* Camera */}
        <div className="text-right">
          <p className="text-xs text-[var(--muted)]">Camera</p>
          <p className="text-sm font-medium">CAM-01</p>
        </div>

        {/* Status */}
        <div className="flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--surface)] px-3 py-1.5">
          <span className="h-2 w-2 animate-pulse rounded-full bg-[var(--success)]" />
          <span className="text-xs text-[var(--secondary)]">
            ONLINE
          </span>
        </div>
      </div>
    </header>
  );
}