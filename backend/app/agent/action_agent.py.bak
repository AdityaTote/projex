import logging

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from app.agent.llm import llm
from app.agent.state import AgentState
from app.agent.tools import make_action_tools
from app.agent.prompt import ACTION_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

_FALLBACK = (
  "<response><message>I didn't receive a message to act on. "
  "Could you please repeat your request?</message>"
  "<action>none</action><payload></payload></response>"
)


def _has_user_content(messages: list) -> bool:
  """Return True if at least one HumanMessage with non-empty content exists."""
  return any(
    getattr(msg, "type", None) == "human" and getattr(msg, "content", None)
    for msg in messages
  )


def _trim_to_last_user(messages: list) -> list:
  """Keep only messages from the last HumanMessage onward.

  When the full checkpoint history is passed to Google GenAI, stale
  tool-call / tool-result pairs from earlier turns can violate the
  strict role-ordering the SDK expects.  Trimming to the last user
  turn gives the model the current question plus any recent tool
  context while avoiding format errors.
  """
  last_human_idx = None
  for i in range(len(messages) - 1, -1, -1):
    if getattr(messages[i], "type", None) == "human":
      last_human_idx = i
      break
  if last_human_idx is not None:
    return messages[last_human_idx:]
  return messages


async def action_agent_node(state: AgentState):
  state_messages = list(state.get("messages") or [])

  # Google GenAI requires at least one user content message beyond the
  # system instruction.  Without a HumanMessage the SDK raises
  # "contents are required".
  if not state_messages or not _has_user_content(state_messages):
    logger.warning(
      "action_agent: no user content in %d message(s), returning fallback. "
      "types=%s",
      len(state_messages),
      [getattr(m, "type", type(m).__name__) for m in state_messages],
    )
    return {
      "messages": [AIMessage(content=_FALLBACK)],
      "route": None,
    }

  tools = make_action_tools(
    access_token=state.get("access_token"),
    portal_id=state.get("portal_id")
  )

  agent = llm.bind_tools(tools)
  tool_node = ToolNode(tools)

  formatted_action_prompt = ACTION_SYSTEM_PROMPT.format(
    current_project_name=state.get("current_project_name") or "none",
    current_project_id=state.get("current_project_id") or "none",
    user_id=state["user_id"]
  )

  # Trim conversation history to the last user message to avoid
  # role-ordering issues that cause Google GenAI to reject the request.
  trimmed = _trim_to_last_user(state_messages)
  llm_messages = [SystemMessage(content=formatted_action_prompt)] + trimmed
  new_messages = []

  logger.info(
    "action_agent: invoking LLM with %d messages (trimmed from %d). "
    "types=%s",
    len(llm_messages),
    len(state_messages) + 1,
    [getattr(m, "type", type(m).__name__) for m in llm_messages],
  )

  while True:
    try:
      response: AIMessage = await agent.ainvoke(llm_messages)
    except ValueError as e:
      if "contents are required" in str(e):
        logger.error(
          "action_agent: Google GenAI rejected messages. count=%d types=%s",
          len(llm_messages),
          [(getattr(m, "type", type(m).__name__), bool(getattr(m, "content", "")))
           for m in llm_messages],
        )
        return {
          "messages": [AIMessage(content=_FALLBACK)],
          "route": None,
        }
      raise

    llm_messages = llm_messages + [response]
    new_messages.append(response)

    if not response.tool_calls:
      break

    try:
      tool_result = await tool_node.ainvoke({"messages": llm_messages})
      result_msgs = tool_result["messages"]

      # Extract only the NEW messages produced by the tool node
      if len(result_msgs) > len(llm_messages):
        tool_messages = result_msgs[len(llm_messages):]
        llm_messages = result_msgs
      else:
        # ToolNode returned the same or fewer messages; the last
        # message(s) after the original prefix are the tool responses.
        tool_messages = result_msgs[len(llm_messages) - len(response.tool_calls):]
        llm_messages = llm_messages + tool_messages

      new_messages.extend(tool_messages)

    except RuntimeError as e:
      if "not approved" in str(e):
        cancel_response = AIMessage(
          content="<response><message>Action cancelled.</message><action>none</action><payload></payload></response>"
        )
        new_messages.append(cancel_response)
        break
      raise

  return {
    "messages": new_messages,
    "route": None
  }