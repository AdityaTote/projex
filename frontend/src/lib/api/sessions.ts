import { apiClient } from "@/lib/api-client";
import {
  apiResponseSchema,
  sessionDetailDataSchema,
  sessionsResponseDataSchema,
} from "@/types/api";
import type { SessionDetailData, SessionListItem } from "@/types/api";

export const sessionsApi = {
  /** Fetch all sessions for the current user */
  list: async (): Promise<SessionListItem[]> => {
    const { data } = await apiClient.get("/sessions/");

    const parsed = apiResponseSchema(sessionsResponseDataSchema).parse(data);
    return parsed.data;
  },

  /** Fetch a session with all chats */
  get: async (sessionId: string): Promise<SessionDetailData> => {
    const { data } = await apiClient.get(`/sessions/${sessionId}`);

    const parsed = apiResponseSchema(sessionDetailDataSchema).parse(data);
    return parsed.data;
  },
};
