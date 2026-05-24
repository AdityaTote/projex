from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth.deps import get_current_user
from app.repository import chat_repository, session_repository

from .schema import (
  SessionChatItem,
  SessionDetailData,
  SessionListItem,
  SessionResponse,
  SessionsResponse,
)

sessions_router = APIRouter()


@sessions_router.get("/", response_model=SessionsResponse)
def list_sessions(user=Depends(get_current_user)):
  sessions = session_repository.get_sessions_by_user(user.id)
  items = [
    SessionListItem(
      id=session.id,
      title=session.title,
      project_id=session.project_id,
      created_at=session.created_at,
      updated_at=session.updated_at,
    )
    for session in sessions
  ]

  return SessionsResponse(
    message="Sessions retrieved",
    data=items,
  )


@sessions_router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: UUID, user=Depends(get_current_user)):
  session = session_repository.get_session_by_id(session_id)
  if session is None or session.user_id != user.id:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Session not found",
    )

  chats = chat_repository.get_chats_by_session(session_id)
  chat_items = [
    SessionChatItem(
      id=chat.id,
      role=chat.role,
      content=chat.content,
      created_at=chat.created_at,
    )
    for chat in chats
  ]

  return SessionResponse(
    message="Session retrieved",
    data=SessionDetailData(
      id=session.id,
      title=session.title,
      project_id=session.project_id,
      created_at=session.created_at,
      updated_at=session.updated_at,
      chats=chat_items,
    ),
  )
