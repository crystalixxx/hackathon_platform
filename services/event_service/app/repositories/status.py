from app.core.utils.repository import CachedRepository
from app.database.models.request import Request


class StatusRepository(CachedRepository):
    model = Request
