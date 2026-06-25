import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserRole, UserStatus
from app.schemas.auth import RegistrationRequest
from app.schemas.user import UserOut
from app.core.security import hash_password
from app.services.otp_service import OTPService
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class RegistrationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, data: RegistrationRequest) -> UserOut:
        """Register a new user with OTP verification."""
        stmt = select(User).where(User.email == data.email)
        existing_user = await self.db.execute(stmt)
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            password=hash_password(data.password),
            role=UserRole.USER,
            status=UserStatus.PENDING,
            is_email_verified=False,
        )

        self.db.add(user)
        await self.db.flush()

        otp_code = OTPService.generate_otp()
        user.otp_code = otp_code
        user.otp_created_at = datetime.now(timezone.utc)
        
        await self.db.commit()

        await EmailService.send_otp_email(
            email=user.email,
            otp_code=otp_code,
            username=f"{user.first_name} {user.last_name}",
        )

        return UserOut.model_validate(user)