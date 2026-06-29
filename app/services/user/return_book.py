import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.book import Book, BookAvailability
from app.models.book_borrow import BookBorrow, BorrowStatus
from app.schemas.book import BookBorrowHistoryOut

logger = logging.getLogger(__name__)


class ReturnBookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def return_book(self, user_id: int, borrow_id: int) -> BookBorrowHistoryOut:
        stmt = select(BookBorrow).where(BookBorrow.id == borrow_id, BookBorrow.user_id == user_id)
        result = await self.db.execute(stmt)
        borrow = result.scalar_one_or_none()

        if not borrow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Borrow record not found",
            )

        if borrow.status != BorrowStatus.BORROWED and borrow.status != BorrowStatus.OVERDUE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is not currently borrowed",
            )

        stmt = select(Book).where(Book.id == borrow.book_id)
        result = await self.db.execute(stmt)
        book = result.scalar_one_or_none()

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )

        borrow.status = BorrowStatus.RETURNED
        borrow.returned_at = datetime.now(timezone.utc)
        book.available_quantity += 1
        book.availability = BookAvailability.YES

        await self.db.commit()
        await self.db.refresh(borrow)
        await self.db.refresh(book)

        logger.info(f"Book returned: borrow_id={borrow_id}, user_id={user_id}")
        return BookBorrowHistoryOut.model_validate(borrow)
