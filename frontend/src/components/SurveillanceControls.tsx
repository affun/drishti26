"use client";

import { useState } from "react";
import { Play, Square, Loader2 } from "lucide-react";

type SurveillanceControlsProps = {
  running: boolean;
  onStatusChange: () => void;
};

export default function SurveillanceControls({
  running,
  onStatusChange,
}: SurveillanceControlsProps) {
  const [loading, setLoading] = useState(false);

  const handleToggle = async () => {
    setLoading(true);

    try {
      const endpoint = running
        ? "http://localhost:8000/api/surveillance/stop"
        : "http://localhost:8000/api/surveillance/start";

      const response = await fetch(endpoint, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Failed to change surveillance state");
      }

      onStatusChange();
    } catch (error) {
      console.error("Surveillance control failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-elevated flex flex-col gap-4 rounded-xl p-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-xs uppercase tracking-[0.15em] text-[var(--muted)]">
          Surveillance
        </p>

        <div className="mt-1 flex items-center gap-2">
          <span
            className={`h-2 w-2 rounded-full ${
              running
                ? "animate-pulse bg-[var(--success)]"
                : "bg-[var(--muted)]"
            }`}
          />

          <span className="text-sm font-medium">
            {running ? "System running" : "System stopped"}
          </span>
        </div>
      </div>

      <button
        onClick={handleToggle}
        disabled={loading}
        className={`
          flex items-center justify-center gap-2 rounded-lg px-4 py-2.5
          text-sm font-medium transition disabled:cursor-not-allowed
          disabled:opacity-60
          ${
            running
              ? "border border-[var(--danger)]/30 bg-[var(--danger)]/10 text-[var(--danger)] hover:bg-[var(--danger)]/20"
              : "bg-[var(--primary)] text-white hover:bg-[var(--primary-hover)]"
          }
        `}
      >
        {loading ? (
          <Loader2 size={16} className="animate-spin" />
        ) : running ? (
          <Square size={15} />
        ) : (
          <Play size={15} />
        )}

        {loading
          ? "Processing..."
          : running
            ? "Stop Surveillance"
            : "Start Surveillance"}
      </button>
    </div>
  );
}