from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.schemas.book import BookCreate
from app.services.books.create_book import CreateBookService
from app.utils.response import api_response


@router.post("/book/create")
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
