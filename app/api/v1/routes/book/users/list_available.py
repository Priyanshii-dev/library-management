from fastapi import Depends, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routes.users.router import router
from app.db.session import get_db
from app.services.books.list_available_books import ListAvailableBooksService
from app.utils.response import api_response


@router.get("/book/list")
async def list_available_books(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = Query(None, min_length=1),
    db: AsyncSession = Depends(get_db),
):
    books = await ListAvailableBooksService(db).list_available_books(page=page, limit=limit, search=search)
    return api_response(
        data=jsonable_encoder(books),
        message="Available books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )
