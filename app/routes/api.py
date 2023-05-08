from fastapi import APIRouter

from app.routes.exposed import exposed

# from app.routes.covered import covered

router = APIRouter()
router.include_router(exposed, tags=["exposed"])
# router.include_router(covered, tags=["covered"])
