import enum
from datetime import datetime, timezone
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class BookAvailability(str, enum.Enum):
    YES = "Yes"
    NO = "No"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=True)
    total_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    available_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    availability: Mapped[BookAvailability] = mapped_column(
        Enum(BookAvailability), default=BookAvailability.YES, nullable=False
    )
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title} available={self.available_quantity}>"
