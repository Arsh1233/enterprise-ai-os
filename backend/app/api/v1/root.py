from fastapi import APIRouter
from typing import Any, Dict
from app.config.settings import settings

router = APIRouter()

@router.get("/")
async def root_endpoint() -> Dict[str, Any]:
    return {
        "project_name": settings.PROJECT_NAME,
        "description": "Enterprise AI Operating System Backend Foundation",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "version": settings.VERSION,
    }
