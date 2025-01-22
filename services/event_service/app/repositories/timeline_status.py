from core.utils.repository import CachedRepository
from database.models.timeline_status import TimelineStatus


class TimelineStatusRepository(CachedRepository):
    model = TimelineStatus
