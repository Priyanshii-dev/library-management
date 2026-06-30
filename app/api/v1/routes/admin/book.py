from fastapi import Depends, Path, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.schemas.book import BookCreate, BookUpdate
from app.services.books.create_book import CreateBookService
from app.services.books.update_book import UpdateBookService
from app.services.books.delete_book import DeleteBookService
from app.services.books.list_books import ListBooksService
from app.services.books.list_borrowed_books import ListBorrowedBooksService
from app.services.books.list_overdue_books import ListOverdueBooksService
from app.services.books.list_returned_books import ListReturnedBooksService
from app.utils.response import api_response


@router.post("/books")
async def create_book(
    data: BookCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    book = await CreateBookService(db).create_book(data)
    return api_response(
        data=jsonable_encoder(book),
        message="Book created successfully.",
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/books")
async def list_books(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = Query(None, min_length=1),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    books = await ListBooksService(db).list_books(page=page, limit=limit, search=search)
    return api_response(
        data=jsonable_encoder(books),
        message="Books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.patch("/books/{book_id}")
async def update_book(
    data: BookUpdate,
    book_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    book = await UpdateBookService(db).update_book(book_id, data)
    return api_response(
        data=jsonable_encoder(book),
        message="Book updated successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.delete("/books/{book_id}")
async def delete_book(
    book_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    await DeleteBookService(db).delete_book(book_id)
    return api_response(
        message="Book deleted successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.get("/books/borrowed")
async def list_borrowed_books(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    records = await ListBorrowedBooksService(db).list_borrowed_books(page=page, limit=limit)
    return api_response(
        data=jsonable_encoder(records),
        message="Borrowed books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.get("/books/overdue")
async def list_overdue_books(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    records = await ListOverdueBooksService(db).list_overdue_books(page=page, limit=limit)
    return api_response(
        data=jsonable_encoder(records),
        message="Overdue books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.get("/books/returned")
async def list_returned_books(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    records = await ListReturnedBooksService(db).list_returned_books(page=page, limit=limit)
    return api_response(
        data=jsonable_encoder(records),
        message="Returned books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )
