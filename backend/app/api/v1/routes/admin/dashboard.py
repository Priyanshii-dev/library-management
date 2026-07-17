from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.services.admin.admin_dashboard import AdminDashboardService
from app.utils.response import api_response


@router.get("/dashboard/stats")
async def get_admin_dashboard(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    stats = await AdminDashboardService(db).get_admin_dashboard_stats()
    return api_response(
        data=stats,
        message="Admin dashboard stats retrieved successfully.",
        status_code=status.HTTP_200_OK
    )