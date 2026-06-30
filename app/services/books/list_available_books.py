import logging
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book
from app.schemas.book import BookOut

logger = logging.getLogger(__name__)


class ListAvailableBooksService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_available_books(
        self,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
    ) -> list[BookOut]:
        offset = (page - 1) * limit
        stmt = select(Book).where(Book.available_quantity > 0)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(or_(Book.title.ilike(like), Book.author.ilike(like)))
        stmt = stmt.offset(offset).limit(limit).order_by(Book.added_at.desc())
        result = await self.db.execute(stmt)
        books = result.scalars().all()
        return [BookOut.model_validate(book) for book in books]
