from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config.settings import settings


def get_engine() -> AsyncEngine:
    return create_async_engine(
        settings.async_database_url,
        echo=settings.DB_ECHO,
        future=True,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


engine = get_engine()
