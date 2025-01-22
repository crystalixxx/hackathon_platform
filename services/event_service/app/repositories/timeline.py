from core.utils.repository import CachedRepository
from database.models.timeline import Timeline


class TimelineRepository(CachedRepository):
    model = Timeline
