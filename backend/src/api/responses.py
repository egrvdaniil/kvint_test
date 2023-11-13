from datetime import datetime

from db.models import CallAggregationResult
from pydantic import BaseModel


class ReportResponse(CallAggregationResult):
    pass


class TaskStatusResponse(BaseModel):
    task_status: str
    task_id: str
    task_name: str
    received: datetime
    completed: datetime | None = None
    error_message: str | None = None


class TaskStatusesListResponse(BaseModel):
    statuses: list[TaskStatusResponse]
