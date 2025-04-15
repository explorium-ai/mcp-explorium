from typing import Optional

from pydantic import BaseModel, Field


class ResponseContext(BaseModel):
    correlation_id: str
    request_status: str
    time_took_in_seconds: float


class BasePaginatedResponse(BaseModel):
    response_context: ResponseContext
    total_results: int
    page: int
    total_pages: int


class RangeInt(BaseModel):
    gte: Optional[int] = Field(default=None, description="Greater than or equal to")
    lte: Optional[int] = Field(default=None, description="Less than or equal to")
