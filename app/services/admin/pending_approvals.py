import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserStatus
from app.schemas.user import UserListOut

logger = logging.getLogger(__name__)


class PendingApprovalsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_pending_approvals(
        self, skip: int = 0, limit: int = 20
    ) -> list[UserListOut]:
        stmt = (
            select(User)
            .where(User.status == UserStatus.PENDING)
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at)
        )
        result = await self.db.execute(stmt)
        users = result.scalars().all()
        return [UserListOut.model_validate(user) for user in users]
