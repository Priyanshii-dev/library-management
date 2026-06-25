
from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.auth.router import router
from app.models.user import User    
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth.logout import LogoutService
from app.utils.response import api_response


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await LogoutService(db).logout(current_user)
    return api_response(
        message="Logout successful.",
        status_code=status.HTTP_200_OK
    )