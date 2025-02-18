import pytest
from app.db.models.package import Package


@pytest.mark.asyncio
async def test_create_and_retrieve(async_session):
    # Create a new record
    new_record = Package(name="Test Record")
    async_session.add(new_record)
    await async_session.commit()
    # Refresh to load data (including the auto-generated ID)
    await async_session.refresh(new_record)

    assert new_record.id is not None, "Record ID should be generated after commit."

    # Retrieve the record by primary key
    retrieved = await async_session.get(Package, new_record.id)
    assert retrieved is not None, "Should retrieve the record by its ID."
    assert (
        retrieved.name == "Test Record"
    ), "Retrieved record should have the correct name."
