import logging

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode

from app.agent.llm import llm
from app.agent.prompt import QUERY_SYSTEM_PROMPT
from app.agent.state import AgentState
from app.agent.tools import make_query_tools

logger = logging.getLogger(__name__)


def _has_user_content(messages: list) -> bool:
  """Return True if at least one HumanMessage with non-empty content exists."""
  return any(
    getattr(msg, "type", None) == "human" and getattr(msg, "content", None)
    for msg in messages
  )


def _trim_to_last_user(messages: list) -> list:
  """Keep only messages from the last HumanMessage onward."""
  last_human_idx = None
  for i in range(len(messages) - 1, -1, -1):
    if getattr(messages[i], "type", None) == "human":
      last_human_idx = i
      break
  if last_human_idx is not None:
    return messages[last_human_idx:]
  return messages


def _message_kind(message: object) -> str:
  if isinstance(message, dict):
    kind = message.get("type") or message.get("role")
    return str(kind) if kind is not None else ""
  kind = getattr(message, "type", None) or getattr(message, "role", None)
  return str(kind) if kind is not None else ""


async def query_agent_node(state: AgentState):
  state_messages = list(state.get("messages") or [])

  if not state_messages or not _has_user_content(state_messages):
    logger.warning(
      "query_agent: no user content in %d message(s), returning fallback. "
      "types=%s",
      len(state_messages),
      [getattr(m, "type", type(m).__name__) for m in state_messages],
    )
    return {
      "messages": [
        AIMessage(
          content="I didn't receive a message. Could you please repeat your request?"
        )
      ],
      "route": None,
    }

  tools = make_query_tools(
    access_token=state["access_token"],
    portal_id=state["portal_id"]
  )
  
  agent = llm.bind_tools(tools)
  tool_node = ToolNode(tools)

  formatted_query_prompt = QUERY_SYSTEM_PROMPT.format(
    current_project_name=state.get("current_project_name") or "none",
    current_project_id=state.get("current_project_id") or "none",
    user_id=state["user_id"]
  )
  
  trimmed = _trim_to_last_user(state_messages)
  llm_messages = [SystemMessage(content=formatted_query_prompt)] + trimmed

  logger.info(
    "query_agent: invoking LLM with %d messages (trimmed from %d). "
    "types=%s",
    len(llm_messages),
    len(state_messages) + 1,
    [getattr(m, "type", type(m).__name__) for m in llm_messages],
  )
  
  new_messages = []
  while True:
    try:
      response: AIMessage = await agent.ainvoke(llm_messages)
    except ValueError as e:
      if "contents are required" in str(e):
        logger.error(
          "query_agent: Google GenAI rejected messages. count=%d types=%s",
          len(llm_messages),
          [(getattr(m, "type", type(m).__name__), bool(getattr(m, "content", "")))
           for m in llm_messages],
        )
        return {
          "messages": [
            AIMessage(content="Something went wrong. Could you please try again?")
          ],
          "route": None,
        }
      raise

    llm_messages = llm_messages + [response]
    new_messages.append(response)
    
    if not response.tool_calls:
      break
    print(
      "query_agent: tool calls=",
      [call.get("name") for call in response.tool_calls],
    )
        
    try:
      tool_result = await tool_node.ainvoke({"messages": llm_messages})
    except Exception as e:
      raise e

    result_msgs = tool_result["messages"]
    tool_messages = []

    if result_msgs and all(_message_kind(msg).lower() == "tool" for msg in result_msgs):
      tool_messages = result_msgs
      llm_messages = llm_messages + tool_messages
    elif len(result_msgs) > len(llm_messages):
      tool_messages = result_msgs[len(llm_messages):]
      llm_messages = result_msgs
    else:
      start_idx = max(len(llm_messages) - len(response.tool_calls), 0)
      tool_messages = result_msgs[start_idx:]
      llm_messages = llm_messages + tool_messages

    new_messages.extend(tool_messages)
    print(
      "query_agent: tool results=",
      len(tool_messages),
      "new_messages=",
      len(new_messages),
    )
  
  return {
    "messages": new_messages,
    "route": None
  }
