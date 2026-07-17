import logging
from contextlib import asynccontextmanager
from sqlalchemy import select

from app.db.session import engine, async_session_maker
from app.core.security import hash_password, verify_password
from app.models.user import User, UserRole, UserStatus

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    logger.info("Database tables ready.")

    # Ensure default admin user exists with specified credentials
    admin_email = "admin@gmail.com"
    admin_password = "Admin@123"

    async with async_session_maker() as session:
        try:
            stmt = select(User).where(User.email == admin_email)
            result = await session.execute(stmt)
            admin = result.scalar_one_or_none()

            if not admin:
                admin = User(
                    first_name="Admin",
                    last_name="User",
                    email=admin_email,
                    password=hash_password(admin_password),
                    role=UserRole.ADMIN,
                    status=UserStatus.APPROVED,
                    is_email_verified=True,
                )
                session.add(admin)
                await session.commit()
                logger.info("Created default admin user: %s", admin_email)
            else:
                changed = False
                if admin.role != UserRole.ADMIN:
                    admin.role = UserRole.ADMIN
                    changed = True
                if admin.status != UserStatus.APPROVED:
                    admin.status = UserStatus.APPROVED
                    changed = True
                if not admin.is_email_verified:
                    admin.is_email_verified = True
                    changed = True
                if not verify_password(admin_password, admin.password):
                    admin.password = hash_password(admin_password)
                    changed = True
                if changed:
                    await session.commit()
                    logger.info("Updated admin user to match configured credentials: %s", admin_email)
        except Exception:
            logger.exception("Failed to ensure default admin user exists")

    yield
    await engine.dispose()
    logger.info("Database connections closed.")