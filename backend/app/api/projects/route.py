from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth.deps import get_current_user
from app.zoho import zoho

from .schema import ProjectListItem, ProjectsResponse

projects_router = APIRouter()


@projects_router.get("/", response_model=ProjectsResponse)
def list_projects(user=Depends(get_current_user)):
  if not user.access_token:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="User is missing Zoho access token",
    )

  try:
    result = zoho.list_projects(
      access_token=user.access_token,
      portal_id=user.portal_id,
      page=1,
      per_page=100,
    )
  except RuntimeError as exc:
    raise HTTPException(
      status_code=status.HTTP_502_BAD_GATEWAY,
      detail=str(exc),
    )

  # Normalize: result could be ListProjectsResponse or a single ProjectItem
  raw_projects = []
  if hasattr(result, "projects") and result.projects:
    raw_projects = result.projects
  elif hasattr(result, "id"):
    raw_projects = [result]

  items = [
    ProjectListItem(
      id=p.id or "",
      name=p.name or "Untitled",
      status=p.status.name if p.status else None,
    )
    for p in raw_projects
    if p.id
  ]

  return ProjectsResponse(
    message="Projects retrieved",
    data=items,
  )
