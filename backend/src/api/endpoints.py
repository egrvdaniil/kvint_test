from fastapi.requests import Request
from choices import TaskStatuses
from api.requests import ReportRequest
from api.responses import TaskStatus
from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask
from db.collections import Task
from db.clients import TasksClient
import uuid


async def create_report(request: Request, report_request: ReportRequest):
    broker: AsyncBroker = request.app.broker
    aggregate_calls: AsyncTaskiqDecoratedTask | None = broker.find_task('aggregate_calls')
    if aggregate_calls is None:
        raise NotImplementedError("Task aggregate_calls does not exist")
    task = Task(
        task_id=str(uuid.uuid5),
        task_status=TaskStatuses.PENDING,
    )
    tasks_client: TasksClient = request.app.tasks_client
    await tasks_client.save_or_update_task(
        task_id=task.task_id,
        task_data=task,
    )
    await aggregate_calls.kicker().with_task_id(task.task_id).kiq(
        numbers=report_request.numbers,
        message_from='client_api',
        correlation_id=report_request.correlation_id,
    )
    return TaskStatus(
        status=task.task_status,
        task_id=task.task_id,
    )
