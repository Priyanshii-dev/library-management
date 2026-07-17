import json
import unittest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException

from app.core.exception_handlers import http_exception_handler
from app.models.user import User, UserRole, UserStatus
from app.services.auth.forgot_password import ForgotPasswordService
from app.services.auth.reset_password import ResetPasswordService


class FakeResult:
    def __init__(self, value):
        self._value = value

    def scalar_one_or_none(self):
        return self._value


class FakeDB:
    def __init__(self, user):
        self.user = user
        self.commits = 0

    async def execute(self, stmt):
        return FakeResult(self.user)

    async def commit(self):
        self.commits += 1


class AuthPasswordResetTests(unittest.IsolatedAsyncioTestCase):
    async def test_forgot_password_generates_otp_and_sends_email(self):
        user = User(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone="+1234567890",
            password="hashed-password",
            role=UserRole.USER,
            status=UserStatus.APPROVED,
            is_email_verified=True,
        )
        db = FakeDB(user)

        with patch("app.services.auth.forgot_password.OTPService.generate_otp", return_value="123456"), patch(
            "app.services.auth.forgot_password.EmailService.send_password_reset_email",
            new_callable=AsyncMock,
        ) as send_email:
            response = await ForgotPasswordService(db).send_reset_link("jane@example.com")

        self.assertEqual(response["message"], "If the account exists, a password reset OTP has been sent")
        self.assertEqual(user.otp_code, "123456")
        self.assertIsNotNone(user.otp_created_at)
        self.assertEqual(db.commits, 1)
        send_email.assert_awaited_once()

    async def test_reset_password_updates_password_and_clears_otp(self):
        user = User(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone="+1234567890",
            password="old-hash",
            role=UserRole.USER,
            status=UserStatus.APPROVED,
            is_email_verified=True,
            otp_code="123456",
            otp_created_at=datetime.now(timezone.utc),
        )
        db = FakeDB(user)

        with patch("app.services.auth.reset_password.OTPService.verify_otp", return_value=True):
            response = await ResetPasswordService(db).reset_password(
                email="jane@example.com",
                otp_code="123456",
                new_password="NewPass@123",
            )

        self.assertEqual(response["message"], "Password reset successfully")
        self.assertNotEqual(user.password, "old-hash")
        self.assertIsNone(user.otp_code)
        self.assertIsNone(user.otp_created_at)
        self.assertEqual(db.commits, 1)

    async def test_http_exception_handler_returns_structured_error_payload(self):
        response = await http_exception_handler(
            None,
            HTTPException(
                status_code=400,
                detail={
                    "message": "Email must be verified before resetting the password",
                    "statusCode": 400,
                    "data": [],
                },
            ),
        )

        body = json.loads(response.body)
        self.assertTrue(body["error"])
        self.assertEqual(body["message"], "Email must be verified before resetting the password")
        self.assertEqual(body["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()
