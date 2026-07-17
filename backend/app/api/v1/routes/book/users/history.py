from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.users.router import router
from app.db.session import get_db
from app.utils.response import api_response


@router.get("/book/history")
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
