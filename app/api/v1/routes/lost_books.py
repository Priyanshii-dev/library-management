from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.users.router import router
from app.db.session import get_db
from app.models.book_borrow import BookBorrow, BorrowStatus
from app.schemas.book import BookBorrowHistoryOut
from app.utils.response import api_response


@router.get("/lost-books")
async def list_lost_books(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(BookBorrow).where(BookBorrow.user_id == current_user.id, BookBorrow.status == BorrowStatus.LOST)
    result = await db.execute(stmt)
    borrows = result.scalars().all()

    return api_response(
        data=[BookBorrowHistoryOut.model_validate(borrow) for borrow in borrows],
        message="Lost books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.post("/lost-books/mark")
async def mark_lost_books(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.services.user.mark_lost_books import MarkLostBooksService

    marked_count = await MarkLostBooksService(db).mark_lost_books()
    return api_response(
        data={"marked_count": marked_count},
        message="Lost books marked successfully.",
        status_code=status.HTTP_200_OK,
    )
