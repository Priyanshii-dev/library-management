from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.users.router import router
from app.db.session import get_db
from app.schemas.book import BookBorrowRequest
from app.utils.response import api_response


@router.post("/book/borrow")
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
