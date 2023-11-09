from pydantic import BaseModel
from typing import Any
from datetime import datetime
from db.models import CallAggregationResult


class ReportResponse(CallAggregationResult):
    pass


class TaskStatusResponse(BaseModel):
    task_status: str
    task_id: str
    task_name: str
    received: datetime
    completed: datetime | None = None


class TaskStatusesListResponse(BaseModel):
    statuses: list[TaskStatusResponse]
