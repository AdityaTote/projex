"use client";

import { Bot, Folder, LogOut, Loader2, AlertCircle } from "lucide-react";
import { useStore } from "@/store/useStore";
import { useLogout } from "@/hooks/useAuth";
import { useOpenSession, useSessions } from "@/hooks/useSessions";

export default function Sidebar() {
  const activeProject = useStore((s) => s.activeProject);
  const user = useStore((s) => s.user);
  const resetChat = useStore((s) => s.resetChat);
  const clearProject = useStore((s) => s.clearProject);
  const sessionId = useStore((s) => s.sessionId);
  const { mutate: logout, isPending: isLoggingOut } = useLogout();
  const {
    data: sessions,
    isLoading: isSessionsLoading,
    error: sessionsError,
  } = useSessions();
  const {
    mutate: openSession,
    isPending: isOpeningSession,
    variables: openingSessionId,
  } = useOpenSession();

  return (
    <aside className="w-[250px] h-full flex flex-col border-r border-slate-100 bg-slate-50/50">
      <div className="p-6">
        {/* App Brand */}
        <div className="flex items-center gap-3 mb-10">
          <div className="w-8 h-8 bg-slate-900 rounded-lg flex items-center justify-center text-white shrink-0">
            <Bot className="w-5 h-5" />
          </div>
          <span className="font-bold tracking-tight text-slate-900">
            Projex
          </span>
        </div>

        {/* User Info */}
        {user && (
          <div className="mb-6">
            <label className="text-[10px] uppercase tracking-widest font-semibold text-slate-400">
              Signed in as
            </label>
            <p className="text-sm font-medium text-slate-700 mt-1 truncate">
              {user.name}
            </p>
            <p className="text-xs text-slate-400 truncate">{user.email}</p>
          </div>
        )}

        {/* Active Project */}
        {activeProject && (
          <div className="space-y-4">
            <label className="text-[10px] uppercase tracking-widest font-semibold text-slate-400">
              Current Project
            </label>
            <div className="flex items-center gap-3 bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
              <Folder className="w-4 h-4 text-blue-500 shrink-0" />
              <span className="text-sm font-medium flex-1 truncate">
                {activeProject.name}
              </span>
            </div>
            <button
              onClick={() => clearProject()}
              className="w-full py-2.5 px-4 text-xs font-medium border border-slate-200 rounded-lg text-slate-600 hover:bg-white transition-colors"
            >
              Switch Project
            </button>
          </div>
        )}

        {/* New Chat */}
        {activeProject && (
          <button
            onClick={() => resetChat()}
            className="w-full mt-4 py-2.5 px-4 text-xs font-medium bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors"
          >
            + New Chat
          </button>
        )}

        {/* Sessions */}
        <div className="mt-8">
          <label className="text-[10px] uppercase tracking-widest font-semibold text-slate-400">
            Recent Sessions
          </label>

          {isSessionsLoading && (
            <div className="mt-3 flex items-center gap-2 text-xs text-slate-400">
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              Loading sessions...
            </div>
          )}

          {sessionsError && (
            <div className="mt-3 flex items-center gap-2 text-xs text-rose-500">
              <AlertCircle className="w-3.5 h-3.5" />
              Failed to load sessions
            </div>
          )}

          {sessions && sessions.length === 0 && (
            <div className="mt-3 text-xs text-slate-400">No sessions yet</div>
          )}

          {sessions && sessions.length > 0 && (
            <div className="mt-3 space-y-2 max-h-[320px] overflow-y-auto pr-1">
              {sessions.map((session) => {
                const isActive = sessionId === session.id;
                const isOpening =
                  isOpeningSession && openingSessionId === session.id;
                const title = session.title?.trim() || "Untitled Session";

                return (
                  <button
                    key={session.id}
                    onClick={() => openSession(session.id)}
                    disabled={isOpeningSession}
                    className={`w-full text-left px-3 py-2 rounded-lg border transition-colors ${
                      isActive
                        ? "bg-slate-900 text-white border-slate-900"
                        : "bg-white text-slate-700 border-slate-200 hover:border-slate-300"
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-xs font-medium truncate">{title}</span>
                      {isOpening && (
                        <Loader2 className="w-3 h-3 animate-spin shrink-0" />
                      )}
                    </div>
                    <span
                      className={`text-[10px] ${
                        isActive ? "text-white/70" : "text-slate-400"
                      }`}
                    >
                      {new Date(session.updated_at).toLocaleDateString()}
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Sidebar Bottom */}
      <div className="mt-auto p-6">
        <button
          onClick={() => logout()}
          disabled={isLoggingOut}
          className="flex items-center gap-2 text-slate-400 hover:text-slate-600 transition-colors text-xs font-medium disabled:opacity-50"
        >
          <LogOut className="w-4 h-4" />
          {isLoggingOut ? "Logging out..." : "Logout"}
        </button>
      </div>
    </aside>
  );
}

