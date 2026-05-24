import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { ChatInterrupt, ChatMessage, MeData } from "@/types/api";

interface ActiveProject {
  id: string;
  name: string;
}

interface AppState {
  /* ── Auth ── */
  token: string | null;
  user: MeData | null;
  setAuth: (token: string, user: MeData) => void;
  clearAuth: () => void;

  /* ── Project ── */
  activeProject: ActiveProject | null;
  setActiveProject: (project: ActiveProject) => void;
  clearProject: () => void;

  /* ── Chat ── */
  sessionId: string | null;
  messages: ChatMessage[];
  interrupts: ChatInterrupt[];
  isLoading: boolean;
  setSessionId: (id: string | null) => void;
  addMessage: (msg: ChatMessage) => void;
  setMessages: (msgs: ChatMessage[]) => void;
  setInterrupts: (interrupts: ChatInterrupt[]) => void;
  setIsLoading: (loading: boolean) => void;
  resetChat: () => void;
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      /* ── Auth ── */
      token: null,
      user: null,
      setAuth: (token, user) => set({ token, user }),
      clearAuth: () => set({ token: null, user: null }),

      /* ── Project ── */
      activeProject: null,
      setActiveProject: (project) => set({ activeProject: project }),
      clearProject: () =>
        set({ activeProject: null, sessionId: null, messages: [], interrupts: [], isLoading: false }),

      /* ── Chat ── */
      sessionId: null,
      messages: [],
      interrupts: [],
      isLoading: false,
      setSessionId: (id) => set({ sessionId: id }),
      addMessage: (msg) =>
        set((state) => ({ messages: [...state.messages, msg] })),
      setMessages: (msgs) => set({ messages: msgs }),
      setInterrupts: (interrupts) => set({ interrupts }),
      setIsLoading: (loading) => set({ isLoading: loading }),
      resetChat: () =>
        set({ sessionId: null, messages: [], interrupts: [], isLoading: false }),
    }),
    {
      name: "projex-store",
      // Only persist auth token, user, and active project
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        activeProject: state.activeProject,
      }),
    }
  )
);
