from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.zoho import zoho_auth
from app.repository import user_repository

from .deps import get_current_user
from .schema import (
	AuthCallbackResponse,
	AuthUrlData,
	AuthUrlResponse,
	LogoutData,
	LogoutResponse,
	MeData,
	MeResponse,
)
from .service import AuthService

auth_router = APIRouter()


@auth_router.get("/url", response_model=AuthUrlResponse)
def get_authorize_url():
	authorize_url = AuthService.get_authorize_url()
	return AuthUrlResponse(
		message="Authorization URL generated",
		data=AuthUrlData(authorize_url=authorize_url),
	)


@auth_router.get("/callback", response_model=AuthCallbackResponse)
def oauth_callback(code: str = Query(...)):
	try:
		return AuthService.handle_callback(code)
	except RuntimeError as exc:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(exc),
		)


@auth_router.get("/me", response_model=MeResponse)
def get_me(user=Depends(get_current_user)):
	return MeResponse(
		message="User profile",
		data=MeData(
			id=user.id,
			email=user.email,
			name=user.name,
			portal_id=user.portal_id,
		),
	)


@auth_router.post("/logout", response_model=LogoutResponse)
def logout(user=Depends(get_current_user)):
	token = user_repository.get_token_by_user_id(user.id)
	if token and token.access_token:
		try:
			zoho_auth.revoke_token(token.access_token)
		except Exception:
			raise HTTPException(
				status_code=status.HTTP_502_BAD_GATEWAY,
				detail="Failed to revoke Zoho token",
			)

	user_repository.delete_token_by_user_id(user.id)
	return LogoutResponse(
		message="Logged out",
		data=LogoutData(revoked=True),
	)