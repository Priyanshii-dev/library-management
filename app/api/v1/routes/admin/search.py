from fastapi import Depends, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.services.admin.search_user import SearchUserService
from app.utils.response import api_response


@router.get("/search")
async def search_users(
    q: str = Query(..., min_length=1, description="Search by email, first name, or last name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    users = await SearchUserService(db).search_users(query=q, skip=skip, limit=limit)
    return api_response(
        data=jsonable_encoder(users),
        message=f"Search completed for query: {q}",
        status_code=status.HTTP_200_OK
    )