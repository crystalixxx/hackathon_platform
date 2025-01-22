from core.utils.repository import CachedRepository
from database.models.track_team import TrackTeam


class TrackTeamRepository(CachedRepository):
    model = TrackTeam
