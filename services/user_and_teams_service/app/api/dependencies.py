from typing import Annotated

from core.utils.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from fastapi import Depends

UOWAlchemyDep = Annotated[AbstractUnitOfWork, Depends(SqlAlchemyUnitOfWork)]
