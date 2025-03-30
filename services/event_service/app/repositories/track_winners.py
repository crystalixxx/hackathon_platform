from core.utils.repository import CachedRepository
from database.models.track_winners import TrackWinner


class TrackWinnerRepository(CachedRepository):
    model = TrackWinner
