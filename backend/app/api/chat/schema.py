from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
  message: str | None = None
  session_id: UUID | None = None
  project_id: str | None = None
  project_name: str | None = None
  resume: dict[str, Any] | None = None


class ChatResponse(BaseModel):
  success: bool = True
  message: str | None = None
  data: dict[str, Any]
