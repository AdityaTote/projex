from datetime import datetime, timedelta, timezone

from app.repository import user_repository
from app.zoho import zoho, zoho_auth

from .schema import AuthCallbackData, AuthCallbackResponse, MeData
from .security import create_access_token


class AuthService:
  @staticmethod
  def get_authorize_url() -> str:
    return zoho_auth.get_authorize_url()

  @staticmethod
  def handle_callback(code: str) -> AuthCallbackResponse:
    token = zoho_auth.generate_token(code)
    access_token = token.access_token
    if not access_token:
      raise RuntimeError("Zoho auth response missing access_token")

    portal_response = zoho.get_portal_id(access_token)
    portal_details = portal_response.portal_details
    if portal_details is None:
      raise RuntimeError("Zoho portal details missing")

    owner = portal_details.owner
    if owner is None:
      raise RuntimeError("Zoho portal owner missing")

    email = owner.email or ""
    name = owner.full_name or owner.name or ""
    portal_id = portal_details.id or 0

    user_id = user_repository.create_user(email=email, name=name, portal_id=portal_id)

    expires_seconds = token.expires_in_sec or token.expires_in
    expires_at = None
    if expires_seconds:
      expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_seconds)

    user_repository.upsert_token(
      user_id=user_id,
      access_token=access_token,
      refresh_token=token.refresh_token,
      expires_at=expires_at,
    )

    jwt_token = create_access_token(user_id)
    return AuthCallbackResponse(
      message="Authentication successful",
      data=AuthCallbackData(
        access_token=jwt_token,
        user=MeData(
          id=user_id,
          email=email,
          name=name,
          portal_id=portal_id,
        ),
      ),
    )