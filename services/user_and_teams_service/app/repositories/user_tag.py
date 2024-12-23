from core.utils.repository import CachedRepository
from database.models.user import UserTag


class UserTagRepository(CachedRepository):
    model = UserTag
