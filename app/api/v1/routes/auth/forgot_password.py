from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routes.auth.router import router
from app.db.session import get_db
from app.schemas.auth import ForgotPasswordRequest
from app.services.auth.forgot_password import ForgotPasswordService
from app.utils.response import api_response


@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    await ForgotPasswordService(db).send_reset_link(data.email)
    return api_response(
        data={},
        message="If the account exists, a password reset OTP has been sent",
        status_code=status.HTTP_200_OK,
    )
