import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User, UserStatus
from app.schemas.user import UserDetailResponse
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class ApproveUserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def approve_user(
        self, user_id: int, admin_id: int
    ) -> UserDetailResponse:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.status == UserStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already approved",
            )

        user.status = UserStatus.APPROVED

        await self.db.commit()
        await self.db.refresh(user)

        await EmailService.send_approval_email(
            email=user.email,
            username=f"{user.first_name} {user.last_name}",
            is_approved=True,
        )

        logger.info(f"User approved: {user.id} by admin {admin_id}")
        return UserDetailResponse.model_validate(user)
