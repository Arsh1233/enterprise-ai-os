from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.root import router as root_router
from app.api.v1.router import api_router
from app.cache.redis import redis_client
from app.config.settings import settings
from app.db.engine import engine
from app.exceptions.handlers import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.logging.logger import get_logger, setup_logging
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.process_time import ProcessTimeMiddleware
from app.middleware.request_id import RequestIDMiddleware

logger = get_logger("lifespan")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup logging
    setup_logging()
    logger.info("startup", message="Application starting up", env=settings.ENVIRONMENT)

    # Initialize Redis
    await redis_client.connect()

    yield

    # Shutdown logging
    logger.info("shutdown", message="Application shutting down")

    # Close Redis
    await redis_client.disconnect()

    # Dispose Database engine
    await engine.dispose()


def create_app() -> FastAPI:
    # Setup structured logging early in case of startup errors
    setup_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    # Add standard middlewares
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom middlewares (in reverse execution order)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ProcessTimeMiddleware)
    app.add_middleware(RequestIDMiddleware)

    # Add exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Include routers
    app.include_router(root_router)
    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app
