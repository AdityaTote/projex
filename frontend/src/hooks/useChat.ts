"use client";

import { useMutation } from "@tanstack/react-query";
import { chatApi } from "@/lib/api/chat";
import { useStore } from "@/store/useStore";
import type { ChatRequest } from "@/types/api";

function extractOutputText(output: unknown): string {
  if (output == null) return "";

  if (typeof output === "string") {
    const trimmed = output.trim();
    if (trimmed.startsWith("{") && trimmed.endsWith("}")) {
      try {
        const parsed = JSON.parse(trimmed) as Record<string, unknown>;
        const reply = parsed.reply || parsed.response || parsed.message;
        if (typeof reply === "string") return reply;
      } catch {
        // Ignore JSON parse failures and fall through to return the raw string.
      }
    }
    return output;
  }

  if (typeof output === "object") {
    const record = output as Record<string, unknown>;
    const reply = record.reply || record.response || record.message;
    if (typeof reply === "string") return reply;
    return JSON.stringify(output);
  }

  return String(output);
}

/** Send a chat message or resume an interrupted action */
export function useSendMessage() {
  const addMessage = useStore((s) => s.addMessage);
  const setSessionId = useStore((s) => s.setSessionId);
  const setInterrupts = useStore((s) => s.setInterrupts);
  const setIsLoading = useStore((s) => s.setIsLoading);
  const sessionId = useStore((s) => s.sessionId);
  const activeProject = useStore((s) => s.activeProject);

  return useMutation({
    mutationFn: (req: ChatRequest) => {
      // Automatically attach the current session ID if one exists
      const payload: ChatRequest = { ...req };
      if (sessionId && !payload.session_id) {
        payload.session_id = sessionId;
      }
      // On first message (no session yet), inject project context
      if (!sessionId && !payload.session_id && activeProject) {
        payload.project_id = activeProject.id;
        payload.project_name = activeProject.name;
      }
      return chatApi.sendMessage(payload);
    },
    onMutate: (req) => {
      setIsLoading(true);
      // Optimistically add the user message to the list
      if (req.message) {
        addMessage({ role: "user", content: req.message });
      }
    },
    onSuccess: (data) => {
      // Track the session ID from the first response
      setSessionId(data.session_id);

      // Add AI response as a message
      const outputText = extractOutputText(data.output);

      addMessage({
        role: "assistant",
        content: String(outputText),
      });

      // Set any interrupts (action cards)
      setInterrupts(data.interrupts || []);
    },
    onSettled: () => {
      setIsLoading(false);
    },
  });
}
