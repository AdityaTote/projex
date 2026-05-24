import logging
from urllib.parse import urlencode

import requests

from app.config import settings

from .schema import OAuthTokenResponse

logger = logging.getLogger(__name__)


class ZohoAuth:
  def __init__(self):
    self.client_id = settings.zoho_client_id
    self.client_secret = settings.zoho_client_secret
    self.access_type = settings.zoho_access_type
    self.redirect_uri = settings.zoho_redirect_uri
    self.base_url = settings.zoho_base_url
    self.scope = settings.zoho_scope

  def _request_json(self, url: str, data: dict[str, str]) -> dict[str, object]:
    logger.info("Zoho request → %s", url)
    res = requests.post(url, data=data)
    logger.info("Zoho response ← %s: %s", res.status_code, res.text[:500])
    if res.status_code >= 400:
      raise RuntimeError(f"Zoho Auth error {res.status_code}: {res.text}")
    try:
      return res.json()
    except ValueError:
      raise RuntimeError("Zoho Auth returned non-JSON response")

  def get_authorize_url(self):
    params = {
      "scope": self.scope,
      "client_id": self.client_id,
      "response_type": "code",
      "access_type": self.access_type,
      "redirect_uri": self.redirect_uri,
    }
    return f"{self.base_url}/auth?{urlencode(params)}"
  
  def generate_token(self, code: str) -> OAuthTokenResponse:
    params = {
      "code": code,
      "grant_type": "authorization_code",
      "client_id": self.client_id,
      "client_secret": self.client_secret,
      "redirect_uri": self.redirect_uri
    }
    data = self._request_json(f"{self.base_url}/token", params)
    return OAuthTokenResponse.model_validate(data)
    
  def refresh_token(self, refresh_token: str) -> OAuthTokenResponse:
    params = {
      "refresh_token": refresh_token,
      "grant_type": "refresh_token",
      "client_id": self.client_id,
      "client_secret": self.client_secret,
      "scope": self.scope,
      "redirect_uri": self.redirect_uri
    }
    data = self._request_json(f"{self.base_url}/token", params)
    return OAuthTokenResponse.model_validate(data)
  
  def revoke_token(self, token):
    params = {
      "token": token,
    }

    res = requests.post(f"{self.base_url}/revoke", data=params)

    if res.status_code == 200:
      return res.json()
    else:
      raise Exception(f"Failed to revoke token: {res.text}")
    
zoho_auth = ZohoAuth()