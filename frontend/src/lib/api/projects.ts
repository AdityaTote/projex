import { apiClient } from "@/lib/api-client";
import {
  apiResponseSchema,
  projectsResponseDataSchema,
} from "@/types/api";
import type { ProjectListItem } from "@/types/api";

export const projectsApi = {
  /** Fetch all Zoho projects for the current user */
  list: async (): Promise<ProjectListItem[]> => {
    const { data } = await apiClient.get("/projects/");

    // Validate response
    const parsed = apiResponseSchema(projectsResponseDataSchema).parse(data);
    return parsed.data;
  },
};
