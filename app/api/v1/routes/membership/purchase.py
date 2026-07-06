from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.membership.router import router
from app.db.session import get_db
from app.models.membership import Membership, MembershipPlan, MembershipStatus
from app.schemas.membership import MembershipPurchaseRequest, MembershipOut
from app.utils.response import api_response


@router.post("/purchase")
async def purchase_membership(
    payload: MembershipPurchaseRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select

    stmt = select(MembershipPlan).where(MembershipPlan.id == payload.plan_id)
    result = await db.execute(stmt)
    plan = result.scalar_one_or_none()
    if not plan:
        return api_response(data={}, message="Membership plan not found.", status_code=status.HTTP_404_NOT_FOUND)

    membership = Membership(
        user_id=current_user.id,
        plan_id=plan.id,
        start_date=date.today(),
        expiry_date=date.today() + timedelta(days=plan.validity_days),
        status=MembershipStatus.ACTIVE,
    )
    db.add(membership)
    await db.commit()
    await db.refresh(membership)

    return api_response(
        data=MembershipOut.model_validate(membership),
        message="Membership purchased successfully.",
        status_code=status.HTTP_201_CREATED,
    )
