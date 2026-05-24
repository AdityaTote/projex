from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class AuthUrlData(BaseModel):
  authorize_url: str


class AuthUrlResponse(BaseModel):
  success: bool = True
  message: str | None = None
  data: AuthUrlData


class MeData(BaseModel):
  id: UUID
  email: str
  name: str
  portal_id: int


class MeResponse(BaseModel):
  success: bool = True
  message: str | None = None
  data: MeData


class AuthCallbackData(BaseModel):
  access_token: str
  token_type: str = "bearer"
  user: MeData


class AuthCallbackResponse(BaseModel):
  success: bool = True
  message: str | None = None
  data: AuthCallbackData


class LogoutData(BaseModel):
  revoked: bool


class LogoutResponse(BaseModel):
  success: bool = True
  message: str | None = None
  data: LogoutData
