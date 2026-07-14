import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from app.models.user import User, UserRole, UserStatus
from app.schemas.auth import OTPVerifyRequest
from app.services.auth.verify_otp import VerifyOTPService


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


class VerifyEmailResponseTests(unittest.IsolatedAsyncioTestCase):
    async def test_verify_email_returns_clean_payload(self):
        user = User(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone="+1234567890",
            password="hashed-password",
            role=UserRole.USER,
            status=UserStatus.PENDING,
            is_email_verified=False,
            otp_code="123456",
            otp_created_at=datetime.now(timezone.utc),
        )
        db = FakeDB(user)

        with patch("app.services.auth.verify_otp.OTPService.verify_otp", return_value=True):
            response = await VerifyOTPService(db).verify_email_otp(
                OTPVerifyRequest(email="jane@example.com", otp_code="123456")
            )

        self.assertEqual(response, {"email_verified": True, "user_id": user.id})
        self.assertNotIn("message", response)
        self.assertNotIn("id", response)


if __name__ == "__main__":
    unittest.main()
