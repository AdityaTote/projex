from dataclasses import dataclass, field
import os

from dotenv import load_dotenv

load_dotenv()


def _get_int(name: str, default: int) -> int:
  value = os.getenv(name)
  if value is None:
    return default
  try:
    return int(value)
  except ValueError:
    return default


def _get_bool(name: str, default: bool) -> bool:
  value = os.getenv(name)
  if value is None:
    return default
  return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _get_csv(name: str, default: str = "") -> list[str]:
  value = os.getenv(name, default)
  return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
  # JWT
  jwt_secret: str = os.getenv("JWT_SECRET", "change-me")
  jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
  jwt_expires_minutes: int = _get_int("JWT_EXPIRES_MINUTES", 1440)

  # Zoho OAuth
  zoho_client_id: str = os.getenv("ZOHO_CLIENT_ID", "")
  zoho_client_secret: str = os.getenv("ZOHO_CLIENT_SECRET", "")
  zoho_access_type: str = os.getenv("ZOHO_ACCESS_TYPE", "offline")
  zoho_redirect_uri: str = os.getenv("ZOHO_REDIRECT_URI", "")
  zoho_base_url: str = os.getenv("ZOHO_BASE_URL", "https://accounts.zoho.in/oauth/v2")
  zoho_scope: str = os.getenv("ZOHO_SCOPE", "")
  zoho_projects_base_url: str = os.getenv("ZOHO_PROJECTS_BASE_URL", "https://projectsapi.zoho.in/api/v3")

  # Database
  db_host: str = os.getenv("DB_HOST", "localhost")
  db_port: int = _get_int("DB_PORT", 5432)
  db_user: str = os.getenv("DB_USER", "postgres")
  db_password: str = os.getenv("DB_PASSWORD", "password")
  db_name: str = os.getenv("DB_NAME", "zoho_chatbot")

  # CORS
  cors_allow_origins: list[str] = field(
    default_factory=lambda: _get_csv("CORS_ALLOW_ORIGINS", "*")
  )
  cors_allow_methods: list[str] = field(
    default_factory=lambda: _get_csv("CORS_ALLOW_METHODS", "*")
  )
  cors_allow_headers: list[str] = field(
    default_factory=lambda: _get_csv("CORS_ALLOW_HEADERS", "*")
  )
  cors_allow_credentials: bool = _get_bool("CORS_ALLOW_CREDENTIALS", False)


settings = Settings()
