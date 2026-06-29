from fastapi import Depends, Path, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.schemas.book import BookCreate, BookUpdate
from app.services.admin.book_service import AdminBookService
from app.utils.response import api_response


@router.post("/books")
async def create_book(
    data: BookCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    book = await AdminBookService(db).create_book(data)
    return api_response(
        data=jsonable_encoder(book),
        message="Book created successfully.",
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/books")
async def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    books = await AdminBookService(db).list_books(skip=skip, limit=limit)
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
    book = await AdminBookService(db).update_book(book_id, data)
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
    await AdminBookService(db).delete_book(book_id)
    return api_response(
        message="Book deleted successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.get("/books/borrowed")
async def list_borrowed_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    records = await AdminBookService(db).list_borrowed_books(skip=skip, limit=limit)
    return api_response(
        data=jsonable_encoder(records),
        message="Borrowed books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.get("/books/overdue")
async def list_overdue_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    records = await AdminBookService(db).list_overdue_books(skip=skip, limit=limit)
    return api_response(
        data=jsonable_encoder(records),
        message="Overdue books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.get("/books/returned")
async def list_returned_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    records = await AdminBookService(db).list_returned_books(skip=skip, limit=limit)
    return api_response(
        data=jsonable_encoder(records),
        message="Returned books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )
