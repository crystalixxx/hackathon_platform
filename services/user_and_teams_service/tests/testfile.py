import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_profile_route(client: AsyncClient):
    response = await client.get("/api/v0/user/")
    print(client.base_url)
    assert response.status_code == 200
