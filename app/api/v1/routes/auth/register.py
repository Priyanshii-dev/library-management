from app.api.v1.routes.auth.router import router
from app.db.session import get_db
from fastapi import  Depends, status
from app.schemas.auth import RegistrationRequest
from app.utils.response import api_response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.services.auth.registration import RegistrationService

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegistrationRequest,
    db: AsyncSession = Depends(get_db),
):
    user_out = await RegistrationService(db).register(data)
    return api_response(
        data=jsonable_encoder(user_out),
        message="Registration successful. Verification OTP sent to email.",
        status_code=status.HTTP_201_CREATED
    )
