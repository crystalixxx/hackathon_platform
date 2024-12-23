from core.utils.repository import CachedRepository
from database.models.team import Team


class TeamRepository(CachedRepository):
    model = Team
