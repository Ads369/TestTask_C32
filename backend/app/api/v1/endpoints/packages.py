from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# from app.db.repositories.package_repository import PackageRepository
# from app.schemas.package import Package, PackageCreate, PackageUpdate
# from app.services.package_service import PackageService
from app.api.v1.schemas.package import Package, PackageCreate
from app.db.mysql import get_db

router = APIRouter()


def get_package_service(db: Session = Depends(get_db)):
    package_repository = PackageRepository(db)
    return PackageService(package_repository)


@router.post("/", response_model=Package)
def create_package(
    package: PackageCreate,
    service: PackageService = Depends(get_package_service),
):
    return service.create_package(package)


@router.get("/{package_id}", response_model=Package)
def read_package(
    package_id: int, service: PackageService = Depends(get_package_service)
):
    db_package = service.get_package(package_id)
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return db_package


@router.put("/{package_id}", response_model=Package)
def update_package(
    package_id: int,
    package: PackageUpdate,
    service: PackageService = Depends(get_package_service),
):
    return service.update_package(package_id, package)


@router.delete("/{package_id}")
def delete_package(
    package_id: int, service: PackageService = Depends(get_package_service)
):
    service.delete_package(package_id)
    return {"message": "Package deleted"}
