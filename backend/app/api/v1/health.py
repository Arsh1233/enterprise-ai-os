from fastapi import APIRouter
from typing import Any, Dict
from datetime import datetime, timezone
import time
from app.config.settings import settings

router = APIRouter()
START_TIME = time.time()

@router.get("/health")
async def health_endpoint() -> Dict[str, Any]:
    uptime = time.time() - START_TIME
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "uptime": round(uptime, 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
