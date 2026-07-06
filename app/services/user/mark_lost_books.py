from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book_borrow import BookBorrow, BorrowStatus


class MarkLostBooksService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def mark_lost_books(self, overdue_days: int = 30) -> int:
        now = datetime.now(timezone.utc)
        threshold = now - timedelta(days=overdue_days)

        stmt = select(BookBorrow).where(
            BookBorrow.status == BorrowStatus.OVERDUE,
            BookBorrow.due_date <= threshold,
        )
        result = await self.db.execute(stmt)
        borrows = result.scalars().all()

        for borrow in borrows:
            borrow.status = BorrowStatus.LOST
            borrow.lost_date = now
            borrow.replacement_amount = borrow.replacement_amount or 0

        if borrows:
            await self.db.commit()

        return len(borrows)
