from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.services.admin.delete_user import DeleteUserService
from app.utils.response import api_response


@router.delete("/{user_id}")
async def admin_delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    await DeleteUserService(db).delete_user(user_id)
    return api_response(
        message="User account deleted successfully.",
        status_code=status.HTTP_200_OK
    )