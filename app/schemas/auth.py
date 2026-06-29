from pydantic import BaseModel, Field, constr

# Validation regexes
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,72}$"
PHONE_REGEX = r"^\+?\d{7,15}$"
NAME_REGEX = r"^[A-Za-z ,.'-]{1,100}$"


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
    email: constr(regex=EMAIL_REGEX)


class OTPVerifyRequest(BaseModel):
    email: constr(regex=EMAIL_REGEX)
    otp_code: str = Field(..., min_length=6, max_length=6)


class LoginRequest(BaseModel):
    email: constr(regex=EMAIL_REGEX)
    password: constr(regex=PASSWORD_REGEX)


class RegistrationRequest(BaseModel):
    first_name: constr(strip_whitespace=True, min_length=1, max_length=100, regex=NAME_REGEX)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=100, regex=NAME_REGEX)
    phone: constr(regex=PHONE_REGEX)
    email: constr(regex=EMAIL_REGEX)
    password: constr(regex=PASSWORD_REGEX)


class ApprovalStatusResponse(BaseModel):
    status: str  # "Pending", "Approved", "Rejected"
    message: str
