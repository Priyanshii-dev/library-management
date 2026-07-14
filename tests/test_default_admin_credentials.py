import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from app.core.lifespan import lifespan
from app.core.security import verify_password
from app.models.user import User


class DefaultAdminBootstrapTests(unittest.IsolatedAsyncioTestCase):
    async def test_lifespan_creates_admin_with_complex_password(self):
        session = AsyncMock()
        result = MagicMock()
        result.scalar_one_or_none.return_value = None
        session.execute.return_value = result
        session.add = MagicMock()
        session.commit = AsyncMock()

        mock_engine = MagicMock()
        mock_engine.dispose = AsyncMock()

        with patch("app.core.lifespan.async_session_maker") as maker, patch(
            "app.core.lifespan.engine", mock_engine
        ):
            maker.return_value.__aenter__.return_value = session
            maker.return_value.__aexit__.return_value = None

            async with lifespan(object()):
                pass

        created_user = session.add.call_args[0][0]
        self.assertIsInstance(created_user, User)
        self.assertTrue(verify_password("Admin@123", created_user.password))


if __name__ == "__main__":
    unittest.main()
