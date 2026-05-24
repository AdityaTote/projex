import { apiClient } from "@/lib/api-client";
import {
  apiResponseSchema,
  authCallbackDataSchema,
  authUrlDataSchema,
  logoutDataSchema,
  meDataSchema,
} from "@/types/api";
import type { AuthCallbackData, AuthUrlData, LogoutData, MeData } from "@/types/api";

export const authApi = {
  /** Get the Zoho OAuth authorize URL */
  getAuthUrl: async (): Promise<AuthUrlData> => {
    const { data } = await apiClient.get("/auth/url");
    const parsed = apiResponseSchema(authUrlDataSchema).parse(data);
    return parsed.data;
  },

  /** Exchange an OAuth code for a JWT + user profile */
  handleCallback: async (code: string): Promise<AuthCallbackData> => {
    const { data } = await apiClient.get("/auth/callback", {
      params: { code },
    });
    const parsed = apiResponseSchema(authCallbackDataSchema).parse(data);
    return parsed.data;
  },

  /** Get the current authenticated user */
  getMe: async (): Promise<MeData> => {
    const { data } = await apiClient.get("/auth/me");
    const parsed = apiResponseSchema(meDataSchema).parse(data);
    return parsed.data;
  },

  /** Logout — revokes Zoho token on backend */
  logout: async (): Promise<LogoutData> => {
    const { data } = await apiClient.post("/auth/logout");
    const parsed = apiResponseSchema(logoutDataSchema).parse(data);
    return parsed.data;
  },
};
