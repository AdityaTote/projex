from langchain.tools import tool

from app.zoho import zoho

def make_list_projects_tools(access_token: str, portal_id: int):
  @tool()
  def list_projects(page: int = 1, per_page: int = 20) -> dict[str, object]:
    """
      List projects in Zoho Projects.

      Args:
          access_token: OAuth access token.
          portal_id: Portal ID to list projects from.
          page: Page number for pagination (optional).
          per_page: Number of items per page for pagination (optional).

      Returns:
          List of projects as returned by the Zoho API.
    """

    data = zoho.list_projects(access_token, portal_id, page, per_page)
    if not data:
      raise RuntimeError("Zoho API error: empty response")
    return data.model_dump()

  return [list_projects]