from app.database.models.team import Team
from app.core.repository import SQLAlchemyRepository


class TeamRepository(SQLAlchemyRepository):
    model = Team
