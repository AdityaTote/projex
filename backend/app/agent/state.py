from typing import Annotated, Optional
from uuid import UUID
from typing_extensions import TypedDict
from enum import StrEnum

from langgraph.graph.message import add_messages

class Route(StrEnum):
  QUERY = "query"
  ACTION = "action"


class AgentState(TypedDict):
  # identity
  user_id: UUID
  portal_id: int
  access_token: str
  session_id: Optional[UUID]

  # project context
  current_project_id: Optional[str]
  current_project_name: Optional[str]

  # action context
  pending_action: Optional[dict]

  # conversation history
  messages: Annotated[list, add_messages]

  # router sets this, agents read it
  route: Optional[Route]

  # long-term memory
  long_term_context: Optional[dict]

  # output to show in UI, agents write to this
  output: Optional[dict]

  # index of last persisted message in chats table
  saved_count: Optional[int]