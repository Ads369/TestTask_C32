import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.package_type_repository import PackageTypeRepository
from app.db.models.package_type import PackageType
from app.api.v1.schemas.package import PackageType as PackageTypeSchema

@pytest.fixture
def package_type_repository(test_async_session: AsyncSession):
    return PackageTypeRepository(test_async_session)

@pytest.fixture
async def sample_package_types(test_async_session: AsyncSession):
    # Create sample package types for testing
    package_types = [
        PackageType(id=1, name="Standard", description="Standard package"),
        PackageType(id=2, name="Express", description="Express package"),
        PackageType(id=3, name="Premium", description="Premium package"),
    ]

    for pt in package_types:
        test_async_session.add(pt)
    await test_async_session.commit()

    return package_types

@pytest.mark.asyncio
async def test_get_existing_package_type(
    package_type_repository: PackageTypeRepository,
    sample_package_types: list[PackageType],
):
    # Test getting an existing package type
    result = await package_type_repository.get(id=1)

    assert result is not None
    assert isinstance(result, PackageTypeSchema)
    assert result.id == 1
    assert result.name == "Standard"
    assert result.description == "Standard package"

@pytest.mark.asyncio
async def test_get_non_existing_package_type(
    package_type_repository: PackageTypeRepository,
    sample_package_types: list[PackageType],  # Add this to ensure DB is initialized
):
    # Test getting a non-existing package type
    result = await package_type_repository.get(id=999)
    assert result is None

@pytest.mark.asyncio
async def test_list_package_types(
    package_type_repository: PackageTypeRepository,
    sample_package_types: list[PackageType],
):
    # Test listing all package types
    results = await package_type_repository.list()

    assert len(results) == 3
    assert all(isinstance(item, PackageTypeSchema) for item in results)
    assert [item.id for item in results] == [1, 2, 3]

@pytest.mark.asyncio
async def test_list_package_types_with_pagination(
    package_type_repository: PackageTypeRepository,
    sample_package_types: list[PackageType],
):
    # Test pagination
    results = await package_type_repository.list(skip=1, limit=2)

    assert len(results) == 2
    assert all(isinstance(item, PackageTypeSchema) for item in results)
    assert [item.id for item in results] == [2, 3]

@pytest.mark.asyncio
async def test_list_package_types_empty(
    package_type_repository: PackageTypeRepository,
):
    # Test listing when no package types exist
    results = await package_type_repository.list()
    assert len(results) == 0
    assert isinstance(results, list)
