from core.utils.repository import CachedRepository
from database.models.request import Request


class RequestRepository(CachedRepository):
    model = Request
