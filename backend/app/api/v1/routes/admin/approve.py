from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.models.user import User
from app.services.admin.approve_user import ApproveUserService
from app.utils.response import api_response


@router.post("/approve/{user_id}")
async def approve_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user_out = await ApproveUserService(db).approve_user(user_id, current_admin.id)
    return api_response(
        data=jsonable_encoder(user_out),
        message="User account approved successfully.",
        status_code=status.HTTP_200_OK
    )