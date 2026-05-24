from langchain.tools import tool

from app.zoho import zoho

def make_query_tools(access_token: str, portal_id: int):
  @tool()
  def list_projects(page: int = 1, per_page: int = 20) -> dict[str, object]:
    """
      List projects in Zoho Projects.

      Args:
          page: Page number for pagination (optional).
          per_page: Number of items per page for pagination (optional).

      Returns:
          List of projects as returned by the Zoho API.
    """

    data = zoho.list_projects(access_token, portal_id, page, per_page)
    if not data:
      raise RuntimeError("Zoho API error: empty response")
    return data.model_dump()

  @tool()
  def list_tasks(project_id: str, page: int = 1, per_page: int = 100) -> dict[str, object]:
    """
      List tasks in a Zoho Projects project.

      Args:
          project_id: Project ID to list tasks from. This MUST be the numerical ID (e.g. '12345'), NOT the project name. Use list_projects first to find the ID.
          page: Page number for pagination (optional).
          per_page: Number of items per page for pagination (optional).

      Returns:
          List of tasks as returned by the Zoho API.
    """
    print(
      "list_tasks: project_id=",
      project_id,
      "page=",
      page,
      "per_page=",
      per_page,
    )
    data = zoho.list_tasks(access_token, portal_id, project_id, page, per_page)
    if not data:
      raise RuntimeError("Zoho API error: empty response")
    tasks = getattr(data, "tasks", None)
    print(
      "list_tasks: returned_count=",
      len(tasks) if isinstance(tasks, list) else "unknown",
    )
    return data.model_dump()


  @tool()
  def get_task_details(project_id: str, task_id: str) -> dict[str, object]:
    """
      Get details of a task in Zoho Projects.

      Args:
          project_id: Project ID where the task exists. This MUST be the numerical ID, NOT the project name.
          task_id: Task ID to get details for.

      Returns:
          Task details as returned by the Zoho API.
    """
    data = zoho.get_task_details(access_token, portal_id, project_id, task_id)
    if not data:
      raise RuntimeError("Zoho API error: empty response")
    return data.model_dump()


  @tool()
  def list_project_members(project_id: str) -> dict[str, object]:
    """
      List members of a Zoho Projects project.

      Args:
          project_id: Project ID to list members from. This MUST be the numerical ID, NOT the project name.

      Returns:
          List of project members as returned by the Zoho API.
    """
    data = zoho.list_project_members(access_token, portal_id, project_id)
    if not data:
      raise RuntimeError("Zoho API error: empty response")
    return data.model_dump()

  @tool()
  def get_task_utilization(
    project_id: str,
    report_type: str,
    view_type: str,
    start_date: str,
    page: int = 1,
    per_page: int = 10,
    filter_criteria: dict[str, object] | None = None,
    view_id: str | None = None,
    timelog_group_id: str | None = None,
    custom_range: dict[str, object] | None = None,
    frompage: str | None = None,
    use_timelogs: bool = False,
  ) -> dict[str, object]:
    """
      Get task utilization (timesheet) report for a Zoho Projects project.

      Args:
          project_id: Project ID to get the report for. This MUST be the numerical ID, NOT the project name.
          report_type: Report type string expected by Zoho (required).
          view_type: Report view type string expected by Zoho (required).
          start_date: Report start date in YYYY-MM-DD format.
          page: Page number for pagination (optional).
          per_page: Number of items per page (optional).
          filter_criteria: Filter payload for the report (optional).
          view_id: Saved view ID to apply (optional).
          timelog_group_id: Timelog group ID to filter by (optional).
          custom_range: Custom date range payload (optional).
          frompage: Report source page hint (optional).
          use_timelogs: Whether to use the timelogs endpoint instead of timesheet (optional).

      Returns:
          Task utilization report as returned by the Zoho API.
    """
    data = zoho.get_timesheet_report(
      access_token,
      portal_id,
      project_id,
      report_type,
      view_type,
      start_date,
      page=page,
      per_page=per_page,
      filter_criteria=filter_criteria,
      view_id=view_id,
      timelog_group_id=timelog_group_id,
      custom_range=custom_range,
      frompage=frompage,
      use_timelogs=use_timelogs,
    )
    if not data:
      raise RuntimeError("Zoho API error: empty response")
    return data.model_dump()
  
  return [
    list_projects,
    list_tasks,
    get_task_details,
    list_project_members,
    get_task_utilization,
  ]