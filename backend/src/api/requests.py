from pydantic import BaseModel


class ReportRequest(BaseModel):
    numbers: list[str]
    correlation_id: str
