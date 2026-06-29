from fastapi import Depends, Path, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin
from app.api.v1.routes.admin.router import router
from app.db.session import get_db
from app.schemas.book import CategoryCreate, CategoryUpdate
from app.services.admin.category_service import CategoryService
from app.utils.response import api_response


@router.post("/categories")
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    category = await CategoryService(db).create_category(data)
    return api_response(
        data=jsonable_encoder(category),
        message="Category created successfully.",
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/categories")
async def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    categories = await CategoryService(db).list_categories()
    return api_response(
        data=jsonable_encoder(categories),
        message="Categories retrieved successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.patch("/categories/{category_id}")
async def update_category(
    data: CategoryUpdate,
    category_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    category = await CategoryService(db).update_category(category_id, data)
    return api_response(
        data=jsonable_encoder(category),
        message="Category updated successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_admin),
):
    await CategoryService(db).delete_category(category_id)
    return api_response(
        message="Category deleted successfully.",
        status_code=status.HTTP_200_OK,
    )
