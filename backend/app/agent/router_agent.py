import re

from langchain_core.messages import HumanMessage, SystemMessage

from .llm import llm
from .prompt.router_agent_prompt import ROUTER_PROMPT
from .state import AgentState, Route

def _response_content_to_str(content: str | list[str | dict]) -> str:
  if isinstance(content, str):
    return content

  parts: list[str] = []
  for item in content:
    if isinstance(item, str):
      parts.append(item)
    elif isinstance(item, dict):
      text = item.get("text")
      if isinstance(text, str):
        parts.append(text)

  return " ".join(parts)

def _parse_route(response: str) -> Route:
  response_clean = response.strip().lower()
  
  match = re.search(r"<route>\s*(query|action)\s*</route>", response_clean)
  if match:
    return Route(match.group(1))
    
  if "action" in response_clean and "query" not in response_clean:
    return Route.ACTION
  
  return Route.QUERY

async def router(state: AgentState):
  if not state.get("messages"):
    return {"route": Route.QUERY}

  last_message = state["messages"][-1].content

  response = await llm.ainvoke([
    SystemMessage(content=ROUTER_PROMPT),
    HumanMessage(content=last_message)
  ])

  content = _response_content_to_str(response.content)
  route = _parse_route(content)

  return {
    "route": route.value
  }
