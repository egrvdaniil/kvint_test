from fastapi.requests import Request
from choices import TaskStatuses
from api.requests import ReportRequest
from api.responses import TaskStatus
from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask


async def create_report(request: Request, report_request: ReportRequest):
    broker: AsyncBroker = request.app.broker
    aggregate_calls: AsyncTaskiqDecoratedTask | None = broker.find_task('aggregate_calls')
    if aggregate_calls is None:
        raise NotImplementedError("Task aggregate_calls does not exist")
    task = await aggregate_calls.kiq(report_request.numbers)
    return TaskStatus(
        status=TaskStatuses.IN_WORK,
        task_id=task.task_id,
    )
