from app.core.utils.repository import SQLAlchemyRepository
from app.database.models.team import TeamUser


class TeamUserRepository(SQLAlchemyRepository):
    model = TeamUser
