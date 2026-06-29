import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException, status

from app.models.book import Book, BookAvailability
from app.models.category import Category
from app.models.book_borrow import BookBorrow, BorrowStatus
from app.schemas.book import BookCreate, BookUpdate, BookOut

logger = logging.getLogger(__name__)


class AdminBookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_book(self, data: BookCreate) -> BookOut:
        stmt = select(Category).where(Category.id == data.category_id)
        result = await self.db.execute(stmt)
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        available_quantity = data.available_quantity if data.available_quantity is not None else data.total_quantity
        availability = BookAvailability.YES if available_quantity > 0 else BookAvailability.NO

        book = Book(
            title=data.title,
            author=data.author,
            price=data.price,
            category_id=data.category_id,
            publication_year=data.publication_year,
            total_quantity=data.total_quantity,
            available_quantity=available_quantity,
            availability=availability,
        )

        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return BookOut.model_validate(book)

    async def update_book(self, book_id: int, data: BookUpdate) -> BookOut:
        stmt = select(Book).where(Book.id == book_id)
        result = await self.db.execute(stmt)
        book = result.scalar_one_or_none()

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )

        if data.category_id:
            stmt = select(Category).where(Category.id == data.category_id)
            result = await self.db.execute(stmt)
            if not result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found",
                )
            book.category_id = data.category_id

        if data.title:
            book.title = data.title
        if data.author:
            book.author = data.author
        if data.price is not None:
            book.price = data.price
        if data.publication_year is not None:
            book.publication_year = data.publication_year
        if data.total_quantity is not None:
            borrowed_count = book.total_quantity - book.available_quantity
            if data.total_quantity < borrowed_count:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Total quantity cannot be less than books already borrowed",
                )
            book.total_quantity = data.total_quantity
            book.available_quantity = data.total_quantity - borrowed_count
        if data.available_quantity is not None:
            book.available_quantity = data.available_quantity

        book.availability = BookAvailability.YES if book.available_quantity > 0 else BookAvailability.NO
        if data.availability:
            try:
                book.availability = BookAvailability(data.availability)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid availability value",
                )

        await self.db.commit()
        await self.db.refresh(book)
        return BookOut.model_validate(book)

    async def delete_book(self, book_id: int) -> None:
        stmt = select(Book).where(Book.id == book_id)
        result = await self.db.execute(stmt)
        book = result.scalar_one_or_none()

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )

        await self.db.delete(book)
        await self.db.commit()

    async def list_books(self, skip: int = 0, limit: int = 20, search: str | None = None) -> list[BookOut]:
        stmt = select(Book)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(or_(Book.title.ilike(like), Book.author.ilike(like)))
        stmt = stmt.offset(skip).limit(limit).order_by(Book.added_at.desc())
        result = await self.db.execute(stmt)
        books = result.scalars().all()
        return [BookOut.model_validate(book) for book in books]

    async def list_available_books(self, skip: int = 0, limit: int = 20, search: str | None = None) -> list[BookOut]:
        stmt = select(Book).where(Book.available_quantity > 0)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(or_(Book.title.ilike(like), Book.author.ilike(like)))
        stmt = stmt.offset(skip).limit(limit).order_by(Book.added_at.desc())
        result = await self.db.execute(stmt)
        books = result.scalars().all()
        return [BookOut.model_validate(book) for book in books]

    async def list_borrowed_books(self, skip: int = 0, limit: int = 20) -> list[dict]:
        stmt = select(BookBorrow).where(BookBorrow.status == BorrowStatus.BORROWED).offset(skip).limit(limit).order_by(BookBorrow.borrowed_at.desc())
        result = await self.db.execute(stmt)
        borrows = result.scalars().all()
        return [self._format_borrow_record(record) for record in borrows]

    async def list_overdue_books(self, skip: int = 0, limit: int = 20) -> list[dict]:
        now = datetime.now(timezone.utc)
        stmt = select(BookBorrow).where(
            BookBorrow.status == BorrowStatus.OVERDUE
        ).offset(skip).limit(limit).order_by(BookBorrow.due_date.asc())
        result = await self.db.execute(stmt)
        borrows = result.scalars().all()
        return [self._format_borrow_record(record) for record in borrows]

    async def list_returned_books(self, skip: int = 0, limit: int = 20) -> list[dict]:
        stmt = select(BookBorrow).where(BookBorrow.status == BorrowStatus.RETURNED).offset(skip).limit(limit).order_by(BookBorrow.returned_at.desc())
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
