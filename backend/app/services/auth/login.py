from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserStatus
from app.schemas.auth import TokenResponse
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
)


class LoginService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def login(self, email: str, password: str) -> TokenResponse:
        """Login user and return tokens."""
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "Invalid email and password",
                    "statusCode": status.HTTP_401_UNAUTHORIZED,
                    "data": [],
                },
            )

        if not user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified. Please verify your email first.",
            )

        if user.status != UserStatus.APPROVED:
            if user.status == UserStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Your account status is Pending. You must wait for admin approval.",
                )
            elif user.status == UserStatus.REJECTED:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Your account registration request has been Rejected.",
                )

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        user.refresh_token = refresh_token
        user.access_token = access_token
        await self.db.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_role=user.role.value,
            user_id=user.id,
            email=user.email,
        )