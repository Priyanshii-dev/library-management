from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserStatus


class ApprovalStatusService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_approval_status(self, user_id: int) -> dict:
        """Check user approval status."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return {
            "user_id": user.id,
            "status": user.status.value,
            "email_verified": user.is_email_verified,
            "can_login": user.status == UserStatus.APPROVED and user.is_email_verified,
        }