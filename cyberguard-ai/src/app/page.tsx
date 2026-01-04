"use client";

import { useState } from "react";
import { FullScreenChat } from "@/components/chat/FullScreenChat";
import { DashboardLayout } from "@/components/dashboard/DashboardLayout";
import { ArrowLeft } from "lucide-react";

export default function Home() {
  // Default to chat view
  const [viewMode, setViewMode] = useState<"chat" | "dashboard">("chat");

  if (viewMode === "chat") {
    return <FullScreenChat onSwitchToDashboard={() => setViewMode("dashboard")} />;
  }

  return (
    <div className="relative">
      <button
        onClick={() => setViewMode("chat")}
        className="fixed top-24 left-6 z-50 p-2 bg-black/50 hover:bg-black/80 rounded-full text-white backdrop-blur-sm border border-white/10 shadow-lg group flex items-center gap-2 pr-4 transition-all"
      >
        <ArrowLeft className="w-5 h-5" />
        <span className="text-xs font-bold w-0 overflow-hidden group-hover:w-auto opacity-0 group-hover:opacity-100 transition-all">Back to Chat</span>
      </button>
      <DashboardLayout />
    </div>
  );
}
