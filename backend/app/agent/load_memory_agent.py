from app.agent.state import AgentState
from app.repository import session_repository, user_repository

def load_memory(state: AgentState):
  user_data = user_repository.get_user_by_id(state["user_id"])
  
  if state["session_id"]:
    session_data = session_repository.get_session_by_id(state["session_id"])
    if session_data:
      chats = session_data.chats
  
  if not user_data:
    return {
      "user_id": state["user_id"],
    }

  return {
    "portal_id": user_data.portal_id,
    "access_token": user_data.access_token,
    "project_id": session_data.project_id if session_data else None,
  }