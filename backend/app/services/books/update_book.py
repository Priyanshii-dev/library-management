import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.book import Book, BookAvailability
from app.models.category import Category
from app.schemas.book import BookUpdate, BookOut

logger = logging.getLogger(__name__)


class UpdateBookService:
    def __init__(self, db: AsyncSession):
        self.db = db

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
