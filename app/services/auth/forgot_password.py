from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.email_service import EmailService
from app.services.otp_service import OTPService


class ForgotPasswordService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def send_reset_link(self, email: str) -> dict:
        """Generate an OTP for password reset and email it when the account exists."""
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return {
                "message": "If the account exists, a password reset OTP has been sent"
            }

        if not user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Email must be verified before resetting the password",
                    "statusCode": 400,
                    "data": [],
                },
            )

        otp_code = OTPService.generate_otp()
        user.otp_code = otp_code
        user.otp_created_at = datetime.now(timezone.utc)

        await self.db.commit()

        await EmailService.send_password_reset_email(
            email=user.email,
            otp_code=otp_code,
            username=f"{user.first_name} {user.last_name}",
        )

        return {
            "message": "If the account exists, a password reset OTP has been sent"
        }
