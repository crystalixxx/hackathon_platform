from app.core.redis_client import RedisClient
from app.core.utils.repository import SQLAlchemyRepository
from app.database.models.team import Team


class TeamRepository(SQLAlchemyRepository):
    model = Team

    def __init__(self):
        super().__init__()
        self.redis_client = RedisClient()

    # async def create_team(self, team_dict: dict):
    # team = await super().add_one(team_dict)
    # return team

    # async def get_teams(self):
    # teams = await super().find_all()
    # return teams

    async def get_team_by_id(self, team_id: int):
        cache_key = f"team:{team_id}"
        cached_team = self.redis_client.get(cache_key)

        if cached_team:
            return cached_team

        team = await super().find_one({"id": team_id})

        if team:
            self.redis_client.set(cache_key, team, expire=120)

        return team

    # async def get_team_by_name(self, team_name: str):
    # team = await super().find_one({"name": team_name})
    # return team

    async def update_team(self, team_id: int, update_dict: dict):
        team = await super().update({"id": team_id}, update_dict)

        if team:
            cache_key = f"team:{team_id}"
            self.redis_client.delete(cache_key)

        return team

    async def delete_team(self, team_id: int):
        team = await super().delete({"id": team_id})

        if team:
            cache_key = f"team:{team_id}"
            self.redis_client.delete(cache_key)

        return team
