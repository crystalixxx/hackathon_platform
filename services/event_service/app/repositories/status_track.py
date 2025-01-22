from core.utils.repository import CachedRepository
from database.models.status_track import StatusTrack


class StatusTrackRepository(CachedRepository):
    model = StatusTrack
