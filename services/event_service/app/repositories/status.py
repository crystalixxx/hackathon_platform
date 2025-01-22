from core.utils.repository import CachedRepository
from database.models.status import Status


class StatusRepository(CachedRepository):
    model = Status
