"use client";

import { useStore } from "@/store/useStore";
import type { ChatMessage } from "@/types/api";

function unescapeString(str: string | null | undefined): string | null {
  if (!str) return null;
  return str
    .replace(/\\n/g, '\n')
    .replace(/\\"/g, '"')
    .replace(/\\\\/g, '\\')
    .replace(/\\t/g, '\t')
    .trim();
}

function parseXMLResponse(content: string) {
  if (!content || typeof content !== "string" || !content.includes("<response>")) {
    return { text: unescapeString(content) || content };
  }

  try {
    const messageMatch = content.match(/<message>([\s\S]*?)<\/message>/);
    const dataMatch = content.match(/<data>([\s\S]*?)<\/data>/);
    const actionMatch = content.match(/<action>([\s\S]*?)<\/action>/);
    const payloadMatch = content.match(/<payload>([\s\S]*?)<\/payload>/);

    return {
      text: messageMatch ? unescapeString(messageMatch[1]) : (unescapeString(content) || content),
      data: dataMatch ? unescapeString(dataMatch[1]) : null,
      action: actionMatch ? unescapeString(actionMatch[1]) : null,
      payload: payloadMatch ? unescapeString(payloadMatch[1]) : null,
    };
  } catch (e) {
    return { text: unescapeString(content) || content };
  }
}

export default function ChatMessages() {
  const messages = useStore((s) => s.messages);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center px-8">
        <div className="w-12 h-12 bg-slate-100 rounded-2xl flex items-center justify-center mb-4">
          <span className="text-xl">💬</span>
        </div>
        <h3 className="text-sm font-semibold text-slate-700 mb-1">
          Start a conversation
        </h3>
        <p className="text-xs text-slate-400 max-w-xs">
          Ask about your projects, tasks, or team members. You can also create
          and update tasks via chat.
        </p>
      </div>
    );
  }

  return (
    <>
      {messages.map((msg: ChatMessage, index: number) => {
        const parsed = parseXMLResponse(msg.content);

        return (
          <div
            key={msg.id || index}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[70%] px-5 py-3 rounded-2xl shadow-sm ${
                msg.role === "user"
                  ? "bg-slate-900 text-white rounded-tr-none"
                  : "bg-slate-100 text-slate-800 rounded-tl-none"
              }`}
            >
              <p className="text-sm leading-relaxed whitespace-pre-wrap">
                {parsed.text}
              </p>

              {parsed.action && parsed.action !== "none" && (
                <div className="mt-3 p-3 bg-white rounded-xl border border-slate-200">
                  <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-2 flex items-center gap-1">
                    <span>⚡</span> Proposed Action: {parsed.action}
                  </div>
                  {parsed.payload && (
                    <pre className="text-[11px] text-slate-600 bg-slate-50 p-2.5 rounded-lg overflow-x-auto font-mono border border-slate-100">
                      {parsed.payload}
                    </pre>
                  )}
                </div>
              )}

              {parsed.data && (
                <div className="mt-3 p-3 bg-white rounded-xl border border-slate-200">
                  <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-2 flex items-center gap-1">
                    <span>📊</span> Data
                  </div>
                  <pre className="text-[11px] text-slate-600 bg-slate-50 p-2.5 rounded-lg overflow-x-auto whitespace-pre-wrap font-mono border border-slate-100">
                    {parsed.data}
                  </pre>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </>
  );
}
