from pydantic import BaseModel
from datetime import datetime
from typing import Any


class PhoneCall(BaseModel):
    phone: str
    start_date: datetime
    end_date: datetime
