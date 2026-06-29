from fastapi import Depends, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.users.router import router
from app.db.session import get_db
from app.schemas.book import BookBorrowRequest, BookActionRequest
from app.services.admin.book_service import AdminBookService
from app.utils.response import api_response


@router.get("/books")
async def list_available_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    books = await AdminBookService(db).list_available_books(skip=skip, limit=limit)
    return api_response(
        data=jsonable_encoder(books),
        message="Available books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.post("/books/borrow")
async def borrow_book(
    data: BookBorrowRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.services.user.borrow_book import BorrowBookService

    borrow = await BorrowBookService(db).borrow_book(current_user.id, data.book_id)
    return api_response(
        data=jsonable_encoder(borrow),
        message="Book borrowed successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.post("/books/return")
async def return_book(
    data: BookActionRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.services.user.return_book import ReturnBookService

    record = await ReturnBookService(db).return_book(current_user.id, data.borrow_id)
    return api_response(
        data=jsonable_encoder(record),
        message="Book returned successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.post("/books/renew")
async def renew_book(
    data: BookActionRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.services.user.renew_book import RenewBookService

    record = await RenewBookService(db).renew_book(current_user.id, data.borrow_id)
    return api_response(
        data=jsonable_encoder(record),
        message="Book renewed successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.get("/books/history")
async def borrowing_history(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.services.user.borrow_history import BorrowHistoryService

    history = await BorrowHistoryService(db).get_borrow_history(current_user.id)
    return api_response(
        data=jsonable_encoder(history),
        message="Borrowing history retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )
