from fastapi import APIRouter

from app.api.api_v1.endpoints import exposed, user

api_router = APIRouter()

api_router.include_router(exposed.router, tags=["exposed"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
