"use client";

import { Send } from "lucide-react";
import { useState, useCallback } from "react";
import { useSendMessage } from "@/hooks/useChat";
import { useStore } from "@/store/useStore";

export default function ChatInput() {
  const [input, setInput] = useState("");
  const { mutate: sendMessage } = useSendMessage();
  const isLoading = useStore((s) => s.isLoading);

  const handleSend = useCallback(() => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    sendMessage({ message: trimmed });
    setInput("");
  }, [input, isLoading, sendMessage]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="p-6 pt-0 bg-white">
      <div className="max-w-3xl mx-auto relative flex items-center bg-white border border-slate-200 rounded-2xl shadow-sm pr-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about your projects or tasks..."
          disabled={isLoading}
          className="flex-1 py-4 px-6 text-sm bg-transparent outline-none text-slate-700 disabled:opacity-50"
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || isLoading}
          className="w-10 h-10 bg-slate-900 hover:bg-slate-800 transition-colors rounded-xl flex items-center justify-center text-white shrink-0 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <Send className="w-4 h-4 ml-0.5" />
          )}
        </button>
      </div>
      <p className="text-center mt-3 text-[10px] text-slate-400 uppercase tracking-widest font-medium">
        Secured by Projex
      </p>
    </div>
  );
}
