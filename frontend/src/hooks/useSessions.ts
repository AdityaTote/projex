"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { sessionsApi } from "@/lib/api/sessions";
import { useStore } from "@/store/useStore";
import type { ChatMessage, SessionDetailData } from "@/types/api";

/** Fetch all sessions for the current user */
export function useSessions() {
  return useQuery({
    queryKey: ["sessions"],
    queryFn: () => sessionsApi.list(),
    staleTime: 60 * 1000, // 1 minute
  });
}

function toChatMessages(session: SessionDetailData): ChatMessage[] {
  return [...session.chats]
    .sort(
      (a, b) =>
        new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
    )
    .map((chat) => ({
      id: chat.id,
      role: chat.role,
      content: chat.content,
      timestamp: chat.created_at,
    }));
}

/** Load a session and hydrate chat messages */
export function useOpenSession() {
  const setSessionId = useStore((s) => s.setSessionId);
  const setMessages = useStore((s) => s.setMessages);
  const setInterrupts = useStore((s) => s.setInterrupts);

  return useMutation({
    mutationFn: (sessionId: string) => sessionsApi.get(sessionId),
    onSuccess: (session) => {
      setSessionId(session.id);
      setMessages(toChatMessages(session));
      setInterrupts([]);
    },
  });
}
