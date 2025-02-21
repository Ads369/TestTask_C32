import pytest
from app.db.models.package_type import PackageType
from sqlalchemy.future import select


@pytest.mark.asyncio
async def test_crud_operations(async_session):
    # Create a new record
    new_record = PackageType(name="Test Package")
    async_session.add(new_record)
    await async_session.flush()  # Flush to assign an ID

    # Read: Verify that the record exists in the session
    result = await async_session.execute(
        select(PackageType).where(PackageType.id == new_record.id)
    )
    record = result.scalar_one_or_none()
    assert record is not None
    assert record.name == "Test Package"

    # Update: Modify the record's name
    record.name = "Updated Package"
    await async_session.flush()  # Save the update in the transaction

    # Read: Confirm the update
    result = await async_session.execute(
        select(PackageType).where(PackageType.id == record.id)
    )
    updated_record = result.scalar_one_or_none()
    assert updated_record.name == "Updated Package"

    # Delete: Remove the record
    await async_session.delete(updated_record)
    await async_session.flush()

    # Read: Ensure the record has been deleted (should be None)
    result = await async_session.execute(
        select(PackageType).where(PackageType.id == updated_record.id)
    )
    deleted_record = result.scalar_one_or_none()
    assert deleted_record is None

    # No need to explicitly call rollback here.
    # The fixture will roll back the transaction after the test,
    # so your working database remains unchanged.
