import { apiClient } from "@/lib/api-client";
import {
  apiResponseSchema,
  chatRequestSchema,
  chatResponseDataSchema,
} from "@/types/api";
import type { ChatRequest, ChatResponseData } from "@/types/api";

export const chatApi = {
  /** Send a chat message or resume an interrupted action */
  sendMessage: async (req: ChatRequest): Promise<ChatResponseData> => {
    // Validate input before sending
    const validatedReq = chatRequestSchema.parse(req);

    const { data } = await apiClient.post("/chat/", validatedReq);

    // Validate response
    const parsed = apiResponseSchema(chatResponseDataSchema).parse(data);
    return parsed.data;
  },
};
