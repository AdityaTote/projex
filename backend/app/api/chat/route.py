from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth.deps import get_current_user

from .schema import ChatRequest, ChatResponse
from .service import ChatService

chat_router = APIRouter()


@chat_router.post("/", response_model=ChatResponse)
async def chat(payload: ChatRequest, user=Depends(get_current_user)):
  if not user.access_token:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="User is missing Zoho access token",
    )

  try:
    return await ChatService.run_chat(
      user_id=user.id,
      portal_id=user.portal_id,
      access_token=user.access_token,
      payload=payload,
    )
  except RuntimeError as exc:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=str(exc),
    )
