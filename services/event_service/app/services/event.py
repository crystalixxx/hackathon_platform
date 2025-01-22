from api.dependencies import AbstractUnitOfWork
from database.schemas.event import EventCreate, EventSchema, EventUpdate
from fastapi import HTTPException
from starlette import status


class EventService:
    async def get_event_by_id(
        self, uow: AbstractUnitOfWork, event_id: int
    ) -> EventSchema | None:
        async with uow as session:
            event = await session.events.find_one({"id": event_id})
            return event

    async def get_event_by_title(
        self, uow: AbstractUnitOfWork, event_title: str
    ) -> EventSchema | None:
        async with uow as session:
            event = await session.events.find_one({"title": event_title})
            return event

    async def create_service(self, uow: AbstractUnitOfWork, event: EventCreate) -> int:
        event_dict = event.model_dump(exclude_none=True)

        async with uow as session:
            event_id = await session.events.add_one(event_dict)
            return event_id

    async def update_service(
        self, uow: AbstractUnitOfWork, event: EventUpdate, event_id: int
    ) -> EventSchema:
        old_event = await self.get_event_by_id(uow, event_id)

        if old_event is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        event_dict = event.model_dump(exclude_none=True)

        async with uow as session:
            event = await session.events.update({"id": event_id}, event_dict)
            return event

    async def delete_event(self, uow: AbstractUnitOfWork, event_id: int) -> EventSchema:
        existing_event = await self.get_event_by_id(uow, event_id)

        if existing_event is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        async with uow as session:
            event = await session.events.remove({"id": event_id})
            return event
