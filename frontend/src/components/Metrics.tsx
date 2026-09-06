import {
  Users,
  ShieldCheck,
  AlertTriangle,
  Activity,
} from "lucide-react";

const metrics = [
  {
    label: "People Detected",
    value: "0",
    icon: Users,
    status: "Live detection",
  },
  {
    label: "Zone Status",
    value: "SECURE",
    icon: ShieldCheck,
    status: "No intrusion detected",
  },
  {
    label: "Active Alerts",
    value: "0",
    icon: AlertTriangle,
    status: "All clear",
  },
  {
    label: "System FPS",
    value: "0",
    icon: Activity,
    status: "AI processing",
  },
];

export default function Metrics() {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
      {metrics.map((metric) => {
        const Icon = metric.icon;

        return (
          <div
            key={metric.label}
            className="glass-elevated rounded-xl p-4 transition hover:border-[var(--primary)]/20"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs text-[var(--muted)]">
                  {metric.label}
                </p>

                <p className="mt-2 text-2xl font-semibold tracking-tight">
                  {metric.value}
                </p>
              </div>

              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[var(--primary)]/10">
                <Icon
                  size={17}
                  strokeWidth={1.8}
                  className="text-[var(--primary-hover)]"
                />
              </div>
            </div>

            <p className="mt-3 text-[10px] text-[var(--secondary)]">
              {metric.status}
            </p>
          </div>
        );
      })}
    </div>
  );
}