from app.api.v1.routes.auth.router import router
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import OTPVerifyRequest
from app.services.auth.verify_otp import VerifyOTPService
from app.utils.response import api_response
from fastapi import  Depends, status

@router.post("/verify-email")
async def verify_email(
    data: OTPVerifyRequest,
    db: AsyncSession = Depends(get_db),
):
    res = await VerifyOTPService(db).verify_email_otp(data)
    return api_response(
        data=res,
        message="Email verified successfully. Your account is now pending admin approval.",
        status_code=status.HTTP_200_OK
    )