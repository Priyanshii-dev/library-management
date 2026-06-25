from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class LogoutService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def logout(self, user: User) -> dict:
        """Logout user by clearing tokens."""
        user.refresh_token = None
        user.access_token = None
        await self.db.commit()

        return {
            "message": "Logged out successfully",
            "user_id": user.id,
            "user_role": user.role.value,
            "email": user.email,
        }