from langgraph.types import interrupt
from pydantic import BaseModel, ConfigDict

from app.agent.state import AgentState
from app.agent.tools import make_list_projects_tools

class ProjectChoice(BaseModel):
  model_config = ConfigDict(extra="ignore")
  id: str
  name: str

class SelectProjectPrompt(BaseModel):
  model_config = ConfigDict(extra="ignore")
  action: str
  message: str
  projects: list[ProjectChoice]

class SelectProjectResponse(BaseModel):
  model_config = ConfigDict(extra="ignore")
  project_id: str | None = None
  project_name: str | None = None
  id: str | None = None
  name: str | None = None

def _normalize_projects(raw_projects: list[object] | None) -> list[dict[str, str]]:
  if not raw_projects:
    return []
  normalized: list[dict[str, str]] = []
  for item in raw_projects:
    if isinstance(item, dict):
      project_id = item.get("id")
      name = item.get("name")
      if isinstance(project_id, str) and isinstance(name, str):
        normalized.append({"id": project_id, "name": name})
  return normalized

def _extract_projects(result: dict[str, object]) -> list[dict[str, str]]:
  projects = result.get("projects")
  if isinstance(projects, list):
    return _normalize_projects(projects)
  project_id = result.get("id")
  name = result.get("name")
  if isinstance(project_id, str) and isinstance(name, str):
    return [{"id": project_id, "name": name}]
  return []

def _has_more_pages(result: dict[str, object], page: int, per_page: int, count: int) -> bool:
  page_context = result.get("page_context")
  if isinstance(page_context, dict):
    has_more = page_context.get("has_more_page")
    if isinstance(has_more, bool):
      return has_more
  return count == per_page and page < 100


async def setup_node(state: AgentState):
  if state.get("current_project_id") and state.get("current_project_name"):
    return {
      "current_project_id": state["current_project_id"],
      "current_project_name": state["current_project_name"]
    }

  tools = make_list_projects_tools(
    access_token=state["access_token"],
    portal_id=state["portal_id"]
  )

  list_projects_tool = tools[0]

  all_projects: list[dict[str, str]] = []
  page = 1
  per_page = 50

  while True:
    result = await list_projects_tool.ainvoke({"page": page, "per_page": per_page})
    if not isinstance(result, dict):
      raise RuntimeError("Unexpected list_projects response")
    page_projects = _extract_projects(result)
    all_projects.extend(page_projects)
    if not _has_more_pages(result, page, per_page, len(page_projects)):
      break
    page += 1

  if not all_projects:
    raise RuntimeError("No projects found to select")

  prompt = SelectProjectPrompt(
    action="select_project",
    message="Select a project for this session.",
    projects=[ProjectChoice(**project) for project in all_projects],
  )
  selection = interrupt(prompt.model_dump())

  selected_id: str | None = None
  selected_name: str | None = None

  if isinstance(selection, dict):
    parsed = SelectProjectResponse.model_validate(selection)
    selected_id = parsed.project_id or parsed.id
    selected_name = parsed.project_name or parsed.name
  elif isinstance(selection, str):
    selected_id = selection

  if not selected_id and selected_name:
    match = next((p for p in all_projects if p["name"] == selected_name), None)
    if match:
      selected_id = match["id"]

  if selected_id and not selected_name:
    match = next((p for p in all_projects if p["id"] == selected_id), None)
    if match:
      selected_name = match["name"]

  if not selected_id or not selected_name:
    raise RuntimeError("Project selection is required")

  return {
    "current_project_id": selected_id,
    "current_project_name": selected_name,
  }