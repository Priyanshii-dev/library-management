from fastapi import Depends, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.services.admin.pending_approvals import PendingApprovalsService
from app.utils.response import api_response


@router.get("/pending-approvals")
async def list_pending_approvals(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    users = await PendingApprovalsService(db).list_pending_approvals(skip=skip, limit=limit)
    return api_response(
        data=jsonable_encoder(users),
        message="Pending approval list retrieved successfully.",
        status_code=status.HTTP_200_OK
    )