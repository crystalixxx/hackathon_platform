from core.utils.repository import CachedRepository
from database.models.event_location import EventLocation


class EventLocationRepository(CachedRepository):
    model = EventLocation
