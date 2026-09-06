import { Camera, Maximize2, Wifi } from "lucide-react";

export default function CameraFeed() {
  return (
    <div className="glass overflow-hidden rounded-2xl">
      {/* Feed header */}
      <div className="flex items-center justify-between border-b border-[var(--border)] px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[var(--primary)]/10">
            <Camera size={16} className="text-[var(--primary-hover)]" />
          </div>

          <div>
            <p className="text-sm font-medium">CAM-01</p>
            <p className="text-[10px] uppercase tracking-wider text-[var(--muted)]">
              Main Entrance
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--surface)] px-2.5 py-1">
            <Wifi size={12} className="text-[var(--success)]" />
            <span className="text-[10px] text-[var(--secondary)]">LIVE</span>
          </div>

          <button
            className="rounded-lg p-2 text-[var(--secondary)] transition hover:bg-[var(--surface-elevated)] hover:text-[var(--foreground)]"
            aria-label="Fullscreen"
          >
            <Maximize2 size={16} />
          </button>
        </div>
      </div>

      {/* Video area */}
      <div className="relative aspect-video overflow-hidden bg-black">
        <img
          src="http://localhost:8000/api/video"
          alt="Live surveillance feed"
          className="h-full w-full object-contain"
        />

        {/* Recording indicator */}
        <div className="absolute left-4 top-4 flex items-center gap-2 rounded-md border border-[var(--border)] bg-black/40 px-2.5 py-1.5 backdrop-blur-md">
          <span className="h-2 w-2 animate-pulse rounded-full bg-[var(--danger)]" />
          <span className="text-[10px] font-medium tracking-wider text-white">
            REC
          </span>
        </div>
      </div>
    </div>
  );
}
