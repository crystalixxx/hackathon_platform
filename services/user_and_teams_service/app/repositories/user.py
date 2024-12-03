from app.core.utils.repository import SQLAlchemyRepository
from app.database.models.user import User


class UserRepository(SQLAlchemyRepository):
    model = User
