import httpx
from fastapi import HTTPException


class ServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def fetch_data(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()

        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error connecting to {url}: {exc}")

        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=response.status_code, detail=f"Service error: {exc.response.text}")
