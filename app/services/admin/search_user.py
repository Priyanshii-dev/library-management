import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.user import User
from app.schemas.user import UserListOut

logger = logging.getLogger(__name__)


class SearchUserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_users(
        self, query: str, skip: int = 0, limit: int = 20
    ) -> list[UserListOut]:
        search_term = f"%{query.lower()}%"
        stmt = (
            select(User)
            .where(
                or_(
                    User.email.ilike(search_term),
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term),
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at.desc())
        )
        result = await self.db.execute(stmt)
        users = result.scalars().all()
        return [UserListOut.model_validate(user) for user in users]
