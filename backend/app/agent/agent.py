from typing import Any, cast

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from .state import AgentState
from .load_memory_agent import load_memory
from .save_message_agent import save_message
from .router_agent import router
from .action_agent import action_agent_node
from .query_agent import query_agent_node
from .setup_agent import setup_node

checkpointer = InMemorySaver()

def _route_after_router(state: AgentState) -> str:
  return state.get("route", "query")

def build_graph():
  graph = StateGraph(AgentState)

  graph.add_node("load_memory", load_memory)
  graph.add_node("setup", setup_node)
  graph.add_node("router", router)
  graph.add_node("action_agent", action_agent_node)
  graph.add_node("query_agent", query_agent_node)
  graph.add_node("save_message", save_message)

  graph.add_edge(START, "load_memory")
  
  graph.add_edge("load_memory", "setup")
  graph.add_edge("setup", "router")
  graph.add_conditional_edges(
    "router",
    _route_after_router,
    {
			"query": "query_agent",
			"action": "action_agent"
		}
  )
  graph.add_edge("query_agent", "save_message")
  graph.add_edge("action_agent", "save_message")
  
  graph.add_edge("save_message", END)

  return graph

def graph_config():
  return  build_graph().compile(checkpointer=checkpointer)

async def run_graph(
  *,
  input_payload: AgentState | None,
  thread_id: str,
  resume: Any | None = None,
) -> dict[str, object]:
  graph = graph_config()
  config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

  if resume is not None:
    result = await graph.ainvoke(
      Command(resume=resume),
      config=config,
      version="v2",
    )
  else:
    if input_payload is None:
      raise ValueError("input_payload is required for initial runs")
    payload = cast(AgentState, input_payload)
    result = await graph.ainvoke(
      payload,
      config=config,
      version="v2",
    )

  return {
    "value": result.value,
    "interrupts": [interrupt.value for interrupt in result.interrupts],
  }
