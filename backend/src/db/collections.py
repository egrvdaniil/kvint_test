from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PhoneCall(BaseModel):
    phone: int
    start_date: datetime
    end_date: datetime


class Task(BaseModel):
    task_id: str
    task_status: str
    task_name: str
    received: datetime = Field(default_factory=datetime.now)
    completed: datetime | None = None
    result: Any | None = None
