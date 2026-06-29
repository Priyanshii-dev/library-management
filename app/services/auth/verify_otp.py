from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import OTPVerifyRequest
from app.services.otp_service import OTPService


class VerifyOTPService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def verify_email_otp(self, data: OTPVerifyRequest) -> dict:
        """Verify email OTP and mark email as verified."""
        stmt = select(User).where(User.email == data.email)
        user = await self.db.execute(stmt)
        user = user.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not OTPService.verify_otp(user.otp_code, data.otp_code, user.otp_created_at):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP",
            )

        user.is_email_verified = True
        user.otp_code = None
        user.otp_created_at = None

        await self.db.commit()

        return {
            "message": "Email verified successfully. Your account is now pending admin approval.",
            "email_verified": True,
            "user_id": user.id,
            "id": user.id,
        }