from app.core.utils.repository import CachedRepository
from app.database.models.request import Request


class StatusTrackRepository(CachedRepository):
    model = Request
