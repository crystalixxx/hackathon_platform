from core.utils.repository import CachedRepository
from database.models.event_prize import EventPrize


class EventPrizeRepository(CachedRepository):
    model = EventPrize
