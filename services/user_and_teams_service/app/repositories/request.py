from app.core.repository import SQLAlchemyRepository
from app.database.models.request import Request


class RequestRepository(SQLAlchemyRepository):
    model = Request
