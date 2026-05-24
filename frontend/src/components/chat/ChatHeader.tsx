"use client";

import { useStore } from "@/store/useStore";

export default function ChatHeader() {
  const activeProject = useStore((s) => s.activeProject);
  const user = useStore((s) => s.user);

  // Generate initials from user name
  const initials = user?.name
    ? user.name
        .split(" ")
        .map((w) => w[0])
        .join("")
        .toUpperCase()
        .slice(0, 2)
    : "?";

  return (
    <header className="h-16 px-8 flex items-center justify-between border-b border-slate-100 shrink-0">
      <div className="flex items-center gap-4">
        <h1 className="text-lg font-semibold">{activeProject?.name ?? "Projex"}</h1>
        <div className="flex items-center gap-1.5 px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full text-[10px] font-bold uppercase">
          <span className="w-1.5 h-1.5 bg-blue-500 rounded-full"></span>
          AI Assistant
        </div>
      </div>
      <div className="flex items-center gap-4">
        <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-xs font-bold text-slate-500 italic">
          {initials}
        </div>
      </div>
    </header>
  );
}
