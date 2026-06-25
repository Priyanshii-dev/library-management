import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserUpdate, UserDetailResponse

logger = logging.getLogger(__name__)


class UpdateProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_user_profile(
        self, user_id: int, data: UserUpdate
    ) -> UserDetailResponse:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if data.email and data.email != user.email:
            stmt = select(User).where(User.email == data.email)
            result = await self.db.execute(stmt)
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use",
                )
            user.email = data.email

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
