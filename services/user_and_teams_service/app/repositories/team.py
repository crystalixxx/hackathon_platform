from app.core.utils import SQLAlchemyRepository
from app.database.models.team import Team


class TeamRepository(SQLAlchemyRepository):
    model = Team
