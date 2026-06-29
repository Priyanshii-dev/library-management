import enum
from datetime import datetime, timezone
from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class BorrowStatus(str, enum.Enum):
    BORROWED = "Borrowed"
    RETURNED = "Returned"
    OVERDUE = "Overdue"


class BookBorrow(Base):
    __tablename__ = "book_borrow"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    borrowed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    renewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[BorrowStatus] = mapped_column(
        Enum(BorrowStatus), default=BorrowStatus.BORROWED, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<BookBorrow id={self.id} user_id={self.user_id} book_id={self.book_id} status={self.status}>"
