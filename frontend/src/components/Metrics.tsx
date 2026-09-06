"use client";

import {
  Users,
  ShieldCheck,
  AlertTriangle,
  Activity,
} from "lucide-react";

type Status = {
  running: boolean;
  camera: string | null;
  camera_status: string;
  people_detected: number;
  people_in_zone: number;
  zone_status: string;
  active_alerts: number;
  fps: number;
};

type MetricsProps = {
  status: Status;
};

export default function Metrics({ status }: MetricsProps) {
  const metrics = [
    {
      label: "People Detected",
      value: status.people_detected,
      icon: Users,
      status: "Live detection",
    },
    {
      label: "Zone Status",
      value: status.zone_status.toUpperCase(),
      icon: ShieldCheck,
      status:
        status.people_in_zone > 0
          ? `${status.people_in_zone} person in zone`
          : "No intrusion detected",
    },
    {
      label: "Active Alerts",
      value: status.active_alerts,
      icon: AlertTriangle,
      status: "Current alerts",
    },
    {
      label: "System FPS",
      value: status.fps,
      icon: Activity,
      status: "AI processing",
    },
  ];

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