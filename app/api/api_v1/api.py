from fastapi import APIRouter

from app.api.api_v1.endpoints import exposed

api_router = APIRouter()
api_router.include_router(exposed.router, prefix="/", tags=["exposed"])
