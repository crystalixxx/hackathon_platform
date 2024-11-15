from app.database.schemas.request import RequestCreate
from app.core.utils.unit_of_work import AbstractUnitOfWork


class RequestService:
    async def create_request(self, uow: AbstractUnitOfWork, request: RequestCreate):
        request_data = request.model_dump(exclude_none=True)

        async with uow:
            request = uow.request.add_one(request_data)
            return request

    async def get_request_by_id(self, uow: AbstractUnitOfWork, request_id: int):
        async with uow:
            request = uow.request.find_one({"id": request_id})
            return request

    async def get_requests_of_user(self, uow: AbstractUnitOfWork, user_id: int):
        async with uow:
            request = uow.request.find_one({"user_id": user_id})
            return request

    async def get_request_of_team(self, uow: AbstractUnitOfWork, team_id: int):
        async with uow:
            request = uow.request.find_one({"team_id": team_id})
            return request

    async def delete_request(self, uow: AbstractUnitOfWork, request_id):
        request = self.get_request_by_id(uow, request_id)

        if request is None:
            return None

        async with uow:
            request = uow.request.delete({"id": request_id})
            return request
