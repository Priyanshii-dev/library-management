from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.dependencies import get_current_user
from app.api.v1.routes.users.router import router
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserDetailResponse
from app.services.user.get_user import GetUserService
from app.services.user.update_profile import UpdateProfileService
from app.services.user.delete_user import DeleteUserService
from app.utils.response import api_response


@router.get("/me")
async def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    user_out = UserDetailResponse.model_validate(current_user)
    return api_response(
        data=jsonable_encoder(user_out),
        message="Profile details retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role.value != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot view other users' profiles",
        )
    user_out = await GetUserService(db).get_user_by_id(user_id)
    return api_response(
        data=jsonable_encoder(user_out),
        message="User retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.patch("/{user_id}")
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role.value != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other users' profiles",
        )
    user_out = await UpdateProfileService(db).update_user_profile(user_id, data)
    return api_response(
        data=jsonable_encoder(user_out),
        message="User updated successfully.",
        status_code=status.HTTP_200_OK
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role.value != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete other users' accounts",
        )
    await DeleteUserService(db).delete_user(user_id)
    return api_response(
        message="User deleted successfully.",
        status_code=status.HTTP_200_OK
    )