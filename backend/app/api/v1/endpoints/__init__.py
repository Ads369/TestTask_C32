from fastapi import APIRouter

from .healthcheck import router as health_checker_router

router = APIRouter()

router.include_router(router=health_checker_router, prefix="/system", tags=["System"])
