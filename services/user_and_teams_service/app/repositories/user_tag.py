from app.core.utils.repository import SQLAlchemyRepository
from app.database.models.user import UserTag


class UserTagRepository(SQLAlchemyRepository):
    model = UserTag
