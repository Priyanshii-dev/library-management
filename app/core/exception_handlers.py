import logging
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(x) for x in e["loc"]), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Validation error.",
            "statusCode": 422,
            "data": [],
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP exception: {exc.detail}")

    if isinstance(exc.detail, dict):
        detail = exc.detail
        message = detail.get("message") or "HTTP error."
        status_code = detail.get("statusCode") or exc.status_code
        data = detail.get("data") or []
    else:
        message = exc.detail if isinstance(exc.detail, str) else "HTTP error."
        status_code = exc.status_code
        data = []

    return JSONResponse(
        status_code=status_code,
        content={
            "error": True,
            "message": message,
            "statusCode": status_code,
            "data":[],
        },
    )


async def db_error_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "A database error occurred.",
            "statusCode": 500,
            "data": [],
        },
    )


async def unhandled_error_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "An unexpected error occurred.",
            "statusCode": 500,
            "data": [],
        },
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(SQLAlchemyError, db_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
