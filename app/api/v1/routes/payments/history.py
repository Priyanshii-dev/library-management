from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.payments.router import router
from app.db.session import get_db
from app.models.membership import Payment
from app.schemas.membership import PaymentOut
from app.utils.response import api_response


@router.get("/history")
async def payment_history(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Payment).where(Payment.user_id == current_user.id).order_by(Payment.created_at.desc())
    result = await db.execute(stmt)
    payments = result.scalars().all()

    return api_response(
        data=[PaymentOut.model_validate(payment) for payment in payments],
        message="Payment history retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )
