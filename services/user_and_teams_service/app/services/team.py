from app.core.utils.unit_of_work import AbstractUnitOfWork
from app.database.schemas.team import TeamCreate, TeamUpdate


class TeamService:
    async def create_team(self, uow: AbstractUnitOfWork, team: TeamCreate):
        team_dict = team.model_dump(exclude_none=True)

        async with uow:
            team = await uow.team.add_one(team_dict)
            return team

    async def get_teams(self, uow: AbstractUnitOfWork):
        async with uow:
            teams = await uow.team.find_all()
            return teams

    async def get_team_by_id(self, uow: AbstractUnitOfWork, team_id: int):
        async with uow:
            team = await uow.team.find_one({"id": team_id})
            return team

    async def get_team_by_name(self, uow: AbstractUnitOfWork, team_name: str):
        async with uow:
            team = await uow.team.find_one({"name": team_name})
            return team

    async def update_team(
        self, uow: AbstractUnitOfWork, team: TeamUpdate, team_id: int
    ):
        old_team = self.get_team_by_id(uow, team_id)

        if old_team is None:
            return None

        team_dict = team.model_dump(exclude_none=True)

        async with uow:
            team = await uow.team.update({"id": team_id}, team_dict)
            return team

    async def delete_team(self, uow: AbstractUnitOfWork, team_id: int):
        team = self.get_team_by_id(uow, team_id)

        if team is None:
            return None

        async with uow:
            team = await uow.team.delete({"id": team_id})
            return team

    async def add_member(self, uow: AbstractUnitOfWork, team_id: int, user_id: int):
        async with uow:
            team = await uow.team.find_one({"id": team_id})

            if not team:
                raise ValueError()

            user = await uow.user.find_one({"id": user_id})

            if not user:
                raise ValueError()

            if user_id in team["members"]:
                raise ValueError()

            team["members"].append(user_id)
            await uow.team.update({"id": team_id}, {"members": team["members"]})

    async def remove_member(self, uow: AbstractUnitOfWork, team_id: int, user_id: int):
        async with uow:
            old_team = await uow.team.find_one({"id": team_id})

            if not old_team:
                raise ValueError()

            if user_id not in old_team.get("members"):
                raise ValueError()

            updated_team = [member for member in old_team["members"] if member != user_id]

            await uow.team.update({"id": team_id}, {"members": updated_team})

    async def get_members(self, uow: AbstractUnitOfWork, team_id: int):
        async with uow:
            team = await uow.team.find_one({"id": team_id})

            if not team:
                raise ValueError()

            return team.get("members")
