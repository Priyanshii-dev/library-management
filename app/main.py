import logging
from fastapi import FastAPI
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.middleware import register_middleware
from app.core.exception_handlers import register_exception_handlers
from app.api.v1.router import api_router
from app.models import user, category, book, book_borrow, membership  # noqa: F401

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="2.0.0",
        description="Library Management System with Role-Based Access Control",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    register_middleware(app)
    register_exception_handlers(app)
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV, "version": "2.0.0"}

    @app.get("/", tags=["Root"])
    async def root():
        return {"message": "Welcome to Library Management System API", "version": "2.0.0", "docs": "/docs"}

    return app

app = create_app()