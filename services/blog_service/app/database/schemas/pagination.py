from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number, starting from 1")
    limit: int = Field(10, ge=1, le=100, description="Number of items per page")
    sort_by: Optional[str] = Field(None, description="Field to sort by")
    sort_order: Optional[str] = Field("asc", description="Sort order (asc or desc)")
    search: Optional[str] = Field(None, description="Search term")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    pages: int

    def __init__(self, **data):
        super().__init__(**data)
        self.pages = (self.total + self.limit - 1) // self.limit if self.limit > 0 else 0
