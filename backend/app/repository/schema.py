from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserModel(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	email: str
	name: str
	portal_id: int
	access_token: str | None = None


class SessionSummaryModel(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	title: str | None
	project_id: str | None = None
	created_at: datetime
	updated_at: datetime


class ChatModel(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	role: str
	content: str
	created_at: datetime


class SessionModel(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	user_id: UUID
	title: str | None
	project_id: str | None
	created_at: datetime
	updated_at: datetime
	chats: list[ChatModel] = Field(default_factory=list)


class TokenModel(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	access_token: str
	refresh_token: str | None
	expires_at: datetime | None
