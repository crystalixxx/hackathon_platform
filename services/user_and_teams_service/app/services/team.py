from core.utils.unit_of_work import AbstractUnitOfWork
from database.schemas.team import TeamCreate, TeamUpdate
from fastapi import HTTPException, status

from services.user import UserService


class TeamService:
    async def create_team(self, uow: AbstractUnitOfWork, team: TeamCreate):
        team_dict = team.model_dump(exclude_none=True)

        async with uow:
            new_team = await uow.team.add_one(team_dict)

        async with uow:
            await self.add_member(uow, new_team, team.captain_id)

            return new_team

    async def get_teams(self, uow: AbstractUnitOfWork):
        async with uow:
            teams = await uow.team.find_all()

            return teams

    async def get_team_by_id(self, uow: AbstractUnitOfWork, team_id: int):
        async with uow:
            team = await uow.team.find_one({"id": team_id})

            if not team:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Команда #{team_id} не найдена.",
                )

            return team

    async def get_team_by_name(self, uow: AbstractUnitOfWork, team_name: str):
        async with uow:
            team = await uow.team.find_one({"title": team_name})

            if not team:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Команда {team_name} не найдена.",
                )

            return team

    async def get_teams_by_captain_id(
        self, uow: AbstractUnitOfWork, team_captain_id: int
    ):
        async with uow:
            teams = await uow.team.find_some({"captain_id": team_captain_id})

            return teams

    async def update_team(
        self, uow: AbstractUnitOfWork, team: TeamUpdate, team_id: int
    ):
        old_team = await self.get_team_by_id(uow, team_id)

        if not old_team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Command does not exist.",
            )

        team_dict = team.model_dump(exclude_unset=True)

        async with uow:
            updated_team = await uow.team.update({"id": team_id}, team_dict)

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

    async def is_member_of_team(self, uow: AbstractUnitOfWork, team_id: int, user_id):
        await self.get_team_by_id(uow, team_id)

        async with uow:
            exist = await uow.team_user.find_one(
                {"team_id": team_id, "user_id": user_id}
            )
            return bool(exist)

    async def change_captain(self, uow: AbstractUnitOfWork, team_id: int, user_id: int):
        team = await self.get_team_by_id(uow, team_id)
        team_dict = team.model_dump(exclude_none=True)

        team_members = await self.get_team_members(uow, team_id)

        if user_id not in [user.id for user in team_members]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't consist in team",
            )

        change_team: TeamUpdate = TeamUpdate()
        for team_attribute, attribute_value in team_dict.items():
            setattr(change_team, team_attribute, attribute_value)
        change_team.captain_id = user_id

        return await self.update_team(uow, change_team, team_id)

    async def add_member(self, uow: AbstractUnitOfWork, team_id: int, user_id: int):
        existing_team = await self.get_team_by_id(uow, team_id)

        if existing_team is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Command does not exist.",
            )

        if await self.is_member_of_team(uow, team_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь #{user_id} не существует.",
            )

        async with uow:
            user = await uow.users.find_one({"id": user_id})

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Пользователь #{user_id} не существует.",
                )

            return await uow.team_user.add_one(
                {"team_id": team_id, "user_id": user_id, "role_name": "Test"}
            )

    async def remove_member(self, uow: AbstractUnitOfWork, team_id: int, user_id: int):
        team = await self.get_team_by_id(uow, team_id)

        if not await self.is_member_of_team(uow, team_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь #{user_id} не в команде.",
            )

        if team.captain_id == user_id:
            team_members = await self.get_team_members(uow, team_id)

            if len(team_members) > 1:
                for user in team_members:
                    if user.id != user_id:
                        await self.change_captain(uow, team_id, user.id)
                        break
            else:
                await self.delete_team(uow, team_id)
                return

        async with uow:
            return await uow.team_user.delete({"team_id": team_id, "user_id": user_id})

    async def get_team_members(self, uow: AbstractUnitOfWork, team_id: int):
        await self.get_team_by_id(uow, team_id)

        async with uow:
            return await uow.team_user.find_some({"team_id": team_id})

    async def get_team_tags(self, uow: AbstractUnitOfWork, team_id: int):
        await self.get_team_by_id(uow, team_id)

        async with uow:
            team_users = await self.get_team_members(uow, team_id)
            team_tags = []

            for user in team_users:
                tags = await UserService().get_user_tags(uow, user.user_id)

                for tag in tags:
                    team_tags.append(tag)

        return team_tags
