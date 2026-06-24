import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserRole, UserStatus
from app.schemas.auth import (
    RegistrationRequest,
    TokenResponse,
    OTPVerifyRequest,
)
from app.schemas.user import UserOut
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.services.otp_service import OTPService
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, data: RegistrationRequest) -> UserOut:
        """
        Register a new user with OTP verification.
        User will be created but not approved until email verified and admin approves.
        """
        # Check if email already exists
        stmt = select(User).where(User.email == data.email)
        existing_user = await self.db.execute(stmt)
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create new user
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            password=hash_password(data.password),
            role=UserRole.USER,
            status=UserStatus.PENDING,
            is_email_verified=False,
        )

        self.db.add(user)
        await self.db.flush()

        # Generate and send OTP
        otp_code = OTPService.generate_otp()
        user.otp_code = otp_code
        user.otp_created_at = datetime.now(timezone.utc)
        
        await self.db.commit()

        # Send OTP email
        await EmailService.send_otp_email(
            email=user.email,
            otp_code=otp_code,
            username=f"{user.first_name} {user.last_name}",
        )

        return UserOut.model_validate(user)

    async def verify_email_otp(self, data: OTPVerifyRequest) -> dict:
        """Verify email OTP and mark email as verified."""
        stmt = select(User).where(User.email == data.email)
        user = await self.db.execute(stmt)
        user = user.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Verify OTP
        if not OTPService.verify_otp(user.otp_code, data.otp_code, user.otp_created_at):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP",
            )

        # Mark email as verified
        user.is_email_verified = True
        user.otp_code = None
        user.otp_created_at = None

        await self.db.commit()

        return {
            "message": "Email verified successfully. Your account is now pending admin approval.",
            "email_verified": True,
            "user_id": user.id,
        }

    async def login(self, email: str, password: str) -> TokenResponse:
        """
        Login user and return tokens.
        User must be approved and email verified to login.
        """
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Check if email is verified
        if not user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified. Please verify your email first.",
            )

        # Check login conditions based on status
        if user.status != UserStatus.APPROVED:
            if user.status == UserStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Your account status is Pending. You must wait for admin approval.",
                )
            elif user.status == UserStatus.REJECTED:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Your account registration request has been Rejected.",
                )

        # Create tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        # Store refresh token
        user.refresh_token = refresh_token
        await self.db.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_role=user.role.value,
            user_id=user.id,
            email=user.email,
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token."""
        try:
            payload = decode_token(refresh_token)
            user_id = int(payload.get("sub"))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or user.refresh_token != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        # Check status before refreshing
        if user.status != UserStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account is not approved.",
            )

        # Create new tokens
        access_token = create_access_token({"sub": str(user.id)})
        new_refresh_token = create_refresh_token({"sub": str(user.id)})

        # Update refresh token
        user.refresh_token = new_refresh_token
        await self.db.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            user_role=user.role.value,
            user_id=user.id,
            email=user.email,
        )

    async def logout(self, user: User) -> None:
        """Logout user by clearing refresh token."""
        user.refresh_token = None
        await self.db.commit()

    async def request_otp_resend(self, email: str) -> dict:
        """Resend OTP to user email."""
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="If email exists, OTP will be sent shortly",
            )

        if user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified",
            )

        # Generate new OTP
        otp_code = OTPService.generate_otp()
        user.otp_code = otp_code
        user.otp_created_at = datetime.now(timezone.utc)

        await self.db.commit()

        # Send OTP email
        await EmailService.send_otp_email(
            email=user.email,
            otp_code=otp_code,
            username=f"{user.first_name} {user.last_name}",
        )

        return {
            "message": "OTP sent to email",
            "email": email,
        }

    async def check_approval_status(self, user_id: int) -> dict:
        """Check user status."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return {
            "user_id": user.id,
            "status": user.status.value,
            "email_verified": user.is_email_verified,
            "can_login": user.status == UserStatus.APPROVED and user.is_email_verified,
        }
