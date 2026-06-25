from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.users.router import router
from app.db.session import get_db
from app.models.user import User
from app.services.user.get_user import GetUserService
from app.utils.response import api_response


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role.value != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot view other users' profiles",
        )
    user_out = await GetUserService(db).get_user_by_id(user_id)
    return api_response(
        data=jsonable_encoder(user_out),
        message="User profile retrieved successfully.",
        status_code=status.HTTP_200_OK
    )