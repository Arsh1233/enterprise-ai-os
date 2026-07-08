import time
from datetime import datetime, timezone
from typing import Any, Dict

import redis.asyncio as redis
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.dependencies import get_redis
from app.config.settings import settings
from app.db.dependencies import get_db

router = APIRouter()
START_TIME = time.time()


@router.get("/health")
async def health_endpoint(
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> Dict[str, Any]:
    uptime = time.time() - START_TIME

    # Check DB
    db_status = "down"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "up"
    except Exception:
        pass

    # Check Redis
    redis_status = "down"
    try:
        await redis_client.ping()
        redis_status = "up"
    except Exception:
        pass

    status = "healthy" if db_status == "up" and redis_status == "up" else "unhealthy"

    return {
        "status": status,
        "database": db_status,
        "redis": redis_status,
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "uptime": round(uptime, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
