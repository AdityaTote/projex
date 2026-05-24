from __future__ import annotations

from typing import Any
from uuid import UUID

from typing import cast

from app.agent.agent import run_graph
from app.agent.state import AgentState
from app.repository import session_repository

from .schema import ChatRequest, ChatResponse


def _message_role(msg: object) -> str:
  if isinstance(msg, dict):
    role = msg.get("role") or msg.get("type")
    return str(role) if role is not None else ""
  role = getattr(msg, "role", None) or getattr(msg, "type", None)
  return str(role) if role is not None else ""


def _message_content(msg: object) -> str:
  content = None
  if isinstance(msg, dict):
    content = msg.get("content")
  else:
    content = getattr(msg, "content", None)

  if isinstance(content, str):
    return content
  if isinstance(content, list):
    parts: list[str] = []
    for item in content:
      if isinstance(item, str):
        parts.append(item)
      elif isinstance(item, dict):
        text = item.get("text")
        if isinstance(text, str):
          parts.append(text)
    return " ".join(parts)
  return ""


def _normalize_title(message: str | None) -> str:
  if not message:
    return "New chat"
  title = " ".join(message.split())
  return title[:80] if title else "New chat"


class ChatService:
  @staticmethod
  async def run_chat(*, user_id: UUID, portal_id: int, access_token: str, payload: ChatRequest) -> ChatResponse:
    session_id = payload.session_id
    project_id = payload.project_id
    project_name = payload.project_name

    if session_id is None:
      session_id = session_repository.create_session(
        user_id=user_id,
        title=_normalize_title(payload.message),
        project_id=project_id,
      )
    else:
      session = session_repository.get_session_by_id(session_id)
      if session is None:
        raise RuntimeError("Session not found")
      if session.user_id != user_id:
        raise RuntimeError("Session not found")
      # Use project from existing session if not provided
      if not project_id and session.project_id:
        project_id = session.project_id

    input_payload = None
    if payload.resume is None:
      if not payload.message:
        raise RuntimeError("message is required when resume is not provided")
      state: dict[str, object] = {
        "user_id": user_id,
        "portal_id": portal_id,
        "access_token": access_token,
        "session_id": session_id,
        "messages": [
          {"role": "user", "content": payload.message}
        ],
      }
      # Inject project context so setup_node skips its fetch
      if project_id:
        state["current_project_id"] = project_id
      if project_name:
        state["current_project_name"] = project_name

      input_payload = cast(AgentState, state)

    result = await run_graph(
      input_payload=input_payload,
      thread_id=str(session_id),
      resume=payload.resume,
    )

    response_message = "Chat completed"
    if result.get("interrupts"):
      response_message = "Action required"

    state_value = result.get("value") or {}
    messages = state_value.get("messages", [])
    
    # Extract the last AI message content
    last_ai_message = ""
    for msg in reversed(messages):
      role = _message_role(msg).lower()
      if role in {"ai", "assistant"}:
        content = _message_content(msg)
        if content:
          last_ai_message = content
          break

    clean_output = {
      "reply": last_ai_message,
      "current_project_id": state_value.get("current_project_id"),
      "current_project_name": state_value.get("current_project_name"),
    }

    return ChatResponse(
      message=response_message,
      data={
        "session_id": session_id,
        "output": clean_output,
        "interrupts": result.get("interrupts") or [],
      },
    )
