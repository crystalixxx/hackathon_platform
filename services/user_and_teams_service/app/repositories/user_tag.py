from app.database.models.user import UserTag
from app.core.utils.repository import SQLAlchemyRepository


class UserTagRepository(SQLAlchemyRepository):
    model = UserTag
