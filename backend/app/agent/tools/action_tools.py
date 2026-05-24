from typing import Any

from langchain.tools import tool
from langgraph.types import interrupt

from app.zoho import zoho


def make_action_tools(access_token: str, portal_id: int):

  #TODO: whether to add access_token and portal_id as args or fetch it from db or from state
  def _require_approval(action: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = interrupt({
      "action": action,
      "payload": payload,
      "message": "Approve this action?",
    })

    print("approval: action=", action, "response=", response)

    approved = False
    final_payload = payload
    if isinstance(response, dict):
      if "approved" in response:
        approved = bool(response.get("approved"))
      elif response.get("action") in {"approve", "approved", "proceed"}:
        approved = True

      updated_payload = response.get("payload")
      if isinstance(updated_payload, dict):
        final_payload = {**payload, **updated_payload}
    else:
      approved = bool(response)

    print("approval: approved=", approved, "final_payload=", final_payload)

    if not approved:
      raise RuntimeError("Action not approved")

    return final_payload


  @tool()
  def create_task(project_id: str, task_data: dict[str, Any]) -> dict[str, Any]:
    """
      Create a task in Zoho Projects.

      Args:
        project_id: Project ID where the task will be created. This MUST be the numerical ID, NOT the project name. Use list_projects first if needed.
        task_data: Task payload matching TaskCreate. Fields:
          - name (str, required)
          - description (str, optional)
          - tasklist (TaskListRef, optional)
          - parental_info (ParentInfo, optional)
          - status (StatusRef, optional)
          - priority (str, optional)
          - start_date (str, optional, format: YYYY-MM-DD)
          - end_date (str, optional, format: YYYY-MM-DD)
          - duration (Duration, optional)
          - completion_percentage (str, optional)
          - billing_type (str, optional)
          - attachments (List[int], optional)
          - owners_and_work (OwnersAndWork, optional)
          - tags (List[TagEntry], optional)
          - teams (List[TeamEntry], optional)
          - recurrence (Recurrence, optional)
          - budget_info (BudgetInfo, optional)

      Returns:
        TaskCreateResponse-like dict from the Zoho API.
    """
    if not isinstance(task_data, dict):
      raise ValueError("task_data must be a dict")

    approval_payload = _require_approval(
      "create_task",
      {
        "portal_id": portal_id,
        "project_id": project_id,
        "task_data": task_data,
      },
    )

    final_project_id = approval_payload.get("project_id", project_id)
    final_task_data = approval_payload.get("task_data", task_data)
    if not isinstance(final_task_data, dict):
      raise ValueError("task_data must be a dict")
    name = final_task_data.get("name")
    if not isinstance(name, str) or not name.strip():
      raise ValueError("task_data.name is required and must be a non-empty string")

    data = zoho.create_task(access_token, portal_id, final_project_id, final_task_data)
    if not data:
      #TODO: better error handling
      raise RuntimeError("Zoho API error: empty response")
    return data.model_dump()

  @tool()
  def update_task(project_id: str, task_id: str, task_data: dict[str, Any]) -> dict[str, Any]:
    """
      Update a task in Zoho Projects.

      Args:
        project_id: Project ID where the task exists. This MUST be the numerical ID, NOT the project name.
        task_id: Task ID to update.
        task_data: Task payload matching TaskUpdate. Fields:
          - tasklist (TaskListRef, optional)
          - parental_info (ParentInfo, optional)
          - name (str, optional)
          - description (str, optional)
          - status (StatusRef, optional)
          - priority (str, optional)
          - start_date (str, optional, format: YYYY-MM-DD)
          - end_date (str, optional, format: YYYY-MM-DD)
          - duration (Duration, optional)
          - completion_percentage (str, optional)
          - billing_type (str, optional)
          - attachments (List[int], optional)
          - owners_and_work (OwnersAndWork, optional)
          - tags (List[TagEntry], optional)
          - teams (List[TeamEntry], optional)
          - recurrence (Recurrence, optional)
          - budget_info (BudgetInfo, optional)

      Returns:
        TaskUpdateResponse-like dict from the Zoho API.
      """
    if not isinstance(task_data, dict):
      raise ValueError("task_data must be a dict")

    approval_payload = _require_approval(
      "update_task",
      {
        "portal_id": portal_id,
        "project_id": project_id,
        "task_id": task_id,
        "task_data": task_data,
      },
    )

    final_project_id = approval_payload.get("project_id", project_id)
    final_task_id = approval_payload.get("task_id", task_id)
    final_task_data = approval_payload.get("task_data", task_data)
    if not isinstance(final_task_data, dict):
      raise ValueError("task_data must be a dict")

    data = zoho.update_task(
      access_token,
      portal_id,
      final_project_id,
      final_task_id,
      final_task_data,
    )
    if not data:
      #TODO: better error handling
      raise RuntimeError("Zoho API error: empty response")
    return data.model_dump()

  @tool()
  def delete_task(project_id: str, task_id: str) -> dict[str, Any]:
    """
      Delete a task in Zoho Projects.

      Args:
        project_id: Project ID where the task exists. This MUST be the numerical ID, NOT the project name.
        task_id: Task ID to delete.

      Returns:
        TaskDeleteResponse-like dict from the Zoho API.
      """
    approval_payload = _require_approval(
      "delete_task",
      {
        "portal_id": portal_id,
        "project_id": project_id,
        "task_id": task_id,
      },
    )

    final_project_id = approval_payload.get("project_id", project_id)
    final_task_id = approval_payload.get("task_id", task_id)

    data = zoho.delete_task(access_token, portal_id, final_project_id, final_task_id)
    if data is None:
      return {"status": "success", "message": "Task deleted successfully (empty response)"}
    return data.model_dump()

  @tool()
  def delete_task_by_name(project_id: str, task_name: str) -> dict[str, Any]:
    """
      Delete a task in Zoho Projects by its name.

      Args:
        project_id: Project ID where the task exists. This MUST be the numerical ID, NOT the project name.
        task_name: Exact task name to delete.

      Returns:
        TaskDeleteResponse-like dict from the Zoho API.
    """
    if not isinstance(task_name, str) or not task_name.strip():
      raise ValueError("task_name is required and must be a non-empty string")

    tasks_response = zoho.list_tasks(access_token, portal_id, project_id, page=1, per_page=200)
    tasks = tasks_response.tasks or []

    normalized = task_name.strip().lower()
    matches = [task for task in tasks if (task.name or "").strip().lower() == normalized]

    if not matches:
      raise RuntimeError("No task found with that name in the project")
    if len(matches) > 1:
      options = [
        {"id": task.id, "name": task.name}
        for task in matches
        if task.id and task.name
      ]
      selection = interrupt({
        "action": "select_task",
        "message": "Multiple tasks match that name. Select a task to delete.",
        "options": options,
      })
      if isinstance(selection, dict):
        selected_id = selection.get("task_id") or selection.get("id")
      else:
        selected_id = selection
      if isinstance(selected_id, str) and selected_id.strip():
        task_id = selected_id
      else:
        raise RuntimeError("Task selection is required")
    else:
      task_id = matches[0].id
    if not task_id:
      raise RuntimeError("Matched task is missing an id")

    approval_payload = _require_approval(
      "delete_task",
      {
        "portal_id": portal_id,
        "project_id": project_id,
        "task_id": task_id,
        "task_name": task_name,
      },
    )

    final_project_id = approval_payload.get("project_id", project_id)
    final_task_id = approval_payload.get("task_id", task_id)

    data = zoho.delete_task(access_token, portal_id, final_project_id, final_task_id)
    if data is None:
      return {"status": "success", "message": "Task deleted successfully (empty response)"}
    return data.model_dump()

  return [
    create_task,
    update_task,
    delete_task,
    delete_task_by_name,
  ]