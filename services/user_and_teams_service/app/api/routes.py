from fastapi import APIRouter, Depends
from app.services.service_client import ServiceClient

router = APIRouter()


def get_service_client() -> ServiceClient:
    return ServiceClient(base_url="http://service1:8000")


@router.get("/fetch-data")
async def fetch_data(client: ServiceClient = Depends(get_service_client)):
    data = await client.fetch_data("/api/data")
    return {"received_data": data}
