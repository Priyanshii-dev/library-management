from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routes.auth.router import router
from app.db.session import get_db
from app.schemas.auth import PasswordResetRequest
from app.services.auth.reset_password import ResetPasswordService
from app.utils.response import api_response


@router.post("/reset-password")
async def reset_password(
    data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
):
    await ResetPasswordService(db).reset_password(
        email=data.email,
        otp_code=data.otp_code,
        new_password=data.new_password,
    )
    return api_response(
        data={},
        message="Password reset successfully",
        status_code=status.HTTP_200_OK,
    )
