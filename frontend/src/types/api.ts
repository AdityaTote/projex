import { z } from "zod/v4";

/* ── Generic API envelope ── */
export const apiResponseSchema = <T extends z.ZodType>(dataSchema: T) =>
  z.object({
    success: z.boolean(),
    message: z.string().nullable(),
    data: dataSchema,
  });

/* ── Auth ── */
export const authUrlDataSchema = z.object({
  authorize_url: z.url(),
});

export const meDataSchema = z.object({
  id: z.string(),
  email: z.email(),
  name: z.string().min(1),
  portal_id: z.number().int(),
});

export const authCallbackDataSchema = z.object({
  access_token: z.string().min(1),
  token_type: z.string(),
  user: meDataSchema,
});

export const logoutDataSchema = z.object({
  revoked: z.boolean(),
});

/* ── Projects ── */
export const projectListItemSchema = z.object({
  id: z.string(),
  name: z.string(),
  status: z.string().nullable().optional(),
});

export const projectsResponseDataSchema = z.array(projectListItemSchema);

/* ── Chat ── */
export const chatRequestSchema = z.object({
  message: z.string().min(1).optional(),
  session_id: z.string().uuid().optional(),
  project_id: z.string().optional(),
  project_name: z.string().optional(),
  resume: z.record(z.string(), z.unknown()).optional(),
});

export const chatInterruptSchema = z
  .object({
    action: z.string(),
    details: z.record(z.string(), z.unknown()).optional().default({}),
  })
  .passthrough();

export const chatResponseDataSchema = z.object({
  session_id: z.string(),
  output: z.record(z.string(), z.unknown()),
  interrupts: z.array(chatInterruptSchema),
});

/* ── Chat Message (for UI) ── */
export const chatMessageSchema = z.object({
  id: z.string().optional(),
  role: z.enum(["user", "assistant", "system"]),
  content: z.string(),
  timestamp: z.string().optional(),
});

/* ── Sessions ── */
export const sessionListItemSchema = z.object({
  id: z.string().uuid(),
  title: z.string().nullable(),
  project_id: z.string().nullable().optional(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const sessionsResponseDataSchema = z.array(sessionListItemSchema);

export const sessionChatItemSchema = z.object({
  id: z.string().uuid(),
  role: z.enum(["user", "assistant", "system"]),
  content: z.string(),
  created_at: z.string(),
});

export const sessionDetailDataSchema = z.object({
  id: z.string().uuid(),
  title: z.string().nullable(),
  project_id: z.string().nullable().optional(),
  created_at: z.string(),
  updated_at: z.string(),
  chats: z.array(sessionChatItemSchema),
});

/* ── Derived TypeScript types ── */
export type ApiResponse<T> = { success: boolean; message: string | null; data: T };
export type AuthUrlData = z.infer<typeof authUrlDataSchema>;
export type MeData = z.infer<typeof meDataSchema>;
export type AuthCallbackData = z.infer<typeof authCallbackDataSchema>;
export type LogoutData = z.infer<typeof logoutDataSchema>;
export type ProjectListItem = z.infer<typeof projectListItemSchema>;
export type ChatRequest = z.infer<typeof chatRequestSchema>;
export type ChatResponseData = z.infer<typeof chatResponseDataSchema>;
export type ChatInterrupt = z.infer<typeof chatInterruptSchema>;
export type ChatMessage = z.infer<typeof chatMessageSchema>;
export type SessionListItem = z.infer<typeof sessionListItemSchema>;
export type SessionChatItem = z.infer<typeof sessionChatItemSchema>;
export type SessionDetailData = z.infer<typeof sessionDetailDataSchema>;
