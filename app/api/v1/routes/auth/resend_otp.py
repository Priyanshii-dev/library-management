from app.api.v1.routes.auth.router import router
from fastapi import  Depends, status
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth.resend_otp import ResendOTPService
from app.utils.response import api_response


@router.post("/resend-otp")
async def resend_otp(
    email: str,
    db: AsyncSession = Depends(get_db),
):
    res = await ResendOTPService(db).resend_otp(email)
    return api_response(
        data=res,
        message="OTP code sent to email successfully.",
        status_code=status.HTTP_200_OK
    )