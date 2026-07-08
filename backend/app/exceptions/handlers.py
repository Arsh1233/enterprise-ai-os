from fastapi import Request
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.logging.logger import get_logger

logger = get_logger("exceptions")

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:
    logger.warning("validation_error", errors=exc.errors())
    return ORJSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> ORJSONResponse:
    logger.warning("http_exception", status_code=exc.status_code, detail=exc.detail)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def unhandled_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    logger.exception("unhandled_exception", error=str(exc))
    return ORJSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
