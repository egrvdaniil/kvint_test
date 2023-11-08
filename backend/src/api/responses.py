from pydantic import BaseModel


class CallDurationCount(BaseModel):
    sec_10: int
    sec_10_30: int
    sec_30: int


class CallAggregation(BaseModel):
    phone: str
    cnt_all_attempts: int
    cnt_att_dur: CallDurationCount
    min_price_att: int
    max_price_att: int
    avg_dur_att: float
    sum_price_att_over_15: float


class ReportResponse(BaseModel):
    data: list[CallAggregation]
    total_duration: float


class TaskStatusResponse(BaseModel):
    status: str
    task_id: str
    response: ReportResponse | None = None


class TaskStatusesListResponse(BaseModel):
    statuses: list[TaskStatusResponse]
