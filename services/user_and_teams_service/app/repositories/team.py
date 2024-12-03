from app.core.utils.repository import SQLAlchemyRepository
from app.database.models.team import Team


class TeamRepository(SQLAlchemyRepository):
    model = Team
