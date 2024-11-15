from app.database.schemas.team import TeamCreate, TeamUpdate
from app.core.utils.unit_of_work import AbstractUnitOfWork


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

    async def update_team(self, uow: AbstractUnitOfWork, team: TeamUpdate, team_id: int):
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
