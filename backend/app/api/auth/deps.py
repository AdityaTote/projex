from __future__ import annotations

from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from app.repository import user_repository

from .security import JWT_ALGORITHM, JWT_SECRET

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
  credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
  if credentials is None or credentials.scheme.lower() != "bearer":
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

  token = credentials.credentials
  try:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

  subject = payload.get("sub")
  if not subject:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

  try:
    user_id = UUID(str(subject))
  except ValueError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

  user = user_repository.get_user_by_id(user_id)
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

  return user
