import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserListOut

logger = logging.getLogger(__name__)


class ListUsersService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all_users(
        self, skip: int = 0, limit: int = 20
    ) -> list[UserListOut]:
        stmt = (
            select(User)
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at.desc())
        )
        result = await self.db.execute(stmt)
        users = result.scalars().all()
        return [UserListOut.model_validate(user) for user in users]
