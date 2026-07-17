import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.book import Book

logger = logging.getLogger(__name__)


class DeleteBookService:
    def __init__(self, db: AsyncSession):
        self.db = db

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
