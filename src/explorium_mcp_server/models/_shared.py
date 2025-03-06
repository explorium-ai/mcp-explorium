from pydantic import BaseModel


class ResponseContext(BaseModel):
    correlation_id: str
    request_status: str
    time_took_in_seconds: float


class BasePaginatedResponse(BaseModel):
    response_context: ResponseContext
    total_results: int
    page: int
    total_pages: int
