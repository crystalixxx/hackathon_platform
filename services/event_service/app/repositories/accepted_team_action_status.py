from core.utils.repository import CachedRepository
from database.models.accepted_team_action_status import AcceptedTeamActionStatus


class AcceptedTeamActionStatusRepository(CachedRepository):
    model = AcceptedTeamActionStatus
