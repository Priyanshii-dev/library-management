from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.schemas.auth import PasswordResetRequest
from app.services.otp_service import OTPService


class ResetPasswordService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def reset_password(self, email: str, otp_code: str, new_password: str) -> dict:
        """Verify OTP and update the user's password."""
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Email must be verified before resetting the password",
                    "statusCode": 400,
                    "data": [],
                },
            )

        if not OTPService.verify_otp(user.otp_code, otp_code, user.otp_created_at):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP",
            )

        user.password = hash_password(new_password)
        user.otp_code = None
        user.otp_created_at = None

        await self.db.commit()

        return {
            "message": "Password reset successfully"
        }
