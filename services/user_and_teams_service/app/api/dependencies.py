from typing import Annotated

from app.core.utils.unit_of_work import (
    AbstractUnitOfWork,
    CachedSQLAlchemyUnitOfWork,
)
from fastapi import Depends

UOWAlchemyDep = Annotated[AbstractUnitOfWork, Depends(CachedSQLAlchemyUnitOfWork)]
