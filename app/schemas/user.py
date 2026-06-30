from pydantic import BaseModel, Field, field_validator, constr
from typing import Optional
from datetime import datetime
import re

# Validation regexes
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
PHONE_REGEX = r"^\+?\d{7,15}$"
NAME_REGEX = r"^[A-Za-z ,.'-]{1,100}$"


def validate_password_complexity(v: str) -> str:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,13}$"
    if not re.match(pattern, v):
        raise ValueError(
            "Password must be 8-13 characters and include at least one "
            "uppercase letter, lowercase letter, digit, and special character."
        )
    return v


class UserBase(BaseModel):
    first_name: constr(strip_whitespace=True, min_length=1, max_length=100, pattern=NAME_REGEX)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=100, pattern=NAME_REGEX)
    email: constr(pattern=EMAIL_REGEX)
    phone: constr(pattern=PHONE_REGEX)


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return validate_password_complexity(v)


class UserUpdate(BaseModel):
    first_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=100, pattern=NAME_REGEX)] = None
    last_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=100, pattern=NAME_REGEX)] = None
    phone: Optional[constr(pattern=PHONE_REGEX)] = None
    email: Optional[constr(pattern=EMAIL_REGEX)] = None
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

    model_config = {"from_attributes": True}

    @field_validator("user_logo", mode="before")
    @classmethod
    def convert_bytes_to_base64(cls, v):
        if isinstance(v, bytes):
            import base64
            return base64.b64encode(v).decode("utf-8")
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

    model_config = {"from_attributes": True}


class UserApprovalRequest(BaseModel):
    user_id: int
    status: str


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

    model_config = {"from_attributes": True}

    @field_validator("user_logo", mode="before")
    @classmethod
    def convert_bytes_to_base64(cls, v):
        if isinstance(v, bytes):
            import base64
            return base64.b64encode(v).decode("utf-8")
        return v