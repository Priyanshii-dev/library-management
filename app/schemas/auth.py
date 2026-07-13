from pydantic import BaseModel, Field, field_validator, constr
import re

# Validation regexes
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
PASSWORD_REGEX = r"^.{8,13}$"
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


def validate_emails(v: str) -> str:
    if not re.match(EMAIL_REGEX, v):
        raise ValueError("Please provide a valid email address.")
    return v


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_role: str
    user_id: int
    id: int
    email: str


class RefreshRequest(BaseModel):
    refresh_token: str


class OTPRequest(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "user@example.com"})

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return validate_emails(v)


class OTPVerifyRequest(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "user@example.com"})
    otp_code: str = Field(
        ..., min_length=6, max_length=6, json_schema_extra={"example": "123456"}
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return validate_emails(v)


class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "user@example.com"})

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return validate_emails(v)


class PasswordResetRequest(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "user@example.com"})
    otp_code: str = Field(
        ..., min_length=6, max_length=6, json_schema_extra={"example": "123456"}
    )
    new_password: str = Field(
        ..., json_schema_extra={"example": "StrongPass@123"}
    )

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        return validate_password_complexity(v)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return validate_emails(v)


class LoginRequest(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "user@example.com"})
    password: str = Field(..., json_schema_extra={"example": "StrongPass@123"})

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return validate_password_complexity(v)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return validate_emails(v)


class RegistrationRequest(BaseModel):
    first_name: constr(strip_whitespace=True, min_length=1, max_length=100, pattern=NAME_REGEX) = Field(
        ..., json_schema_extra={"example": "John"}
    )
    last_name: constr(strip_whitespace=True, min_length=1, max_length=100, pattern=NAME_REGEX) = Field(
        ..., json_schema_extra={"example": "Doe"}
    )
    phone: constr(pattern=PHONE_REGEX) = Field(
        ..., json_schema_extra={"example": "+1234567890"}
    )
    email: str = Field(..., json_schema_extra={"example": "user@example.com"})
    password: str = Field(..., json_schema_extra={"example": "StrongPass@123"})

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return validate_password_complexity(v)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return validate_emails(v)


class ApprovalStatusResponse(BaseModel):
    status: str
    message: str