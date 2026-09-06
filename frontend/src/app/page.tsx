"use client";

import { useState } from "react";
import { Menu, Camera } from "lucide-react";
import Sidebar from "@/components/Sidebar";

export default function Home() {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <main className="min-h-screen bg-[var(--background)] text-[var(--foreground)]">
      <Sidebar
        collapsed={collapsed}
        mobileOpen={mobileOpen}
        onToggle={() => setCollapsed(!collapsed)}
        onMobileClose={() => setMobileOpen(false)}
      />

      {/* Main content */}
      <section
        className={`
          min-h-screen transition-all duration-300
          ${collapsed ? "lg:ml-20" : "lg:ml-60"}
        `}
      >
        {/* Header */}
        <header className="glass sticky top-0 z-20 flex items-center justify-between px-4 py-4 sm:px-6 lg:px-8 lg:py-5">
          <div className="flex items-center gap-3">
            {/* Mobile menu */}
            <button
              onClick={() => setMobileOpen(true)}
              className="rounded-lg border border-[var(--border)] p-2 text-[var(--secondary)] hover:bg-[var(--surface-elevated)] lg:hidden"
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

          {/* Camera status */}
          <div className="hidden items-center gap-6 sm:flex">
            <div className="text-right">
              <p className="text-xs text-[var(--muted)]">Camera</p>
              <p className="text-sm font-medium">CAM-01</p>
            </div>

            <div className="flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--surface)] px-3 py-1.5">
              <span className="h-2 w-2 animate-pulse rounded-full bg-[var(--success)]" />
              <span className="text-xs text-[var(--secondary)]">
                ONLINE
              </span>
            </div>
          </div>
        </header>

        {/* Page content */}
        <div className="p-4 sm:p-6 lg:p-8">
          <div className="glass flex aspect-video w-full items-center justify-center rounded-2xl">
            <div className="text-center">
              <Camera
                size={42}
                strokeWidth={1.5}
                className="mx-auto mb-3 text-[var(--muted)]"
              />

              <p className="text-sm text-[var(--secondary)]">
                Camera feed will appear here
              </p>

              <p className="mt-1 text-xs text-[var(--muted)]">
                AI surveillance is currently offline
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}