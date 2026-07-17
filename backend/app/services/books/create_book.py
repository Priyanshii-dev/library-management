import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.book import Book, BookAvailability
from app.models.category import Category
from app.schemas.book import BookCreate, BookOut

logger = logging.getLogger(__name__)


class CreateBookService:
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
