from fastapi import APIRouter
from app.api.v1.routes.auth.router import router as auth_router
from app.api.v1.routes.admin.router import router as admin_router
from app.api.v1.routes.users.router import router as users_router

api_router = APIRouter()

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(admin_router)
api_router.include_router(users_router)