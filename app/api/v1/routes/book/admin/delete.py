from fastapi import Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.services.books.delete_book import DeleteBookService
from app.utils.response import api_response


@router.delete("/book/delete/{book_id}")
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
