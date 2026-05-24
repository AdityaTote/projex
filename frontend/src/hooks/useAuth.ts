"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { authApi } from "@/lib/api/auth";
import { useStore } from "@/store/useStore";

/** Fetch current user profile — enabled only when JWT token exists */
export function useMe() {
  const token = useStore((s) => s.token);
  const setAuth = useStore((s) => s.setAuth);

  return useQuery({
    queryKey: ["auth", "me"],
    queryFn: async () => {
      const user = await authApi.getMe();
      // Sync user data into store (token is already there)
      if (token) setAuth(token, user);
      return user;
    },
    enabled: !!token,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: false,
  });
}

/** Exchange OAuth code for JWT + user, then redirect to /chat */
export function useAuthCallback() {
  const setAuth = useStore((s) => s.setAuth);
  const router = useRouter();

  return useMutation({
    mutationFn: (code: string) => authApi.handleCallback(code),
    onSuccess: (data) => {
      setAuth(data.access_token, data.user);
      router.replace("/chat");
    },
  });
}

/** Logout — revokes backend token, clears store, redirects to / */
export function useLogout() {
  const clearAuth = useStore((s) => s.clearAuth);
  const resetChat = useStore((s) => s.resetChat);
  const router = useRouter();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => authApi.logout(),
    onSettled: () => {
      // Always clear local state, even if the API call fails
      clearAuth();
      resetChat();
      queryClient.clear();
      router.replace("/");
    },
  });
}
