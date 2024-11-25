from app.core.utils import SQLAlchemyRepository
from app.database.models.request import Request


class RequestRepository(SQLAlchemyRepository):
    model = Request
