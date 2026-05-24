from uuid import UUID

from app.database import PostgresDB
from app.repository.schema import ChatModel


class ChatRepository:
  def __init__(self, db: PostgresDB) -> None:
    self._db = db

  def create_chat(
    self,
    session_id: UUID,
    role: str,
    content: str,
  ) -> UUID:
    if role not in ("user", "assistant", "system"):
      raise ValueError(f"Invalid role '{role}'. Must be user, assistant, or system.")

    query = """
      INSERT INTO chats (session_id, role, content)
      VALUES (%s, %s, %s)
      RETURNING id
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (session_id, role, content))
        row = cursor.fetchone()
        if row is None:
          raise RuntimeError("Failed to create chat; no id returned.")

        cursor.execute(
          "UPDATE sessions SET updated_at = now() WHERE id = %s",
          (session_id,)
        )

    return row[0]

  def get_chats_by_session(self, session_id: UUID) -> list[ChatModel]:
    query = """
      SELECT id, role, content, created_at
      FROM chats
      WHERE session_id = %s
      ORDER BY created_at ASC
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (session_id,))
        rows = cursor.fetchall()
    return [
      ChatModel(
        id=row[0],
        role=row[1],
        content=row[2],
        created_at=row[3],
      )
      for row in rows
    ]

  def get_last_n_chats(self, session_id: UUID, n: int) -> list[ChatModel]:
    query = """
      SELECT id, role, content, created_at
      FROM (
        SELECT id, role, content, created_at
        FROM chats
        WHERE session_id = %s
        ORDER BY created_at DESC
        LIMIT %s
      ) sub
      ORDER BY created_at ASC
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (session_id, n))
        rows = cursor.fetchall()
    return [
      ChatModel(
        id=row[0],
        role=row[1],
        content=row[2],
        created_at=row[3],
      )
      for row in rows
    ]

  def delete_chat(self, chat_id: UUID) -> bool:
    query = """
      DELETE FROM chats
      WHERE id = %s
      RETURNING id
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (chat_id,))
        row = cursor.fetchone()
    return row is not None

  def delete_all_chats_in_session(self, session_id: UUID) -> int:
    query = """
      DELETE FROM chats
      WHERE session_id = %s
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (session_id,))
        return cursor.rowcount


