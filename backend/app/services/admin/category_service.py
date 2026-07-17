import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.category import Category
from app.schemas.book import CategoryCreate, CategoryUpdate, CategoryOut

logger = logging.getLogger(__name__)


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_categories(self) -> list[CategoryOut]:
        stmt = select(Category).order_by(Category.name)
        result = await self.db.execute(stmt)
        categories = result.scalars().all()
        return [CategoryOut.model_validate(category) for category in categories]

    async def create_category(self, data: CategoryCreate) -> CategoryOut:
        stmt = select(Category).where(Category.name == data.name)
        existing = await self.db.execute(stmt)
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists",
            )

        category = Category(
            name=data.name,
            description=data.description,
        )

        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return CategoryOut.model_validate(category)

    async def update_category(self, category_id: int, data: CategoryUpdate) -> CategoryOut:
        stmt = select(Category).where(Category.id == category_id)
        result = await self.db.execute(stmt)
        category = result.scalar_one_or_none()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        if data.name:
            stmt = select(Category).where(Category.name == data.name, Category.id != category_id)
            existing = await self.db.execute(stmt)
            if existing.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category name already in use",
                )
            category.name = data.name

        if data.description is not None:
            category.description = data.description

        await self.db.commit()
        await self.db.refresh(category)
        return CategoryOut.model_validate(category)

    async def delete_category(self, category_id: int) -> None:
        stmt = select(Category).where(Category.id == category_id)
        result = await self.db.execute(stmt)
        category = result.scalar_one_or_none()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        await self.db.delete(category)
        await self.db.commit()
