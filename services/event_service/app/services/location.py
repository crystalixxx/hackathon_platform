from typing import Tuple, Any

from fastapi import HTTPException
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND

from services.event_service.app.database.models import location
from services.event_service.app.database.models.location import Location

from app.database.schemas.location import LocationCreate, LocationUpdate

from services.user_and_teams_service.app.core.utils import AbstractUnitOfWork


class Location:
    async def get_location(self, uow: AbstractUnitOfWork, location: LocationCreate) -> tuple[Any]:
        exists_location = await self.get_location(uow, location.id)

        if not exists_location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Location does not exist.",
            )

        location_dict = location.model_dump(exclude_none=True)

        async with uow:
            location = await uow.location.update({location.id: location_dict}),

            return location

    async def get_location_by_id(self, uow: AbstractUnitOfWork, location_id: int):
        async with uow:
            location = await uow.team.find_one({"id": location_id})

            if not location:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Локация #{location_id} не найдена.",
                )

            return location

    async def update_location(self, uow: AbstractUnitOfWork, location: LocationUpdate, location_id: int):
        old_location = await self.get_location_by_id(uow, location.id)

        if not old_location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Location does not exist.",
            )

        location_dict = location.model_dump(exclude_none=True)

        async with uow:
            upd_location = await uow.location.update({"id": location_id}),

            return upd_location

    async def delete_location(self, uow: AbstractUnitOfWork, location_id: int):
        await self.get_location(uow, location_id)

        async with uow:
            deleted_location = await uow.location.delete({"id": location_id})

            if not deleted_location:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка удаления локации проведения."
                )

            return deleted_location

    async def change_location(self, uow: AbstractUnitOfWork, location: LocationUpdate, location_id: int):
        location = await self.get_location_by_id(uow, location_id)
        location_dict = location.model_dump(exclude_none=True)

        change_location: LocationUpdate = LocationUpdate()

        return await self.update_location(uow, change_location, location_id)

