import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.book import Book, BookAvailability
from app.models.book_borrow import BookBorrow, BorrowStatus
from app.models.membership import Membership, MembershipStatus
from app.models.user import User
from app.schemas.book import BookBorrowHistoryOut

logger = logging.getLogger(__name__)


class BorrowBookService:
    def __init__(self, db: AsyncSession | None):
        self.db = db

    def validate_borrow_request(self, user: User, book: Book, membership: Membership | None, active_borrows: list[BookBorrow], overdue_borrows: list[BookBorrow]) -> None:
        if not user.is_email_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email must be verified before borrowing books")

        if not membership or membership.status != MembershipStatus.ACTIVE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An active membership is required to borrow books")

        today = datetime.now(timezone.utc).date()
        if membership.expiry_date < today:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Membership has expired")

        if len(active_borrows) >= membership.plan.max_books:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Borrow limit reached for your membership plan")

        if book.available_quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is not available for borrowing")

        if overdue_borrows:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please clear overdue books before borrowing again")

    async def borrow_book(self, user_id: int, book_id: int) -> BookBorrowHistoryOut:
        stmt = select(Book).where(Book.id == book_id)
        result = await self.db.execute(stmt)
        book = result.scalar_one_or_none()

        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        stmt = select(Membership).where(Membership.user_id == user_id).order_by(Membership.created_at.desc())
        result = await self.db.execute(stmt)
        membership = result.scalar_one_or_none()

        stmt = select(BookBorrow).where(BookBorrow.user_id == user_id, BookBorrow.status == BorrowStatus.BORROWED)
        result = await self.db.execute(stmt)
        active_borrows = list(result.scalars().all())

        stmt = select(BookBorrow).where(BookBorrow.user_id == user_id, BookBorrow.status == BorrowStatus.OVERDUE)
        result = await self.db.execute(stmt)
        overdue_borrows = list(result.scalars().all())

        self.validate_borrow_request(user, book, membership, active_borrows, overdue_borrows)

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
