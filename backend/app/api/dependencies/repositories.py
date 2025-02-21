from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.package_type_repository import PackageTypeRepository


async def get_package_type_repository(session: AsyncSession) -> PackageTypeRepository:
    return PackageTypeRepository(session)
