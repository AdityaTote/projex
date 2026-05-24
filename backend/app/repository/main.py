from app.config import settings
from app.database import PostgresDB, DBConfig
from .chats import ChatRepository
from .session import SessionRepository
from .user import UserRepository

pg = PostgresDB(DBConfig(
  host=settings.db_host,
  port=settings.db_port,
  user=settings.db_user,
  password=settings.db_password,
  database=settings.db_name,
))

user_repository = UserRepository(pg)
chat_repository = ChatRepository(pg)
session_repository = SessionRepository(pg)