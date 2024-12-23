from core.utils.repository import CachedRepository
from database.models.user import User


class UserRepository(CachedRepository):
    model = User
