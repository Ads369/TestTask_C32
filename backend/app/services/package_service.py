from app.api.v1.schemas.package import (
    PackageCreate,
    PackageUpdate,
)
from app.db.repositories.package_repository import PackageRepository


class PackageService:
    def __init__(self, repository: PackageRepository):
        self.repository = repository

    async def get_packages(self, user_session: str, skip: int = 0, limit: int = 100):
        return await self.repository.list(
            skip=skip, limit=limit, user_session=user_session
        )

    async def get_package_by_id(self, package_id: int, user_session: str):
        return await self.repository.get(package_id, user_session)

    async def create_package(self, package: PackageCreate, user_session: str):
        package_dict = package.model_dump()
        package_dict["user_session"] = user_session
        modified_package = PackageCreate(**package_dict)
        return await self.repository.create(modified_package)

    async def update_package(
        self, package_id: int, package_update: PackageUpdate, user_session: str
    ):
        # First verify the package belongs to the user_session
        existing_package = await self.repository.get(package_id, user_session)
        if not existing_package:
            return None
        return await self.repository.update(package_id, package_update)

    async def delete_package(self, package_id: int, user_session: str):
        # First verify the package belongs to the user_session
        existing_package = await self.repository.get(package_id, user_session)
        if not existing_package:
            return None
        return await self.repository.delete(package_id)
