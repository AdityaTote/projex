from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionListItem(BaseModel):
  id: UUID
  title: str | None
  project_id: str | None = None
  created_at: datetime
  updated_at: datetime


class SessionsResponse(BaseModel):
  success: bool = True
  message: str | None = None
  data: list[SessionListItem]


class SessionChatItem(BaseModel):
  id: UUID
  role: str
  content: str
  created_at: datetime


class SessionDetailData(BaseModel):
  id: UUID
  title: str | None
  project_id: str | None = None
  created_at: datetime
  updated_at: datetime
  chats: list[SessionChatItem]


class SessionResponse(BaseModel):
  success: bool = True
  message: str | None = None
  data: SessionDetailData
