from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class MembershipPlanCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    validity_days: int = Field(..., gt=0)
    max_books: int = Field(..., gt=0)


class MembershipPlanOut(BaseModel):
    id: int
    name: str
    price: float
    validity_days: int
    max_books: int
    created_at: datetime

    class Config:
        from_attributes = True


class MembershipPurchaseRequest(BaseModel):
    plan_id: int


class MembershipOut(BaseModel):
    id: int
    user_id: int
    plan_id: int
    start_date: date
    expiry_date: date
    status: str
    payment_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaymentOut(BaseModel):
    id: int
    user_id: int
    borrow_id: Optional[int] = None
    amount: float
    payment_type: str
    payment_status: str
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
