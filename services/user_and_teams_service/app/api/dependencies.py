from typing import Annotated

from fastapi import Depends

from app.core.utils.unit_of_work import (
    AbstractUnitOfWork,
    CachedSQLAlchemyUnitOfWork,
)

UOWAlchemyDep = Annotated[AbstractUnitOfWork, Depends(CachedSQLAlchemyUnitOfWork)]
