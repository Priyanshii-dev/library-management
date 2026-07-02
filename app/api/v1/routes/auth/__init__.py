from app.api.v1.routes.auth.router import router as auth_router

from app.api.v1.routes.auth import (
    login,
    register,
    logout,
    me,
    refresh,
    verify_email,
    resend_otp,
    approval_status,
    forgot_password,
    reset_password,
)

__all__ = [
    "auth_router",
    "login",
    "register",
    "logout",
    "me",
    "refresh",
    "verify_email",
    "resend_otp",
    "approval_status",
    "forgot_password",
    "reset_password",
]