from pydantic import BaseModel, Field, field_validator, constr
from typing import Optional
from datetime import datetime


# Validation regexes (keep in sync with auth schema)
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,72}$"
PHONE_REGEX = r"^\+?\d{7,15}$"
NAME_REGEX = r"^[A-Za-z ,.'-]{1,100}$"



class UserBase(BaseModel):
    first_name: constr(strip_whitespace=True, min_length=1, max_length=100, regex=NAME_REGEX)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=100, regex=NAME_REGEX)
    email: constr(regex=EMAIL_REGEX)
    phone: constr(regex=PHONE_REGEX)


class UserCreate(UserBase):
    password: constr(regex=PASSWORD_REGEX)


class UserUpdate(BaseModel):
    first_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=100, regex=NAME_REGEX)] = None
    last_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=100, regex=NAME_REGEX)] = None
    phone: Optional[constr(regex=PHONE_REGEX)] = None
    email: Optional[constr(regex=EMAIL_REGEX)] = None
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
