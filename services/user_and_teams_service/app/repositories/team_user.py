from core.utils.repository import CachedRepository
from database.models.team import TeamUser


class TeamUserRepository(CachedRepository):
    model = TeamUser
