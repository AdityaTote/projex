from uuid import UUID
from datetime import datetime

from app.database.database import PostgresDB
from app.repository.schema import TokenModel, UserModel

class UserRepository:
  def __init__(self, db: PostgresDB) -> None:
    self._db = db

  def create_user(self, email: str, name: str, portal_id: int) -> UUID:
    query = """
      INSERT INTO users (email, name, portal_id)
      VALUES (%s, %s, %s)
      ON CONFLICT (email) DO UPDATE SET
        name = EXCLUDED.name,
        portal_id = EXCLUDED.portal_id
      RETURNING id
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (email, name, portal_id))
        row = cursor.fetchone()
    if row is None:
      raise RuntimeError("Failed to create user; no id returned.")
    return row[0]

  def get_user_by_email(self, email: str) -> UserModel | None:
    query = """
      SELECT u.id, u.email, u.name, u.portal_id, t.access_token
      FROM users u
      LEFT JOIN tokens t ON t.user_id = u.id
      WHERE u.email = %s
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
      return None
    return UserModel(
      id=row[0],
      email=row[1],
      name=row[2],
      portal_id=row[3],
      access_token=row[4],
    )

  def get_user_by_id(self, user_id: UUID) -> UserModel | None:
    query = """
      SELECT u.id, u.email, u.name, u.portal_id, t.access_token
      FROM users u
      LEFT JOIN tokens t ON t.user_id = u.id
      WHERE u.id = %s
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
    if row is None:
      return None
    return UserModel(
      id=row[0],
      email=row[1],
      name=row[2],
      portal_id=row[3],
      access_token=row[4],
    )

  def upsert_token(
    self,
    user_id: UUID,
    access_token: str,
    refresh_token: str | None,
    expires_at: datetime | None,
  ) -> UUID:
    query = """
      INSERT INTO tokens (user_id, access_token, refresh_token, expires_at)
      VALUES (%s, %s, %s, %s)
      ON CONFLICT (user_id) DO UPDATE SET
        access_token  = EXCLUDED.access_token,
        refresh_token = EXCLUDED.refresh_token,
        expires_at    = EXCLUDED.expires_at
      RETURNING user_id
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (user_id, access_token, refresh_token, expires_at))
        row = cursor.fetchone()
    if row is None:
      raise RuntimeError("Failed to upsert token; no id returned.")
    return row[0]

  def get_token_by_user_id(self, user_id: UUID) -> TokenModel | None:
    query = """
      SELECT access_token, refresh_token, expires_at
      FROM tokens
      WHERE user_id = %s
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
    if row is None:
      return None
    return TokenModel(
      access_token=row[0],
      refresh_token=row[1],
      expires_at=row[2],
    )

  def delete_token_by_user_id(self, user_id: UUID) -> bool:
    query = """
      DELETE FROM tokens
      WHERE user_id = %s
      RETURNING user_id
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
    return row is not None
