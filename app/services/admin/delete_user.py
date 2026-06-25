import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User

logger = logging.getLogger(__name__)


class DeleteUserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def delete_user(self, user_id: int) -> None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        await self.db.delete(user)
        await self.db.commit()

        logger.info(f"User account deleted by admin: {user_id}")
