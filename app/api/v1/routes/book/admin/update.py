from fastapi import Depends, Path, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.schemas.book import BookUpdate
from app.services.books.update_book import UpdateBookService
from app.utils.response import api_response


@router.patch("/book/update/{book_id}")
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
