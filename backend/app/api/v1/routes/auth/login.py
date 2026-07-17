from fastapi import  Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.routes.auth.router import router
from app.db.session import get_db
from app.schemas.auth import LoginRequest
from app.services.auth.login import LoginService
from app.utils.response import api_response


@router.post("/login")
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    token_response = await LoginService(db).login(data.email, data.password)
    return api_response(
        data=jsonable_encoder(token_response),
        message="Login successful.",
        status_code=status.HTTP_200_OK
    )