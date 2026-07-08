import sys
from fastapi import APIRouter
from typing import Any, Dict
from app.config.settings import settings

router = APIRouter()

@router.get("/version")
async def version_endpoint() -> Dict[str, Any]:
    return {
        "application_version": settings.VERSION,
        "python_version": sys.version,
        "api_version": "v1",
        "environment": settings.ENVIRONMENT,
    }
