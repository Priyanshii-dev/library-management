import logging
from contextlib import asynccontextmanager
from app.db.session import engine

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app):
    logger.info("Database tables ready.")
    yield
    await engine.dispose()
    logger.info("Database connections closed.")