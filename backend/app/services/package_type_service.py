from typing import List

from app.api.v1.schemas.package import (
    PackageType,
)
from app.db.repositories.package_type_repository import PackageTypeRepository


class PackageTypeService:
    def __init__(self, repository: PackageTypeRepository):
        self.repository = repository

    async def get_package_types(self, skip: int, limit: int) -> List[PackageType]:
        return await self.repository.list()
