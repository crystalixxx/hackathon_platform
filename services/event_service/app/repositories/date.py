from core.utils.repository import CachedRepository
from database.models.date import Date


class DateRepository(CachedRepository):
    model = Date
