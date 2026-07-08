from fastapi import APIRouter

from app.api.v1.agent import router as agent_router
from app.api.v1.health import router as health_router
from app.api.v1.root import router as root_router
from app.api.v1.version import router as version_router

api_router = APIRouter()

api_router.include_router(root_router, tags=["Root"])
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(version_router, tags=["Version"])
api_router.include_router(agent_router, prefix="/agent", tags=["Agent"])
