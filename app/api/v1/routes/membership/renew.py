from datetime import date, timedelta
from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.membership.router import router
from app.db.session import get_db
from app.models.membership import Membership, MembershipPlan, MembershipStatus
from app.schemas.membership import MembershipOut
from app.utils.response import api_response


@router.post("/renew")
async def renew_membership(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Membership).where(Membership.user_id == current_user.id).order_by(Membership.created_at.desc())
    result = await db.execute(stmt)
    membership = result.scalar_one_or_none()

    if not membership:
        return api_response(data={}, message="No membership found.", status_code=status.HTTP_404_NOT_FOUND)

    plan_stmt = select(MembershipPlan).where(MembershipPlan.id == membership.plan_id)
    plan_result = await db.execute(plan_stmt)
    plan = plan_result.scalar_one_or_none()
    if not plan:
        return api_response(data={}, message="Membership plan not found.", status_code=status.HTTP_404_NOT_FOUND)

    membership.start_date = date.today()
    membership.expiry_date = date.today() + timedelta(days=plan.validity_days)
    membership.status = MembershipStatus.ACTIVE

    await db.commit()
    await db.refresh(membership)

    return api_response(
        data=MembershipOut.model_validate(membership),
        message="Membership renewed successfully.",
        status_code=status.HTTP_200_OK,
    )
