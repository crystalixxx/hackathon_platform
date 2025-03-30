from core.utils.repository import CachedRepository
from database.models.track import Track


class TrackRepository(CachedRepository):
    model = Track
