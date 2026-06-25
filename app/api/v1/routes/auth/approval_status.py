from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.routes.auth.router import router
from app.db.session import get_db
from app.services.auth.approval_status import ApprovalStatusService
from app.utils.response import api_response

@router.get("/approval-status/{user_id}")
async def check_approval_status(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    res = await ApprovalStatusService(db).check_approval_status(user_id)
    return api_response(
        data=res,
        message="User status details retrieved successfully.",
        status_code=status.HTTP_200_OK
    )