from core.utils.repository import CachedRepository
from database.models.status_event import StatusEvent


class StatusEventRepository(CachedRepository):
    model = StatusEvent
