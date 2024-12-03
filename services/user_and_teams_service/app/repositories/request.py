from app.core.utils.repository import SQLAlchemyRepository
from app.database.models.request import Request


class RequestRepository(SQLAlchemyRepository):
    model = Request
