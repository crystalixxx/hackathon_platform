from app.core.utils.repository import CachedRepository
from app.database.models.user import UserTag


class UserTagRepository(CachedRepository):
    model = UserTag
