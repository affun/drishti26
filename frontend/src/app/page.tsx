"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import CameraFeed from "@/components/CameraFeed";
import Metrics from "@/components/Metrics";

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
        <Header onMenuClick={() => setMobileOpen(true)} />

        {/* Page content */}
        <div className="p-4 sm:p-6 lg:p-8">
          <CameraFeed />
          <div className="mt-4">
            <Metrics />
          </div>
        </div>
      </section>
    </main>
  );
}
