from fastapi import APIRouter
from app.api.v1.routes.auth import auth_router
from app.api.v1.routes.admin import admin_router
from app.api.v1.routes.users import users_router
from app.api.v1.routes.membership import membership_router
from app.api.v1.routes.payments import payments_router

api_router = APIRouter()

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(admin_router)
api_router.include_router(users_router)
api_router.include_router(membership_router)
api_router.include_router(payments_router)
