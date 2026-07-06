import unittest
from datetime import date

from fastapi import HTTPException

from app.models.book import Book, BookAvailability
from app.models.book_borrow import BookBorrow, BorrowStatus
from app.models.membership import Membership, MembershipPlan, MembershipStatus, Payment, PaymentStatus, PaymentType
from app.models.user import User, UserRole, UserStatus
from app.services.user.borrow_book import BorrowBookService


class MembershipBorrowingTests(unittest.TestCase):
    def test_rejects_borrow_when_no_active_membership(self):
        user = User(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone="+1234567890",
            password="hashed",
            role=UserRole.USER,
            status=UserStatus.APPROVED,
            is_email_verified=True,
        )
        book = Book(
            title="Django Basics",
            author="Ada",
            price=100.0,
            category_id=1,
            total_quantity=1,
            available_quantity=1,
            availability=BookAvailability.YES,
        )
        service = BorrowBookService(None)

        with self.assertRaises(HTTPException) as context:
            service.validate_borrow_request(user, book, None, [], [])

        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("active membership", str(context.exception.detail).lower())

    def test_allows_borrow_when_membership_is_active_and_book_available(self):
        user = User(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone="+1234567890",
            password="hashed",
            role=UserRole.USER,
            status=UserStatus.APPROVED,
            is_email_verified=True,
        )
        plan = MembershipPlan(name="Basic", price=200, validity_days=30, max_books=2)
        membership = Membership(
            user_id=user.id or 1,
            plan_id=1,
            start_date=date.today(),
            expiry_date=date.today(),
            status=MembershipStatus.ACTIVE,
        )
        membership.plan = plan
        book = Book(
            title="Django Basics",
            author="Ada",
            price=100.0,
            category_id=1,
            total_quantity=1,
            available_quantity=1,
            availability=BookAvailability.YES,
        )

        service = BorrowBookService(None)
        service.validate_borrow_request(user, book, membership, [], [])


if __name__ == "__main__":
    unittest.main()
