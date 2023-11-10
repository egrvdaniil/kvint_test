from pydantic import BaseModel, Field
from datetime import datetime


class CallDurationCount(BaseModel):
    sec_10: int = Field(alias='10_sec')
    sec_10_30: int = Field(alias='10_30_sec')
    sec_30: int = Field(alias='30_sec')


class CallAggregation(BaseModel):
    phone: int
    cnt_all_attempts: int
    cnt_att_dur: CallDurationCount
    min_price_att: int
    max_price_att: int
    avg_dur_att: float
    sum_price_att_over_15: float


class CallAggregationResult(BaseModel):
    data: list[CallAggregation]
    total_duration: float
    received: datetime | None = None
    task_from: str | None = None
    task_to: str | None = None
    correlation_id: str | None = None
