from app.core.utils.repository import CachedRepository
from app.database.models.user import User


class UserRepository(CachedRepository):
    model = User
