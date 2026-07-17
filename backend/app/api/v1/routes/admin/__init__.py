from app.api.v1.routes.admin.router import router as admin_router
from app.api.v1.routes.book import admin as book_admin

from app.api.v1.routes.admin import (
    users,
    dashboard,
    search,
    pending_approvals,
    approve,
    reject,
    delete,
    category,
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
    "category",
    "book_admin",
]