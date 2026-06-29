from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_role: str  # "Admin" or "User"
    user_id: int
    id: int
    email: str


class RefreshRequest(BaseModel):
    refresh_token: str


class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp_code: str = Field(..., min_length=6, max_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class RegistrationRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=1, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class ApprovalStatusResponse(BaseModel):
    status: str  # "Pending", "Approved", "Rejected"
    message: str
