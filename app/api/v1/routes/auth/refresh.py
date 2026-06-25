from fastapi import  Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.routes.auth.router import router
from app.db.session import get_db
from app.schemas.auth import RefreshRequest
from app.services.auth.refresh import RefreshService
from app.utils.response import api_response


@router.post("/refresh")
async def refresh_token(
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    token_response = await RefreshService(db).refresh(body.refresh_token)
    return api_response(
        data=jsonable_encoder(token_response),
        message="Tokens refreshed successfully.",
        status_code=status.HTTP_200_OK
    )