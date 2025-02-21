from typing import List, Optional

from app.api.v1.schemas.package import PackageType as PackageTypeSchema
from app.db.models.package_type import PackageType
from app.db.repositories.base import BaseReadRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PackageTypeRepository(BaseReadRepository[PackageType, PackageTypeSchema]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[PackageTypeSchema]:
        return None

    async def list(self, skip: int = 0, limit: int = 100) -> List[PackageTypeSchema]:
        query = select(PackageType).offset(skip).limit(limit)
        db_instances = await self.session.execute(query)
        results = db_instances.scalars().all()
        output = [PackageTypeSchema.model_validate(record) for record in results]
        return output
