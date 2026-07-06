from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.membership.router import router
from app.db.session import get_db
from app.models.membership import MembershipPlan
from app.schemas.membership import MembershipPlanCreate, MembershipPlanOut
from app.utils.response import api_response


@router.get("/plans")
async def list_membership_plans(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select

    result = await db.execute(select(MembershipPlan))
    plans = result.scalars().all()
    return api_response(
        data=[MembershipPlanOut.model_validate(plan) for plan in plans],
        message="Membership plans retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.post("/plans", status_code=status.HTTP_201_CREATED)
async def create_membership_plan(
    payload: MembershipPlanCreate,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    plan = MembershipPlan(**payload.model_dump())
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return api_response(
        data=MembershipPlanOut.model_validate(plan),
        message="Membership plan created successfully.",
        status_code=status.HTTP_201_CREATED,
    )
