import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.book import Book, BookAvailability
from app.models.book_borrow import BookBorrow, BorrowStatus
from app.schemas.book import BookBorrowHistoryOut

logger = logging.getLogger(__name__)


class BorrowBookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def borrow_book(self, user_id: int, book_id: int) -> BookBorrowHistoryOut:
        stmt = select(Book).where(Book.id == book_id)
        result = await self.db.execute(stmt)
        book = result.scalar_one_or_none()

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )

        if book.available_quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is not available for borrowing",
            )

        borrow = BookBorrow(
            user_id=user_id,
            book_id=book_id,
            due_date=datetime.now(timezone.utc) + timedelta(days=14),
            status=BorrowStatus.BORROWED,
        )

        book.available_quantity -= 1
        book.availability = BookAvailability.YES if book.available_quantity > 0 else BookAvailability.NO

        self.db.add(borrow)
        await self.db.commit()
        await self.db.refresh(borrow)
        await self.db.refresh(book)

        logger.info(f"Book borrowed: book_id={book_id}, user_id={user_id}")
        return BookBorrowHistoryOut.model_validate(borrow)
