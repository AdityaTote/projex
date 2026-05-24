from app.agent.state import AgentState
from app.repository import chat_repository


def _message_role(msg: object) -> str:
  if isinstance(msg, dict):
    role = msg.get("role") or msg.get("type")
    return str(role).lower() if role is not None else ""
  role = getattr(msg, "role", None) or getattr(msg, "type", None)
  return str(role).lower() if role is not None else ""


def _normalize_role(role: str) -> str:
  if role in {"user", "assistant", "system"}:
    return role
  if role == "human":
    return "user"
  if role == "ai":
    return "assistant"
  return ""


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


def save_message(state: AgentState):
  session_id = state.get("session_id")
  if session_id is None:
    return {}

  messages = list(state.get("messages") or [])
  if not messages:
    return {}

  saved_count = state.get("saved_count")
  if not isinstance(saved_count, int) or saved_count < 0:
    saved_count = 0
  if saved_count > len(messages):
    saved_count = 0

  new_messages = messages[saved_count:]
  saved_any = False
  for msg in new_messages:
    role = _normalize_role(_message_role(msg))
    if not role:
      continue

    content = _message_content(msg)
    if not content:
      continue

    chat_repository.create_chat(
      session_id=session_id,
      role=role,
      content=content,
    )
    saved_any = True

  if not saved_any:
    return {"saved_count": len(messages)}

  return {"saved_count": len(messages)}