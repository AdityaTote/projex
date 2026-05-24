import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.repository import pg

from app.api.auth import auth_router
from app.api.chat import chat_router
from app.api.projects import projects_router
from app.api.sessions import sessions_router

def _configure_logging() -> None:
	root = logging.getLogger()
	if not root.handlers:
		handler = logging.StreamHandler()
		formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
		handler.setFormatter(formatter)
		root.addHandler(handler)
	root.setLevel(logging.INFO)


_configure_logging()

logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(_: FastAPI):
	try:
		with pg.get_conn() as conn:
			with conn.cursor() as cursor:
				cursor.execute("SELECT 1")
				cursor.fetchone()
		logger.info("Startup DB check OK")
	except Exception:
		logger.exception("Startup DB check failed")

	yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.cors_allow_origins,
	allow_methods=settings.cors_allow_methods,
	allow_headers=settings.cors_allow_headers,
	allow_credentials=settings.cors_allow_credentials,
)


@app.middleware("http")
async def request_logging(request: Request, call_next):
	start = time.monotonic()
	response = await call_next(request)
	elapsed_ms = (time.monotonic() - start) * 1000
	logger.info(
		"%s %s -> %s (%.2fms)",
		request.method,
		request.url.path,
		response.status_code,
		elapsed_ms,
	)
	return response

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])
app.include_router(sessions_router, prefix="/sessions", tags=["sessions"])


@app.get("/health")
def health():
	return {
		"success": True,
		"message": "OK",
		"data": {"status": "healthy"},
	}


@app.get("/ready")
def ready():
	try:
		with pg.get_conn() as conn:
			with conn.cursor() as cursor:
				cursor.execute("SELECT 1")
				cursor.fetchone()
	except Exception:
		return {
			"success": False,
			"message": "Database not ready",
			"data": {"status": "not_ready"},
		}

	return {
		"success": True,
		"message": "OK",
		"data": {"status": "ready"},
	}