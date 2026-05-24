from psycopg2.pool import SimpleConnectionPool
import psycopg2.extras
from contextlib import contextmanager

psycopg2.extras.register_uuid()

from pydantic import BaseModel

class DBConfig(BaseModel):
  host: str
  port: int
  user: str
  password: str
  database: str

class PostgresDB:
  def __init__(self, config: DBConfig):
    self._pool = self._init_pool(config)

  def _init_pool(self, config: DBConfig):
    return SimpleConnectionPool(
      minconn=1,
      maxconn=10,
      dbname=config.database,
      user=config.user,
      password=config.password,
      host=config.host,
      port=config.port,
    )

  @contextmanager
  def get_conn(self):
    conn = self._pool.getconn()
    try:
      yield conn
      conn.commit()
    except Exception:
      conn.rollback()
      raise
    finally:
      self._pool.putconn(conn)