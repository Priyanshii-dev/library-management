from datetime import datetime, timezone
from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.payments.router import router
from app.db.session import get_db
from app.models.book import Book
from app.models.book_borrow import BookBorrow, BorrowStatus
from app.models.membership import Payment, PaymentStatus, PaymentType
from app.schemas.membership import PaymentOut
from app.utils.response import api_response


@router.post("/lost-books/{borrow_id}/pay")
async def pay_lost_book(
    borrow_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(BookBorrow).where(BookBorrow.id == borrow_id, BookBorrow.user_id == current_user.id)
    result = await db.execute(stmt)
    borrow = result.scalar_one_or_none()
    if not borrow:
        return api_response(data={}, message="Borrow record not found.", status_code=status.HTTP_404_NOT_FOUND)

    if borrow.status != BorrowStatus.LOST:
        return api_response(data={}, message="Borrow record is not marked as lost.", status_code=status.HTTP_400_BAD_REQUEST)

    stmt = select(Book).where(Book.id == borrow.book_id)
    result = await db.execute(stmt)
    book = result.scalar_one_or_none()

    amount = float(borrow.replacement_amount or 0) + float(borrow.fine_amount or 0)
    payment = Payment(
        user_id=current_user.id,
        borrow_id=borrow.id,
        amount=amount,
        payment_type=PaymentType.LOST_BOOK,
        payment_status=PaymentStatus.SUCCESS,
        paid_at=datetime.now(timezone.utc),
    )
    db.add(payment)

    borrow.status = BorrowStatus.RETURNED
    if book:
        book.total_quantity = max(0, book.total_quantity - 1)
        book.available_quantity = max(0, book.available_quantity)

    await db.commit()
    await db.refresh(payment)

    return api_response(
        data=PaymentOut.model_validate(payment),
        message="Lost book payment recorded successfully.",
        status_code=status.HTTP_200_OK,
    )
