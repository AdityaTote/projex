"use client";

import { useQuery } from "@tanstack/react-query";
import { projectsApi } from "@/lib/api/projects";

/** Fetch user's Zoho projects */
export function useProjects() {
  return useQuery({
    queryKey: ["projects"],
    queryFn: () => projectsApi.list(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
