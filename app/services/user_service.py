import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.models.user import User, UserStatus
from app.schemas.user import (
    UserOut,
    UserUpdate,
    UserListOut,
    UserDetailResponse,
)
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> UserDetailResponse:
        """Get user by ID (authenticated users can view their own profile)."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return UserDetailResponse.model_validate(user)

    async def update_user_profile(
        self, user_id: int, data: UserUpdate
    ) -> UserDetailResponse:
        """Update user profile."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Update email if provided (and it's different)
        if data.email and data.email != user.email:
            # Check if email is already taken
            stmt = select(User).where(User.email == data.email)
            result = await self.db.execute(stmt)
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use",
                )
            user.email = data.email

        # Update other fields
        if data.first_name:
            user.first_name = data.first_name
        if data.last_name:
            user.last_name = data.last_name
        if data.phone:
            user.phone = data.phone
        if data.user_logo is not None:
            if data.user_logo == "":
                user.user_logo = None
            else:
                import base64
                try:
                    logo_str = data.user_logo
                    if "," in logo_str:
                        logo_str = logo_str.split(",")[1]
                    user.user_logo = base64.b64decode(logo_str)
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid base64 string for user_logo: {str(e)}"
                    )

        await self.db.commit()
        await self.db.refresh(user)

        logger.info(f"User profile updated: {user.id}")
        return UserDetailResponse.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        """Delete user account (hard delete as per the schema)."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        await self.db.delete(user)
        await self.db.commit()

        logger.info(f"User account deleted: {user_id}")

    async def search_users(
        self, query: str, skip: int = 0, limit: int = 20
    ) -> list[UserListOut]:
        """Search users by email, first name, or last name (admin only)."""
        search_term = f"%{query.lower()}%"
        stmt = (
            select(User)
            .where(
                or_(
                    User.email.ilike(search_term),
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term),
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at.desc())
        )
        result = await self.db.execute(stmt)
        users = result.scalars().all()
        return [UserListOut.model_validate(user) for user in users]

    async def list_pending_approvals(
        self, skip: int = 0, limit: int = 20
    ) -> list[UserListOut]:
        """List users pending admin approval (status is Pending)."""
        stmt = (
            select(User)
            .where(User.status == UserStatus.PENDING)
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at)
        )
        result = await self.db.execute(stmt)
        users = result.scalars().all()
        return [UserListOut.model_validate(user) for user in users]

    async def approve_user(
        self, user_id: int, admin_id: int
    ) -> UserDetailResponse:
        """Approve user account (admin only)."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.status == UserStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already approved",
            )

        # Approve user
        user.status = UserStatus.APPROVED

        await self.db.commit()
        await self.db.refresh(user)

        # Send approval email
        await EmailService.send_approval_email(
            email=user.email,
            username=f"{user.first_name} {user.last_name}",
            is_approved=True,
        )

        logger.info(f"User approved: {user.id} by admin {admin_id}")
        return UserDetailResponse.model_validate(user)

    async def reject_user(
        self, user_id: int, rejection_reason: str
    ) -> UserDetailResponse:
        """Reject/deactivate user account (admin only)."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Reject user
        user.status = UserStatus.REJECTED

        await self.db.commit()
        await self.db.refresh(user)

        # Send rejection email
        await EmailService.send_approval_email(
            email=user.email,
            username=f"{user.first_name} {user.last_name}",
            is_approved=False,
            rejection_reason=rejection_reason,
        )

        logger.info(f"User rejected: {user.id}")
        return UserDetailResponse.model_validate(user)

    async def list_all_users(
        self, skip: int = 0, limit: int = 20
    ) -> list[UserListOut]:
        """List all users (admin only)."""
        stmt = (
            select(User)
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at.desc())
        )
        result = await self.db.execute(stmt)
        users = result.scalars().all()
        return [UserListOut.model_validate(user) for user in users]

    async def get_admin_dashboard_stats(self) -> dict:
        """Get admin user statistics for the dashboard."""
        stmt_total = select(func.count(User.id))
        total = await self.db.scalar(stmt_total) or 0
        
        stmt_approved = select(func.count(User.id)).where(User.status == UserStatus.APPROVED)
        approved = await self.db.scalar(stmt_approved) or 0
        
        stmt_rejected = select(func.count(User.id)).where(User.status == UserStatus.REJECTED)
        rejected = await self.db.scalar(stmt_rejected) or 0
        
        stmt_pending = select(func.count(User.id)).where(User.status == UserStatus.PENDING)
        pending = await self.db.scalar(stmt_pending) or 0
        
        return {
            "total_users": total,
            "approved_users": approved,
            "rejected_users": rejected,
            "pending_users": pending
        }
