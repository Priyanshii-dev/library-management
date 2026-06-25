import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User, UserStatus

logger = logging.getLogger(__name__)


class AdminDashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_admin_dashboard_stats(self) -> dict:
        stmt_total = select(func.count(User.id))
        total = await self.db.scalar(stmt_total) or 0

        stmt_approved = select(func.count(User.id)).where(User.status == UserStatus.APPROVED)
        approved = await self.db.scalar(stmt_approved) or 0

        stmt_rejected = select(func.count(User.id)).where(User.status == UserStatus.REJECTED)
        rejected = await self.db.scalar(stmt_rejected) or 0

        stmt_pending = select(func.count(User.id)).where(User.status == UserStatus.PENDING)
        pending = await self.db.scalar(stmt_pending) or 0

        return {
            "total_users": total,
            "approved_users": approved,
            "rejected_users": rejected,
            "pending_users": pending,
        }
