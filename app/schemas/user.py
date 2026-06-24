from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    user_logo: Optional[str] = None  


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    role: str
    status: str
    user_logo: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_validator('user_logo', mode='before')
    @classmethod
    def convert_bytes_to_base64(cls, v):
        if isinstance(v, bytes):
            import base64
            return base64.b64encode(v).decode('utf-8')
        return v


class UserListOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    role: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserApprovalRequest(BaseModel):
    user_id: int
    status: str  # "Approved" or "Rejected"


class UserDetailResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    role: str
    status: str
    user_logo: Optional[str] = None 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_validator('user_logo', mode='before')
    @classmethod
    def convert_bytes_to_base64(cls, v):
        if isinstance(v, bytes):
            import base64
            return base64.b64encode(v).decode('utf-8')
        return v
