from app.api.v1.routes.auth.router import router as auth_router
from app.api.v1.routes.users.router import router as users_router

__all__ = ["auth_router", "users_router"]
