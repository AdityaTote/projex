from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from app.config import settings

JWT_SECRET = settings.jwt_secret
JWT_ALGORITHM = settings.jwt_algorithm
JWT_EXPIRES_MINUTES = settings.jwt_expires_minutes


def create_access_token(user_id: UUID) -> str:
  now = datetime.now(timezone.utc)
  payload = {
    "sub": str(user_id),
    "iat": int(now.timestamp()),
    "exp": int((now + timedelta(minutes=JWT_EXPIRES_MINUTES)).timestamp()),
  }
  return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
