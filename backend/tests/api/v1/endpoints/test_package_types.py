import pytest

# from app.db.models.package_type import PackageType
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession


# @pytest.mark.asyncio
# async def test_get_package_types_empty(client: AsyncClient):
#     response = await client.get("/api/v1/package_types/")
#     assert response.status_code == 200
#     assert response.json() == []


# @pytest.mark.asyncio
# async def test_get_package_types_with_data(client: AsyncClient, session: AsyncSession):
#     # Create and add test data
#     package_type = PackageType(name="TestType")
#     session.add(package_type)
#     await session.commit()  # Commit the changes

#     # Call the endpoint
#     response = await client.get("/api/v1/package_types/")
#     assert response.status_code == 200
#     data = response.json()

#     # Validate response
#     assert len(data) == 1
#     assert data[0]["name"] == "TestType"


# @pytest.mark.asyncio
# async def test_foo_api_en(async_client):
#     response = await async_client.get(
#         "api/examples/foo", headers={"Accept-Language": "en;q=0.8,"}
#     )
#     assert response.text == "bar"


# @pytest.mark.asyncio
# async def test_foo_api_ru(async_client):
#     response = await async_client.get(
#         "api/examples/foo", headers={"Accept-Language": "ru;q=0.8,"}
#     )
#     assert response.text == "бар"


# @pytest.mark.asyncio
# async def test_pydantic_validation_error_en(async_client):
#     response = await async_client.post("api/examples/foo", json={})
#     assert response.status_code == 422
#     assert response.json()["detail"][0]["msg"] == "Field required"


# @pytest.mark.asyncio
# async def test_pydantic_validation_error_with_locale(async_client):
#     response = await async_client.post(
#         "api/examples/foo", headers={"Accept-Language": "ru;q=0.8,"}, json={}
#     )
#     assert response.status_code == 422
#     assert response.json()["detail"][0]["msg"] == "Обязательное поле"


# @pytest.mark.asyncio
# async def test_pagination(async_client):
#     response = await async_client.get(
#         "api/examples/a-lot-of-data?page=1&size=10",
#     )
#     assert response.status_code == 200
#     assert response.json()["total"] == 1000
#     assert response.json()["items"][0]["foo"] == "0"
#     assert response.json()["items"][-1]["foo"] == "9"


@pytest.mark.asyncio
async def test_pagination(async_client):
    response = await async_client.get(
        "/api/v1/package_types/",
    )
    assert response.status_code == 200
