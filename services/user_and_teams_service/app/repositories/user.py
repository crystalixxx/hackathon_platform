from app.database.models.user import User
from app.core.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
