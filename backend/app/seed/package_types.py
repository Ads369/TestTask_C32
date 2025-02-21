from app.db.models.package_type import PackageType
from app.db.mysql import AsyncSessionLocal
from sqlalchemy import select


async def seed_package_types():
    async with AsyncSessionLocal() as session:
        # Check if any package types already exist
        result = await session.execute(select(PackageType))
        existing = result.scalars().first()
        if existing:
            return

        initial_types = [
            PackageType(name="Одежда"),
            PackageType(name="Электроника"),
            PackageType(name="Разное"),
        ]
        session.add_all(initial_types)
        await session.commit()
        print("Seeded PackageType data.")
