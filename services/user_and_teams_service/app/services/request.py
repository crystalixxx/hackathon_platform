from app.core.utils.unit_of_work import AbstractUnitOfWork
from app.database.schemas.request import RequestCreate
from fastapi import HTTPException, status


class RequestService:
    async def create_request(self, uow: AbstractUnitOfWork, request: RequestCreate):
        request_data = request.model_dump(exclude_none=True)

        async with uow:
            request = await uow.request.add_one(request_data)
            return request

    async def get_request_by_id(self, uow: AbstractUnitOfWork, request_id: int):
        async with uow:
            request = await uow.request.find_one({"id": request_id})
            return request

    async def get_requests_of_user(self, uow: AbstractUnitOfWork, user_id: int):
        async with uow:
            request = await uow.request.find_some({"user_id": user_id})
            return request

    async def get_requests_of_team(self, uow: AbstractUnitOfWork, team_id: int):
        async with uow:
            request = await uow.request.find_some({"request_team_id": team_id})
            return request

    async def get_requests_sent_by_team(self, uow: AbstractUnitOfWork, team_id: int):
        async with uow:
            requests = await uow.request.find_some(
                {"request_team_id": team_id, "sent_by_team": True}
            )
            return requests

    async def get_requests_to_team(self, uow: AbstractUnitOfWork, team_id: int):
        async with uow:
            requests = await uow.request.find_some(
                {"request_team_id": team_id, "sent_by_team": False}
            )
            return requests

    async def delete_request(self, uow: AbstractUnitOfWork, request_id):
        await self.get_request_by_id(uow, request_id)

        async with uow:
            request = await uow.request.delete({"id": request_id})
            return request

    async def approve_request(self, uow: AbstractUnitOfWork, request_id: int):
        async with uow:
            request = await self.get_request_by_id(uow, request_id)

            if not request:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Реквест #{request_id} не найден.",
                )

            updated_request = await uow.request.update(
                {"id": request_id}, {"is_ok": True}
            )
            return updated_request

    async def reject_request(self, uow: AbstractUnitOfWork, request_id: int):
        async with uow:
            request = await self.get_request_by_id(uow, request_id)

            if not request:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Реквест #{request_id} не найден.",
                )

            return await uow.request.delete({"id": request_id})
