from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.services.otp_service import OTPService
from app.services.email_service import EmailService


class ResendOTPService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def resend_otp(self, email: str) -> dict:
        """Resend OTP to user email."""
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="If email exists, OTP will be sent shortly",
            )

        if user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified",
            )

        # Clear any existing OTP before generating a new one
        user.otp_code = None
        user.otp_created_at = None

        otp_code = OTPService.generate_otp()
        user.otp_code = otp_code
        user.otp_created_at = datetime.now(timezone.utc)

        await self.db.commit()

        await EmailService.send_otp_email(
            email=user.email,
            otp_code=otp_code,
            username=f"{user.first_name} {user.last_name}",
        )

        return {
            "message": "OTP sent to email",
            "email": email,
        }