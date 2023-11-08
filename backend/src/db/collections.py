from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any
from bson.objectid import ObjectId


class PhoneCall(BaseModel):
    phone: str
    start_date: datetime
    end_date: datetime


class Task(BaseModel):
    task_id: str
    task_status: str
    recived: datetime = Field(default_factory=datetime.now)
    result: dict[str, Any] | None = None
