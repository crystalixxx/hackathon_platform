from app.core.utils.repository import CachedRepository
from app.database.models.team import TeamUser


class TeamUserRepository(CachedRepository):
    model = TeamUser
