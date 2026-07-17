from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.users.router import router
from app.db.session import get_db
from app.schemas.book import BookActionRequest
from app.utils.response import api_response


@router.post("/book/return")
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
