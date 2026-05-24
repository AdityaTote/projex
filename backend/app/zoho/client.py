import json
from typing import Any, Literal, cast
import requests

from app.config import settings

from .schema import (
  CustomRange,
  DeleteTaskResponse,
  GetPortalIdResponse,
  ListProjectMembersResponse,
  ListProjectsResponse,
  ListTasksResponse,
  MemberFilter,
  ProjectItem,
  ReportFilter,
  TaskCreate,
  TaskCreateResponse,
  TaskDetailResponse,
  TaskFilter,
  TaskUpdate,
  TaskUpdateResponse,
  TimesheetReportResponse,
)

JsonType = dict[str, "JsonType"] | list["JsonType"] | str | int | float | bool | None

class ZohoClient:
  def __init__(self):
    self.base_url = settings.zoho_projects_base_url

  def _request_json(self, method: str, url: str, **kwargs: Any) -> JsonType:
    res = requests.request(method, url, **kwargs)
    if res.status_code >= 400:
      raise RuntimeError(f"Zoho API error {res.status_code}: {res.text}")
    if not res.content:
      return None
    try:
      return res.json()
    except ValueError:
      raise RuntimeError("Zoho API returned non-JSON response")

  def get_portal_id(self, access_token: str) -> GetPortalIdResponse:
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    data = self._request_json("GET", self.base_url + "/portals", headers=headers)
    if isinstance(data, dict) and "portals" in data and isinstance(data["portals"], list) and data["portals"]:
      return GetPortalIdResponse(portal_details=data["portals"][0])
    if isinstance(data, list) and data:
      return GetPortalIdResponse(portal_details=data[0])
    return GetPortalIdResponse.model_validate(data)

  def list_projects(
    self,
    access_token: str,
    portal_id: int,
    page: int = 1,
    per_page: int = 10,
  ) -> ListProjectsResponse | ProjectItem:
    params = {
      "page": page,
      "per_page": per_page
    }
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    data = self._request_json(
      "GET",
      self.base_url + f"/portal/{portal_id}/projects",
      headers=headers,
      params=params,
    )
    if isinstance(data, dict) and "projects" in data:
      return ListProjectsResponse.model_validate(data)
    if isinstance(data, list):
      return ListProjectsResponse(projects=data)
    return ProjectItem.model_validate(data)
  
  def list_tasks(
    self,
    access_token: str,
    portal_id: int,
    project_id: str,
    page: int = 1,
    per_page: int = 100,
    sort_by: Literal[
      "ASC(id)",
      "ASC(name)",
      "ASC(start_date)",
      "ASC(end_date)",
      "ASC(completion_percentage)",
      "ASC(created_time)",
      "ASC(last_modified_time)",
      "ASC(created_by)",
      "ASC(is_completed)",
      "DESC(id)",
      "DESC(name)",
      "DESC(start_date)",
      "DESC(end_date)",
      "DESC(completion_percentage)",
      "DESC(created_time)",
      "DESC(last_modified_time)",
      "DESC(created_by)",
      "DESC(is_completed)",
    ] | None = None,
    view_id: int | None = None,
    filter_criteria: "TaskFilter | None" = None,
  ) -> ListTasksResponse:
    params: dict[str, str | int | float | bool] = {
      "page": page,
      "per_page": per_page
    }
    if sort_by:
      params["sort_by"] = sort_by
    if view_id:
      params["view_id"] = view_id
    if filter_criteria:
      params["filter"] = json.dumps(filter_criteria)
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    data = self._request_json(
      "GET",
      self.base_url + f"/portal/{portal_id}/projects/{project_id}/tasks",
      headers=headers,
      params=params,
    )
    return ListTasksResponse.model_validate(data)
  
  def get_task_details(self, access_token: str, portal_id: str, project_id: str, task_id: str) -> TaskDetailResponse:
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    data = self._request_json(
      "GET",
      self.base_url + f"/portal/{portal_id}/projects/{project_id}/tasks/{task_id}",
      headers=headers,
    )
    return TaskDetailResponse.model_validate(data)
  
  def create_task(
    self,
    access_token: str,
    portal_id: int,
    project_id: str,
    task_data: TaskCreate | dict[str, object],
  ) -> TaskCreateResponse:
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    payload = (
      task_data.model_dump(exclude_none=True)
      if isinstance(task_data, TaskCreate)
      else task_data
    )
    payload = cast(JsonType, payload)
    data = self._request_json(
      "POST",
      self.base_url + f"/portal/{portal_id}/projects/{project_id}/tasks",
      headers=headers,
      json=payload,
    )
    return TaskCreateResponse.model_validate(data)
  
  def update_task(
    self,
    access_token: str,
    portal_id: int,
    project_id: str,
    task_id: str,
    task_data: TaskUpdate | dict[str, object],
  ) -> TaskUpdateResponse:
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    payload = (
      task_data.model_dump(exclude_none=True)
      if isinstance(task_data, TaskUpdate)
      else task_data
    )
    payload = cast(JsonType, payload)
    data = self._request_json(
      "PATCH",
      self.base_url + f"/portal/{portal_id}/projects/{project_id}/tasks/{task_id}",
      headers=headers,
      json=payload,
    )
    return TaskUpdateResponse.model_validate(data)
  
  def delete_task(self, access_token: str, portal_id: int, project_id: str, task_id: str) -> DeleteTaskResponse | None:
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    data = self._request_json(
      "DELETE",
      self.base_url + f"/portal/{portal_id}/projects/{project_id}/tasks/{task_id}",
      headers=headers,
    )
    if data is None:
      return None
    return DeleteTaskResponse.model_validate(data)
  
  def list_project_members(
    self,
    access_token: str,
    portal_id: int,
    project_id: str,
    type: str | None = None,
    view_type: str | None = None,
    sort: str | None = None,
    page: int = 1,
    per_page: int = 10,
    filter_criteria: "MemberFilter | None" = None,
    ids: str | None = None,
    company_ids: str | None = None,
  ) -> ListProjectMembersResponse:
    params: dict[str, str | int | float | bool] = {
      "page": page,
      "per_page": per_page,
    }
    if type:
      params["type"] = type
    if view_type:
      params["view_type"] = view_type
    if sort:
      params["sort"] = sort
    if filter_criteria:
      params["filter"] = json.dumps(filter_criteria)
    if ids:
      params["ids"] = ids
    if company_ids:
      params["company_ids"] = company_ids
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    data = self._request_json(
      "GET",
      self.base_url + f"/portal/{portal_id}/projects/{project_id}/users",
      headers=headers,
      params=params,
    )
    return ListProjectMembersResponse.model_validate(data)

  def get_timesheet_report(
    self,
    access_token: str,
    portal_id: int,
    project_id: str,
    report_type: str,
    view_type: str,
    start_date: str,
    page: int = 1,
    per_page: int = 10,
    filter_criteria: "ReportFilter | None" = None,
    view_id: str | None = None,
    timelog_group_id: str | None = None,
    custom_range: "CustomRange | None" = None,
    frompage: str | None = None,
    use_timelogs: bool = False,
  ) -> TimesheetReportResponse:
    params: dict[str, str | int | float | bool] = {
      "page": page,
      "per_page": per_page,
      "report_type": report_type,
      "view_type": view_type,
      "start_date": start_date,
    }
    if filter_criteria:
      params["filter"] = json.dumps(filter_criteria)
    if view_id:
      params["view_id"] = view_id
    if timelog_group_id:
      params["timelog_group_id"] = timelog_group_id
    if custom_range:
      params["custom_range"] = json.dumps(custom_range)
    if frompage:
      params["frompage"] = frompage
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    endpoint = "timelogs" if use_timelogs else "timesheet"
    data = self._request_json(
      "GET",
      self.base_url + f"/portal/{portal_id}/projects/{project_id}/{endpoint}/report",
      headers=headers,
      params=params,
    )
    return TimesheetReportResponse.model_validate(data)

zoho = ZohoClient()