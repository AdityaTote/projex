from uuid import UUID

from app.database.database import PostgresDB
from app.repository.schema import ChatModel, SessionModel, SessionSummaryModel


class SessionRepository:
  def __init__(self, db: PostgresDB) -> None:
    self._db = db

  def create_session(self, user_id: UUID, title: str, project_id: str | None = None) -> UUID:
    query = """
      INSERT INTO sessions (user_id, title, project_id)
      VALUES (%s, %s, %s)
      RETURNING id
    """
    with self._db.get_conn() as conn:
      conn.autocommit = False
      with conn.cursor() as cursor:
        cursor.execute(query, (user_id, title, project_id))
        row = cursor.fetchone()
    if row is None:
      raise RuntimeError("Failed to create session; no id returned.")
    return row[0]

  def get_sessions_by_user(self, user_id: UUID) -> list[SessionSummaryModel]:
    query = """
      SELECT id, title, project_id, created_at, updated_at
      FROM sessions
      WHERE user_id = %s
      ORDER BY updated_at DESC
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
    return [
      SessionSummaryModel(
        id=row[0],
        title=row[1],
        project_id=row[2],
        created_at=row[3],
        updated_at=row[4],
      )
      for row in rows
    ]

  def get_session_by_id(self, session_id: UUID) -> SessionModel | None:
    query = """
      SELECT
        s.id,
        s.user_id,
        s.title,
        s.project_id,
        s.created_at,
        s.updated_at,
        c.id,
        c.role,
        c.content,
        c.created_at
      FROM sessions s
      LEFT JOIN LATERAL (
        SELECT id, role, content, created_at
        FROM chats
        WHERE session_id = s.id
        ORDER BY created_at DESC
        LIMIT 6
      ) c ON true
      WHERE s.id = %s
      ORDER BY c.created_at ASC
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (session_id,))
        rows = cursor.fetchall()
    if not rows:
      return None
    chats = [
      ChatModel(
        id=row[6],
        role=row[7],
        content=row[8],
        created_at=row[9],
      )
      for row in rows
      if row[6] is not None
    ]
    return SessionModel(
      id=rows[0][0],
      user_id=rows[0][1],
      title=rows[0][2],
      project_id=rows[0][3],
      created_at=rows[0][4],
      updated_at=rows[0][5],
      chats=chats,
    )

  def update_session_title(self, session_id: UUID, title: str) -> bool:
    query = """
      UPDATE sessions
      SET title = %s, updated_at = now()
      WHERE id = %s
      RETURNING id
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (title, session_id))
        row = cursor.fetchone()
    return row is not None

  def delete_session(self, session_id: UUID) -> bool:
    query = """
      DELETE FROM sessions
      WHERE id = %s
      RETURNING id
    """
    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (session_id,))
        row = cursor.fetchone()
    return row is not None
  
  def upsert_session(
    self,
    session_id: UUID,
    user_id: UUID,
    project_id: str | None,
    project_name: str | None,
    messages: list[dict[str, str]],
  ) -> UUID:
    if not isinstance(messages, list):
      raise ValueError("messages must be a list")

    normalized_messages: list[dict[str, str]] = []
    for message in messages:
      role = message.get("role")
      content = message.get("content")
      if role in ("user", "assistant", "system") and isinstance(content, str):
        normalized_messages.append({"role": role, "content": content})

    upsert_query = """
      INSERT INTO sessions (id, user_id, title, project_id)
      VALUES (%s, %s, %s, %s)
      ON CONFLICT (id) DO UPDATE
      SET user_id = EXCLUDED.user_id,
          title = EXCLUDED.title,
          project_id = EXCLUDED.project_id,
          updated_at = now()
      RETURNING id
    """
    insert_chat_query = """
      INSERT INTO chats (session_id, role, content)
      VALUES (%s, %s, %s)
    """

    with self._db.get_conn() as conn:
      with conn.cursor() as cursor:
        cursor.execute(
          upsert_query,
          (session_id, user_id, project_name, project_id),
        )
        row = cursor.fetchone()
        if row is None:
          raise RuntimeError("Failed to upsert session; no id returned.")

        if normalized_messages:
          cursor.executemany(
            insert_chat_query,
            [
              (session_id, message["role"], message["content"])
              for message in normalized_messages
            ],
          )

    return row[0]


