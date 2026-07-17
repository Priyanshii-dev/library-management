from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserStatus
from app.schemas.auth import TokenResponse
from app.core.security import create_access_token, create_refresh_token, decode_token


class RefreshService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token."""
        try:
            payload = decode_token(refresh_token)
            user_id = int(payload.get("sub"))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or user.refresh_token != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        if user.status != UserStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account is not approved.",
            )

        access_token = create_access_token({"sub": str(user.id)})
        new_refresh_token = create_refresh_token({"sub": str(user.id)})

        user.refresh_token = new_refresh_token
        user.access_token = access_token
        await self.db.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            user_role=user.role.value,
            user_id=user.id,
            id=user.id,
            email=user.email,
        )