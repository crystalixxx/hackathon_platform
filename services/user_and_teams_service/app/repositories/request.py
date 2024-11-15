from app.database.models.request import Request
from app.core.repository import SQLAlchemyRepository


class RequestRepository(SQLAlchemyRepository):
    model = Request
