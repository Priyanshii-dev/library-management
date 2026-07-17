import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models.book_borrow import BookBorrow
from app.schemas.book import BookBorrowHistoryOut

logger = logging.getLogger(__name__)


class BorrowHistoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_borrow_history(self, user_id: int) -> list[BookBorrowHistoryOut]:
        stmt = select(BookBorrow).where(BookBorrow.user_id == user_id).order_by(BookBorrow.borrowed_at.desc())
        result = await self.db.execute(stmt)
        records = result.scalars().all()

        return [BookBorrowHistoryOut.model_validate(record) for record in records]
