import random
import string
from datetime import datetime, timezone, timedelta
from app.core.config import settings


class OTPService:
    """Service for OTP generation and verification."""

    @staticmethod
    def generate_otp() -> str:
        """Generate a random OTP code."""
        return ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))

    @staticmethod
    def verify_otp(stored_otp: str | None, provided_otp: str, created_at: datetime | None) -> bool:
        """
        Verify if the provided OTP matches the stored OTP and is not expired.
        
        Args:
            stored_otp: The OTP stored in the database
            provided_otp: The OTP provided by the user
            created_at: When the OTP was created
            
        Returns:
            True if OTP is valid and not expired, False otherwise
        """
        if not stored_otp or not created_at:
            return False
        
        # Check if OTP matches
        if stored_otp != provided_otp:
            return False
        
        # Check if OTP is expired
        current_time = datetime.now(timezone.utc)
        expiry_time = created_at + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
        if current_time > expiry_time:
            return False
        
        return True

    @staticmethod
    def is_otp_expired(created_at: datetime | None) -> bool:
        """Check if OTP has expired."""
        if not created_at:
            return True
        
        current_time = datetime.now(timezone.utc)
        expiry_time = created_at + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
        return current_time > expiry_time
