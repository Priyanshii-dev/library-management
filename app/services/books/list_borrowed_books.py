import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book_borrow import BookBorrow, BorrowStatus
from app.schemas.book import BookBorrowRecordResponse

logger = logging.getLogger(__name__)


class ListBorrowedBooksService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_borrowed_books(self, page: int = 1, limit: int = 20) -> list[dict]:
        offset = (page - 1) * limit
        stmt = select(BookBorrow).where(BookBorrow.status == BorrowStatus.BORROWED)
        stmt = stmt.offset(offset).limit(limit).order_by(BookBorrow.borrowed_at.desc())
        result = await self.db.execute(stmt)
        borrows = result.scalars().all()
        return [self._format_borrow_record(record) for record in borrows]

    def _format_borrow_record(self, record: BookBorrow) -> dict:
        return {
            "borrow_id": record.id,
            "user_id": record.user_id,
            "book_id": record.book_id,
            "status": record.status.value,
            "borrowed_at": record.borrowed_at,
            "due_date": record.due_date,
            "renewed_at": record.renewed_at,
            "returned_at": record.returned_at,
        }
