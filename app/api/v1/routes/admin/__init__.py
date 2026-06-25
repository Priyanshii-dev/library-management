from app.api.v1.routes.admin.router import router as admin_router

from app.api.v1.routes.admin import (
    users,
    dashboard,
    search,
    pending_approvals,
    approve,
    reject,
    delete,
)

__all__ = [
    "admin_router",
    "users",
    "dashboard",
    "search",
    "pending_approvals",
    "approve",
    "reject",
    "delete",
]