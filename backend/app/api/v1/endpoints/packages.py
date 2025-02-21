from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import validate_user_session
from app.api.dependencies.databas import get_async_db
from app.api.v1.schemas.package import PackageCreate, PackageOut, PackageUpdate
from app.db.repositories.package_repository import PackageRepository
from app.services.package_service import PackageService

router = APIRouter()


def get_package_service(db: AsyncSession = Depends(get_async_db)):
    package_repository = PackageRepository(session=db)
    return PackageService(package_repository)


@router.get("/packages", response_model=List[PackageOut])
async def get_packages(
    service: PackageService = Depends(get_package_service),
    user_session: str = Depends(validate_user_session),
    skip: int = 0,
    limit: int = 100,
) -> List[PackageOut]:
    packages = await service.get_packages(user_session, skip=skip, limit=limit)
    return packages


@router.get("/packages/{package_id}", response_model=PackageOut)
async def get_package(
    package_id: int,
    service: PackageService = Depends(get_package_service),
    user_session: str = Depends(validate_user_session),
):
    package = await service.get_package_by_id(package_id, user_session)
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Package with ID {package_id} not found",
        )
    return package


@router.post(
    "/packages"
    # , response_model=PackageOut, status_code=status.HTTP_201_CREATED
)
async def create_package(
    package: PackageCreate,
    service: PackageService = Depends(get_package_service),
    user_session: str = Depends(validate_user_session),
):
    try:
        new_package = await service.create_package(package, user_session)
        return new_package
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/packages/{package_id}", response_model=PackageOut)
async def update_package(
    package_id: int,
    package_update: PackageUpdate,
    service: PackageService = Depends(get_package_service),
    user_session: str = Depends(validate_user_session),
):
    try:
        updated_package = await service.update_package(
            package_id, package_update, user_session
        )
        if not updated_package:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Package with ID {package_id} not found",
            )
        return updated_package
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/packages/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_package(
    package_id: int,
    service: PackageService = Depends(get_package_service),
    user_session: str = Depends(validate_user_session),
):
    deleted = await service.delete_package(package_id, user_session)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Package with ID {package_id} not found",
        )
    return None
