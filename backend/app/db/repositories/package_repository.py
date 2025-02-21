from typing import List, Optional

from app.api.v1.schemas.package import (
    PackageCreate,
    PackageOut,
    PackageUpdate,
)
from app.db.models.package import Package
from app.db.repositories.base import BaseCRUDRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class PackageRepository(
    BaseCRUDRepository[Package, PackageOut, PackageCreate, PackageUpdate]
):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, id: int, user_session: str) -> Optional[PackageOut]:
        query = (
            select(Package)
            .options(joinedload(Package.type))
            .where(Package.id == id)
            .where(Package.user_session == user_session)
        )
        result = await self.session.execute(query)
        db_instance = result.scalar_one_or_none()
        if db_instance is not None:
            return PackageOut.model_validate(db_instance)
        return None

    async def list(
        self, user_session: str, skip: int = 0, limit: int = 100
    ) -> List[PackageOut]:
        query = (
            select(Package)
            .options(joinedload(Package.type))
            .where(Package.user_session == user_session)
        )
        db_instances = await self.session.execute(query)
        results = db_instances.scalars().all()
        output = [PackageOut.model_validate(record) for record in results]
        return output

    async def create(self, obj_in: PackageCreate) -> PackageOut:
        db_obj = Package(
            name=obj_in.name,
            weight=obj_in.weight,
            type_id=obj_in.type_id,
            content_cost=obj_in.content_cost,
            user_session=obj_in.user_session,  # Make sure this is included
        )
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return PackageOut.model_validate(db_obj)

    async def update(self, db_obj: Package, obj_in: PackageUpdate) -> PackageOut:
        return await super().update(db_obj, obj_in)

    async def delete(self, id: int) -> Optional[PackageOut]:
        return await super().delete(id)

    async def get_unprocessed_packages(self) -> List[Package]:
        """Get all packages without delivery cost."""
        query = select(Package).where(Package.delivery_cost.is_(None))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def bulk_update_delivery_costs(self, packages: List[Package]) -> None:
        """Update delivery costs for multiple packages."""
        for package in packages:
            self.session.add(package)
        await self.session.commit()
