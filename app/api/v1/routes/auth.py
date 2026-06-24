from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    TokenResponse,
    RefreshRequest,
    RegistrationRequest,
    OTPVerifyRequest,
    LoginRequest,
)
from app.schemas.user import UserOut
from app.services.auth_service import AuthService
from app.utils.response import api_response

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegistrationRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user account.
    User will receive an OTP via email for verification.
    """
    user_out = await AuthService(db).register(data)
    return api_response(
        data=jsonable_encoder(user_out),
        message="Registration successful. Verification OTP sent to email.",
        status_code=status.HTTP_201_CREATED
    )


@router.post("/verify-email")
async def verify_email(
    data: OTPVerifyRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Verify user email using OTP code.
    """
    res = await AuthService(db).verify_email_otp(data)
    return api_response(
        data=res,
        message="Email verified successfully. Your account is now pending admin approval.",
        status_code=status.HTTP_200_OK
    )


@router.post("/resend-otp")
async def resend_otp(
    email: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Resend OTP to user email if they haven't verified yet.
    """
    res = await AuthService(db).request_otp_resend(email)
    return api_response(
        data=res,
        message="OTP code sent to email successfully.",
        status_code=status.HTTP_200_OK
    )


@router.post("/login")
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Login with email and password.
    """
    token_response = await AuthService(db).login(data.email, data.password)
    return api_response(
        data=jsonable_encoder(token_response),
        message="Login successful.",
        status_code=status.HTTP_200_OK
    )


@router.post("/refresh")
async def refresh_token(
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Exchange refresh token for new token pair.
    """
    token_response = await AuthService(db).refresh(body.refresh_token)
    return api_response(
        data=jsonable_encoder(token_response),
        message="Tokens refreshed successfully.",
        status_code=status.HTTP_200_OK
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Logout and invalidate refresh token.
    """
    await AuthService(db).logout(current_user)
    return api_response(
        message="Logout successful.",
        status_code=status.HTTP_200_OK
    )


@router.get("/me")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Get current authenticated user's profile.
    """
    user_out = UserOut.model_validate(current_user)
    return api_response(
        data=jsonable_encoder(user_out),
        message="Current user profile retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.get("/approval-status/{user_id}")
async def check_approval_status(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Check if user is approved and can login.
    """
    res = await AuthService(db).check_approval_status(user_id)
    return api_response(
        data=res,
        message="User status details retrieved successfully.",
        status_code=status.HTTP_200_OK
    )
