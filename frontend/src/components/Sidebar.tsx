"use client";

import {
  LayoutDashboard,
  Monitor,
  Shield,
  AlertTriangle,
  Image,
  Settings,
  X,
  ChevronRight,
  ChevronLeft,
} from "lucide-react";

type SidebarProps = {
  collapsed: boolean;
  mobileOpen: boolean;
  onToggle: () => void;
  onMobileClose: () => void;
};

const navigation = [
  { name: "Overview", icon: LayoutDashboard },
  { name: "Live Monitor", icon: Monitor },
  { name: "Zones", icon: Shield },
  { name: "Incidents", icon: AlertTriangle },
  { name: "Evidence", icon: Image },
];

export default function Sidebar({
  collapsed,
  mobileOpen,
  onToggle,
  onMobileClose,
}: SidebarProps) {
  return (
    <>
      {/* Mobile backdrop */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm lg:hidden"
          onClick={onMobileClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          glass fixed left-0 top-0 z-50 flex h-screen flex-col
          px-3 py-6 transition-all duration-300
          ${collapsed ? "w-20" : "w-60"}
          ${mobileOpen ? "translate-x-0" : "-translate-x-full"}
          lg:translate-x-0
        `}
      >
        {/* Brand */}
        <div className="relative mb-10">
          <div
            className={`flex items-center ${
              collapsed ? "justify-center" : "justify-start"
            }`}
          >
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[var(--primary)] text-white">
              <Shield size={19} strokeWidth={2} />
            </div>

            {!collapsed && (
              <div className="ml-3 whitespace-nowrap">
                <h1 className="text-lg font-semibold tracking-wide">DRISHTI</h1>
                <p className="text-[9px] tracking-[0.2em] text-[var(--muted)]">
                  AI SECURITY
                </p>
              </div>
            )}
          </div>

          {/* Mobile close */}
          <button
            onClick={onMobileClose}
            className="absolute right-0 top-0 rounded-lg p-2 text-[var(--secondary)] hover:bg-[var(--surface-elevated)] lg:hidden"
          >
            <X size={18} />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex flex-col gap-1">
          {!collapsed && (
            <p className="mb-3 px-3 text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--muted)]">
              Monitoring
            </p>
          )}

          {navigation.map((item) => (
            <button
              key={item.name}
              title={collapsed ? item.name : undefined}
              className={`
                flex items-center gap-3 rounded-lg px-3 py-2.5
                text-sm transition
                ${
                  item.name === "Live Monitor"
                    ? "bg-[var(--primary)]/10 text-[var(--primary-hover)]"
                    : "text-[var(--secondary)] hover:bg-[var(--surface-elevated)] hover:text-[var(--foreground)]"
                }
                ${collapsed ? "justify-center" : ""}
              `}
            >
              <item.icon size={17} strokeWidth={1.8} />

              {!collapsed && <span>{item.name}</span>}
            </button>
          ))}
        </nav>

        {/* Bottom */}
        <div className="mt-auto">
          {!collapsed && (
            <div className="mb-4 border-t border-[var(--border)] pt-5">
              <button
                title="Settings"
                className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-[var(--secondary)] transition hover:bg-[var(--surface-elevated)] hover:text-[var(--foreground)]"
              >
                <Settings size={17} strokeWidth={1.8} />
                Settings
              </button>
            </div>
          )}

          {!collapsed && (
            <div className="mt-4 flex items-center gap-2 px-3 text-xs text-[var(--secondary)]">
              <span className="h-2 w-2 rounded-full bg-[var(--success)]" />
              System operational
            </div>
          )}
        </div>
      </aside>

      {/* Desktop collapse control */}
      <button
        onClick={onToggle}
        className={`
    fixed top-8 z-[60] hidden
    h-10 w-6 items-center justify-center
    border border-[var(--border)]
    bg-[var(--surface)]
    text-[var(--secondary)]
    backdrop-blur-xl
    transition-all duration-300
    hover:bg-[var(--surface-elevated)]
    hover:text-[var(--foreground)]
    lg:flex
    rounded-md
    ${collapsed ? "left-[68px]" : "left-[228px]"}
  `}
        title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
      >
        {collapsed ? (
          <ChevronRight size={15} strokeWidth={1.8} />
        ) : (
          <ChevronLeft size={15} strokeWidth={1.8} />
        )}
      </button>
    </>
  );
}
