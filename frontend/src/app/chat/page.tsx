"use client";

import { useEffect, useRef } from "react";
import { useStore } from "@/store/useStore";
import Sidebar from "@/components/chat/Sidebar";
import ChatHeader from "@/components/chat/ChatHeader";
import ChatMessages from "@/components/chat/ChatMessages";
import ActionCard from "@/components/chat/ActionCard";
import TypingIndicator from "@/components/chat/TypingIndicator";
import ChatInput from "@/components/chat/ChatInput";
import ProjectSelector from "@/components/chat/ProjectSelector";

export default function ChatPage() {
  const messages = useStore((s) => s.messages);
  const isLoading = useStore((s) => s.isLoading);
  const activeProject = useStore((s) => s.activeProject);
  const sessionId = useStore((s) => s.sessionId);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, isLoading]);

  return (
    <div className="flex h-screen bg-white text-slate-900 font-sans overflow-hidden">
      <Sidebar />

      <main className="flex-1 flex flex-col bg-white h-full relative min-h-0">
        <ChatHeader />

        {activeProject || sessionId ? (
          <>
            <section
              ref={scrollRef}
              className="flex-1 min-h-0 overflow-y-auto flex flex-col p-8 space-y-6"
            >
              <ChatMessages />
              <ActionCard />
              {isLoading && <TypingIndicator />}
            </section>

            <ChatInput />
          </>
        ) : (
          <ProjectSelector />
        )}
      </main>
    </div>
  );
}
