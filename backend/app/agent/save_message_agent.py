from app.agent.state import AgentState
from app.repository import chat_repository

def save_message(state: AgentState):
  last_message = state.get("messages")[-1] if state.get("messages") else None
  session_id = state.get("session_id")
  if last_message and session_id is not None:
    msg_type = getattr(last_message, "type", "")
    if msg_type == "human":
      role = "user"
    elif msg_type == "ai":
      role = "assistant"
    elif msg_type == "system":
      role = "system"
    else:
      return {}
      
    content = last_message.content
    if not isinstance(content, str):
      content = str(content)

    chats = chat_repository.create_chat(
      session_id=session_id,
      role=role,
      content=content,
    )
    if not chats:
      return {}

  return {}