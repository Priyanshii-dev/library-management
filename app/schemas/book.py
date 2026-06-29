from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None


class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    category_id: int
    publication_year: Optional[int] = None
    total_quantity: int = Field(..., gt=0)
    available_quantity: Optional[int] = Field(None, ge=0)


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = None
    publication_year: Optional[int] = None
    total_quantity: Optional[int] = Field(None, gt=0)
    available_quantity: Optional[int] = Field(None, ge=0)
    availability: Optional[str] = None


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    price: float
    category_id: int
    publication_year: Optional[int] = None
    total_quantity: int
    available_quantity: int
    availability: str
    added_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookBorrowRequest(BaseModel):
    book_id: int


class BookActionRequest(BaseModel):
    borrow_id: int


class BookBorrowHistoryOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    status: str
    borrowed_at: datetime
    due_date: datetime
    renewed_at: Optional[datetime] = None
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BookBorrowAdminOut(BookBorrowHistoryOut):
    book_title: str
    user_email: str
