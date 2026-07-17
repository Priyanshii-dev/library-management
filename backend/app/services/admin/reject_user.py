import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User, UserStatus
from app.schemas.user import UserDetailResponse
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class RejectUserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def reject_user(
        self, user_id: int, rejection_reason: str
    ) -> UserDetailResponse:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user.status = UserStatus.REJECTED

        await self.db.commit()
        await self.db.refresh(user)

        await EmailService.send_approval_email(
            email=user.email,
            username=f"{user.first_name} {user.last_name}",
            is_approved=False,
            rejection_reason=rejection_reason,
        )

        logger.info(f"User rejected: {user.id}")
        return UserDetailResponse.model_validate(user)
