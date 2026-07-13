import enum
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Enum, Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
from pydantic import BaseModel, Field, field_validator, constr

class UserRole(str, enum.Enum):
    ADMIN = "Admin"
    USER = "User"


class UserStatus(str, enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Basic Info
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Security (hashed password stored in password column)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    from sqlalchemy import Text

    refresh_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    access_token:  Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # User Logo (stored in binary format)
    user_logo: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # OTP Verification
    otp_code: Mapped[str | None] = mapped_column(String(6), nullable=True)
    otp_created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Role and Status
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.PENDING, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role} status={self.status}>"
