from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.databas import get_async_db
from app.api.v1.schemas.package import PackageType as PackageTypeSchema
from app.db.repositories.package_type_repository import PackageTypeRepository
from app.services.package_type_service import PackageTypeService

router = APIRouter()


def get_package_type_service(db: AsyncSession = Depends(get_async_db)):
    package_repository = PackageTypeRepository(session=db)
    return PackageTypeService(package_repository)


@router.get("/", response_model=List[PackageTypeSchema])
async def get_package_types(
    service: PackageTypeService = Depends(get_package_type_service),
    skip: int = 0,
    limit: int = 100,
):
    return await service.get_package_types(skip=skip, limit=limit)
