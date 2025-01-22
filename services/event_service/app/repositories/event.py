from core.utils.repository import CachedRepository
from database.models.event import Event


class EventRepository(CachedRepository):
    model = Event
