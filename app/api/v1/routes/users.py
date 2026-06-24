from fastapi import APIRouter, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user, get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    UserUpdate,
    UserDetailResponse,
)
from app.services.user_service import UserService
from app.utils.response import api_response

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile/me")
async def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Get current user's profile details.
    """
    user_out = UserDetailResponse.model_validate(current_user)
    return api_response(
        data=jsonable_encoder(user_out),
        message="Profile details retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.patch("/profile/me")
async def update_my_profile(
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update current user's profile.
    Can update: first_name, last_name, phone, email.
    """
    user_out = await UserService(db).update_user_profile(current_user.id, data)
    return api_response(
        data=jsonable_encoder(user_out),
        message="Profile updated successfully.",
        status_code=status.HTTP_200_OK
    )


@router.delete("/profile/me")
async def delete_my_account(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete own account.
    """
    await UserService(db).delete_user(current_user.id)
    return api_response(
        message="Account deleted successfully.",
        status_code=status.HTTP_200_OK
    )


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get user profile by ID.
    Users can only view their own profile, admins can view any user.
    """
    if current_user.id != user_id and current_user.role.value != "Admin":
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot view other users' profiles",
        )
    
    user_out = await UserService(db).get_user_by_id(user_id)
    return api_response(
        data=jsonable_encoder(user_out),
        message="User profile retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


# ──────────────────────────────────────────────────────────────────
# ADMIN ONLY ENDPOINTS
# ──────────────────────────────────────────────────────────────────


@router.get("/")
async def list_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    """
    List all users in the system.
    Admin only.
    """
    users = await UserService(db).list_all_users(skip=skip, limit=limit)
    return api_response(
        data=jsonable_encoder(users),
        message="All users retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.get("/admin/dashboard/stats")
async def get_admin_dashboard(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    """
    Get admin dashboard stats for users.
    Admin only.
    """
    stats = await UserService(db).get_admin_dashboard_stats()
    return api_response(
        data=stats,
        message="Admin dashboard stats retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.get("/admin/search")
async def search_users(
    q: str = Query(..., min_length=1, description="Search by email, first name, or last name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    """
    Search users by email, first name, or last name.
    Admin only.
    """
    users = await UserService(db).search_users(query=q, skip=skip, limit=limit)
    return api_response(
        data=jsonable_encoder(users),
        message=f"Search completed for query: {q}",
        status_code=status.HTTP_200_OK
    )


@router.get("/admin/pending-approvals")
async def list_pending_approvals(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    """
    List users pending admin approval.
    Admin only.
    """
    users = await UserService(db).list_pending_approvals(skip=skip, limit=limit)
    return api_response(
        data=jsonable_encoder(users),
        message="Pending approval list retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.post("/admin/approve/{user_id}")
async def approve_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Approve a user account for login.
    Admin only.
    """
    user_out = await UserService(db).approve_user(user_id, current_admin.id)
    return api_response(
        data=jsonable_encoder(user_out),
        message="User account approved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.post("/admin/reject/{user_id}")
async def reject_user(
    user_id: int,
    rejection_reason: str = Query(..., min_length=5, description="Reason for rejection"),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    """
    Reject a user account.
    Admin only.
    """
    user_out = await UserService(db).reject_user(user_id, rejection_reason)
    return api_response(
        data=jsonable_encoder(user_out),
        message="User account registration rejected.",
        status_code=status.HTTP_200_OK
    )


@router.delete("/admin/{user_id}")
async def admin_delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    """
    Admin can delete any user account.
    Admin only.
    """
    await UserService(db).delete_user(user_id)
    return api_response(
        message="User account deleted successfully.",
        status_code=status.HTTP_200_OK
    )
