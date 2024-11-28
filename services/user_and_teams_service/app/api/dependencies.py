from typing import Annotated

from fastapi import Depends

from app.core.utils.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork

UOWAlchemyDep = Annotated[AbstractUnitOfWork, Depends(SqlAlchemyUnitOfWork)]
