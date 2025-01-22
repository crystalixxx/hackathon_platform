from core.utils.repository import CachedRepository
from database.models.location import Location


class LocationRepository(CachedRepository):
    model = Location
