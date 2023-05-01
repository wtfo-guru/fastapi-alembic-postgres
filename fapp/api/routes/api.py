from fastapi import APIRouter

from fapp.api.routes import exposed, covered

router = APIRouter()
router.include_router(exposed.router, tags=["exposed"])
