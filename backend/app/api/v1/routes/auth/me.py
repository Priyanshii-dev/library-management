from app.api.v1.routes.auth.router import router
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from app.api.v1.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserOut
from app.utils.response import api_response

@router.get("/me")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    user_out = UserOut.model_validate(current_user)
    return api_response(
        data=jsonable_encoder(user_out),
        message="Current user profile retrieved successfully.",
        status_code=status.HTTP_200_OK
    )
