import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.books.create_book import CreateBookService
from app.services.books.update_book import UpdateBookService
from app.services.books.delete_book import DeleteBookService
from app.services.books.list_books import ListBooksService
from app.services.books.list_borrowed_books import ListBorrowedBooksService
from app.services.books.list_overdue_books import ListOverdueBooksService
from app.services.books.list_returned_books import ListReturnedBooksService

logger = logging.getLogger(__name__)


class AdminBookService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.create_service = CreateBookService(db)
        self.update_service = UpdateBookService(db)
        self.delete_service = DeleteBookService(db)
        self.list_service = ListBooksService(db)
        self.borrowed_service = ListBorrowedBooksService(db)
        self.overdue_service = ListOverdueBooksService(db)
        self.returned_service = ListReturnedBooksService(db)

    async def create_book(self, data):
        return await self.create_service.create_book(data)

    async def update_book(self, book_id: int, data):
        return await self.update_service.update_book(book_id, data)

    async def delete_book(self, book_id: int) -> None:
        return await self.delete_service.delete_book(book_id)

    async def list_books(self, page: int = 1, limit: int = 20, search: str | None = None):
        return await self.list_service.list_books(page=page, limit=limit, search=search)

    async def list_borrowed_books(self, page: int = 1, limit: int = 20) -> list[dict]:
        return await self.borrowed_service.list_borrowed_books(page=page, limit=limit)

    async def list_overdue_books(self, page: int = 1, limit: int = 20) -> list[dict]:
        return await self.overdue_service.list_overdue_books(page=page, limit=limit)

    async def list_returned_books(self, page: int = 1, limit: int = 20) -> list[dict]:
        return await self.returned_service.list_returned_books(page=page, limit=limit)
