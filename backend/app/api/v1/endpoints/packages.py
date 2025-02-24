from typing import Annotated, List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, status
from fastapi.params import Body, Path
from pydantic import Field
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


@router.get(
    "/packages",
    response_model=List[PackageOut],
    summary="Retrieve Packages",
    description=(
        "Retrieve a paginated list of packages for the authenticated user. "
        "The endpoint uses the provided user session to fetch packages and "
        "supports pagination through the 'skip' and 'limit' query parameters."
    ),
)
async def get_packages(
    service: PackageService = Depends(get_package_service),
    user_session: str = Depends(validate_user_session),
    limit: Annotated[
        int,
        Query(
            title="Limit",
            description="Maximum number of records to return",
            ge=1,
        ),
    ] = 100,
    skip: Annotated[
        int,
        Query(
            title="Skip",
            description="Number of records to skip for pagination",
            ge=0,
        ),
    ] = 0,
) -> List[PackageOut]:
    """
    Retrieve a paginated list of packages for the authenticated user session.

    **Parameters:**
    - **service**: An instance of PackageService injected via dependency injection.
      This service handles business logic related to packages.
    - **user_session**: A validated user session string used to identify the user.
    - **skip**: (Optional) The number of records to skip for pagination. Defaults to 0.
    - **limit**: (Optional) The maximum number of records to return. Defaults to 100.

    **Returns:**
    A list of packages conforming to the PackageOut schema.

    **Example:**
    A GET request to `/packages?skip=10&limit=50` will return packages starting from
    the 11th record, up to 50 records.
    """
    packages = await service.get_packages(user_session, skip=skip, limit=limit)
    return packages


@router.get("/packages/{package_id}", response_model=PackageOut)
async def get_package(
    package_id: Annotated[
        int,
        Path(
            title="Package ID",
            description="The unique identifier of the package to retrieve",
            ge=1,
        ),
    ],
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
    # package: PackageCreate,
    package: Annotated[
        PackageCreate,
        Body(
            ...,
            example={
                "name": "Standard Package",
                "weight": 2.5,
                "type_id": 1,
                "content_cost": 25.0,
            },
            description=(
                "The package details required to create a new package. "
                "This includes:\n"
                "- **name**: The name of the package (max length 255).\n"
                "- **weight**: The weight of the package (a positive float).\n"
                "- **type_id**: The identifier for the package type.\n"
                "- **content_cost**: The cost of the package's content (must be greater than 0).\n"
                "- **user_session**: (Optional) A user session string; if omitted, "
                "the system uses the session derived from the authenticated user."
            ),
        ),
    ],
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
    package_id: Annotated[
        int,
        Path(
            title="Package ID",
            description="The unique identifier of the package to retrieve",
            ge=1,
        ),
    ],
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
    package_id: Annotated[
        int,
        Path(
            title="Package ID",
            description="The unique identifier of the package to retrieve",
            ge=1,
        ),
    ],
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
