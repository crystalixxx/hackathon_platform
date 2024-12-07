from app.core.utils.repository import CachedRepository
from app.database.models.team import Team


class TeamRepository(CachedRepository):
    model = Team
