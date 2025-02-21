from fastapi import APIRouter

from .healthcheck import router as health_checker_router
from .package_types import router as package_types_router
from .packages import router as packages_router

router = APIRouter()

router.include_router(router=health_checker_router, prefix="/system", tags=["System"])
router.include_router(router=packages_router, prefix="/packages", tags=["Packages"])
router.include_router(
    package_types_router, prefix="/package-types", tags=["Package Types"]
)
