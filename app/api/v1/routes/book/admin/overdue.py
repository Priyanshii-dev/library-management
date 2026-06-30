from fastapi import Depends, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.services.books.list_overdue_books import ListOverdueBooksService
from app.utils.response import api_response


@router.get("/book/overdue")
async def list_overdue_books(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    records = await ListOverdueBooksService(db).list_overdue_books(page=page, limit=limit)
    return api_response(
        data=jsonable_encoder(records),
        message="Overdue books retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )
