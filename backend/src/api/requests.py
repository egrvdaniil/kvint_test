from pydantic import BaseModel


class ReportRequest(BaseModel):
    numbers: list[int]
    correlation_id: str
