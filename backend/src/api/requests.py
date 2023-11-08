from pydantic import BaseModel


class ReportRequest(BaseModel):
    numbers: list[str]
