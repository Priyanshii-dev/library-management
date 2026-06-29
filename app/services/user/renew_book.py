import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.book_borrow import BookBorrow, BorrowStatus
from app.schemas.book import BookBorrowHistoryOut

logger = logging.getLogger(__name__)


class RenewBookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def renew_book(self, user_id: int, borrow_id: int) -> BookBorrowHistoryOut:
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
                detail="Only borrowed or overdue books can be renewed",
            )

        borrow.renewed_at = datetime.now(timezone.utc)
        borrow.due_date = datetime.now(timezone.utc) + timedelta(days=14)
        if borrow.status == BorrowStatus.OVERDUE:
            borrow.status = BorrowStatus.BORROWED

        await self.db.commit()
        await self.db.refresh(borrow)

        logger.info(f"Book renewed: borrow_id={borrow_id}, user_id={user_id}")
        return BookBorrowHistoryOut.model_validate(borrow)
