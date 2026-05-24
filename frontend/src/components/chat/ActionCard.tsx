"use client";

import { useStore } from "@/store/useStore";
import { useSendMessage } from "@/hooks/useChat";
import type { ChatInterrupt } from "@/types/api";

export default function ActionCard() {
  const interrupts = useStore((s) => s.interrupts);
  const sessionId = useStore((s) => s.sessionId);
  const { mutate: sendMessage, isPending } = useSendMessage();

  if (interrupts.length === 0) return null;

  const handleAction = (interrupt: ChatInterrupt, approved: boolean) => {
    sendMessage({
      session_id: sessionId || undefined,
      resume: {
        action: interrupt.action,
        approved,
        ...interrupt.details,
      },
    });
  };

  return (
    <>
      {interrupts.map((interrupt, index) => (
        <div key={index} className="flex justify-start">
          <div className="w-[380px] bg-white border border-slate-200 rounded-2xl p-5 shadow-lg shadow-slate-100">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-slate-900">
                Action Required
              </h3>
              <span className="px-2 py-0.5 bg-slate-100 text-slate-600 rounded text-[10px] font-bold uppercase tracking-wide">
                {interrupt.action || "Action"}
              </span>
            </div>

            <div className="space-y-3 mb-5">
              {Object.entries(interrupt.details || {}).map(([key, value]) => (
                <div key={key} className="flex justify-between items-center">
                  <span className="text-xs text-slate-400 capitalize">
                    {key.replace(/_/g, " ")}
                  </span>
                  <span className="text-xs font-medium text-slate-700">
                    {String(value)}
                  </span>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => handleAction(interrupt, true)}
                disabled={isPending}
                className="flex items-center justify-center gap-2 py-2 border border-emerald-500 text-emerald-600 rounded-lg text-xs font-bold hover:bg-emerald-50 transition-colors disabled:opacity-50"
              >
                <span>✅</span> Approve
              </button>
              <button
                onClick={() => handleAction(interrupt, false)}
                disabled={isPending}
                className="flex items-center justify-center gap-2 py-2 border border-rose-500 text-rose-600 rounded-lg text-xs font-bold hover:bg-rose-50 transition-colors disabled:opacity-50"
              >
                <span>❌</span> Decline
              </button>
            </div>
          </div>
        </div>
      ))}
    </>
  );
}
