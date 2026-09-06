"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import CameraFeed from "@/components/CameraFeed";
import Metrics from "@/components/Metrics";
import SurveillanceControls from "@/components/SurveillanceControls";

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

export default function Home() {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [status, setStatus] = useState<Status>({
    running: false,
    camera: null,
    camera_status: "OFFLINE",
    people_detected: 0,
    people_in_zone: 0,
    zone_status: "secure",
    active_alerts: 0,
    fps: 0,
  });

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/status");

        if (!response.ok) {
          throw new Error("Failed to fetch status");
        }

        const data = await response.json();
        setStatus(data);
      } catch (error) {
        console.error("Backend connection failed:", error);
      }
    };

    fetchStatus();

    const interval = setInterval(fetchStatus, 1000);

    return () => clearInterval(interval);
  }, []);

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
        <Header onMenuClick={() => setMobileOpen(true)} />

        {/* Page content */}
        <div className="p-4 sm:p-6 lg:p-8">
          <CameraFeed />
          <div className="mt-4">
            <Metrics status={status} />
          </div>

          <div className="mt-4">
            {" "}
            <SurveillanceControls
              running={status.running}
              onStatusChange={() => {}}
            />{" "}
          </div>
        </div>
      </section>
    </main>
  );
}
