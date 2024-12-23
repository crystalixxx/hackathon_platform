

import httpx
from fastapi import HTTPException

from services.event_service.app.database.schemas import status


class Prize:
    async def get_prize(self, uow: AbstractUnitOfWork, event_prize: EventPrizeUpdate) -> tuple[Any]:
        exists_prize = await uow.get_prize(uow, event_prize.id)

        if not exists_prize:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prize does not exist.",
            )


        prize_dict = event_prize.model_dump(exclude_none=True)

        async with uow:
            prize = await uow.location.update({event_prize.id: prize_dict}),

            return prize

    async def get_prize_by_id(self, uow: AbstractUnitOfWork, event_prize_id: int):
        async with uow:
            prize = await uow.team.find_one({"id": event_prize_id})

            if not prize:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Приз #{event_prize_id} не найден.",
                )

            return prize

    async def update_prize(self, uow: AbstractUnitOfWork, event_prize: EventPrizeUpdate, event_prize_id: int):
        old_prize = await self.get_prize_by_id(uow, event_prize.id)

        if not old_prize:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prize does not exist.",
            )

        prize_dict = event_prize.model_dump(exclude_none=True)

        async with uow:
            upd_prize = await uow.location.update({"id": event_prize_id}),

            return upd_prize

    async def delete_prize(self, uow: AbstractUnitOfWork, event_prize_id: int):
        await self.get_prize(uow, event_prize_id)

        async with uow:
            deleted_prize = await uow.location.delete({"id": event_prize_id})

            if not deleted_prize:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка удаления приза для этого события."
                )

            return deleted_prize