from __future__ import annotations

from pydantic import BaseModel


class ProjectListItem(BaseModel):
  id: str
  name: str
  status: str | None = None


class ProjectsResponse(BaseModel):
  success: bool = True
  message: str | None = None
  data: list[ProjectListItem]
