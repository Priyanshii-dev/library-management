from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.membership.router import router
from app.db.session import get_db
from app.models.membership import Membership
from app.schemas.membership import MembershipOut
from app.utils.response import api_response


@router.get("/history")
async def membership_history(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Membership).where(Membership.user_id == current_user.id).order_by(Membership.created_at.desc())
    result = await db.execute(stmt)
    memberships = result.scalars().all()

    return api_response(
        data=[MembershipOut.model_validate(membership) for membership in memberships],
        message="Membership history retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )
