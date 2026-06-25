from fastapi import Depends, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.services.admin.reject_user import RejectUserService
from app.utils.response import api_response


@router.post("/reject/{user_id}")
async def reject_user(
    user_id: int,
    rejection_reason: str = Query(..., min_length=5, description="Reason for rejection"),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    user_out = await RejectUserService(db).reject_user(user_id, rejection_reason)
    return api_response(
        data=jsonable_encoder(user_out),
        message="User account registration rejected.",
        status_code=status.HTTP_200_OK
    )