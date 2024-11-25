from app.core.utils.unit_of_work import AbstractUnitOfWork
from app.database.schemas.team import TeamCreate, TeamUpdate
from fastapi import HTTPException, status


class TeamService:
    async def create_team(self, uow: AbstractUnitOfWork, team: TeamCreate):
        team_dict = team.model_dump(exclude_none=True)

        async with uow:
            team = await uow.team.add_one(team_dict)

            if not team:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка создания команды.",
                )

            return team

    async def get_teams(self, uow: AbstractUnitOfWork):
        async with uow:
            teams = await uow.team.find_all()

            return teams

    async def get_team_by_id(self, uow: AbstractUnitOfWork, team_id: int):
        team = await uow.team.find_one({"id": team_id})

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Команда #{team_id} не найдена.",
            )

        return team

    async def get_team_by_name(self, uow: AbstractUnitOfWork, team_name: str):
        team = await uow.team.find_one({"name": team_name})

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Команда {team_name} не найдена.",
            )

        return team

    async def update_team(
        self, uow: AbstractUnitOfWork, team: TeamUpdate, team_id: int
    ):
        await self.get_team_by_id(uow, team_id)

        team_dict = team.model_dump(exclude_none=True)

        async with uow:
            updated_team = await uow.team.update({"id": team_id}, team_dict)

            if not updated_team:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка обновления команды.",
                )

            return updated_team

    async def delete_team(self, uow: AbstractUnitOfWork, team_id: int):
        await self.get_team_by_id(uow, team_id)

        async with uow:
            deleted_team = await uow.team.delete({"id": team_id})

            if not deleted_team:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка удаления команды.",
                )

            return deleted_team

    async def add_member(self, uow: AbstractUnitOfWork, team_id: int, user_id: int):
        await self.get_team_by_id(uow, team_id)

        async with uow:
            user = await uow.user.find_one({"id": user_id})

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Пользователь #{user_id} не существует.",
                )

            exist = await uow.team_user.find_one(
                {"team_id": team_id, "user_id": user_id}
            )

            if exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Пользователь #{user_id} уже в команде.",
                )

            await uow.team_user.add_one({"team_id": team_id, "user_id": user_id})

    async def remove_member(self, uow: AbstractUnitOfWork, team_id: int, user_id: int):
        await self.get_team_by_id(uow, team_id)

        async with uow:
            exist = await uow.team_user.find_one(
                {"team_id": team_id, "user_id": user_id}
            )

            if not exist:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Пользователь #{user_id} не в команде.",
                )

            await uow.team_user.delete({"team_id": team_id, "user_id": user_id})

    async def get_team_members(self, uow: AbstractUnitOfWork, team_id: int):
        await self.get_team_by_id(uow, team_id)

        async with uow:
            members = await uow.team_user.find_all({"team_id": team_id})

            return [member["user_id"] for member in members]
