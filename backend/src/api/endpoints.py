from fastapi.requests import Request
from fastapi import HTTPException
from choices import TaskStatuses
from api.requests import ReportRequest
from api.responses import TaskStatusResponse, TaskStatusesListResponse, ReportResponse
from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask
from db.collections import Task
from db.clients import TasksClient
import uuid
import asyncio


async def create_report(request: Request, report_request: ReportRequest):
    task_name = 'tasks.calls:aggregate_calls'
    broker: AsyncBroker = request.app.broker
    aggregate_calls: AsyncTaskiqDecoratedTask | None = broker.find_task(task_name)
    if aggregate_calls is None:
        raise NotImplementedError("Task aggregate_calls does not exist")
    task = Task(
        task_name=task_name,
        task_id=str(uuid.uuid4()),
        task_status=TaskStatuses.PENDING,
    )
    tasks_client: TasksClient = request.app.tasks_client
    save_in_db_task = asyncio.create_task(
        tasks_client.save_or_update_task(
            task_id=task.task_id,
            task_data=task,
        ),
    )
    await aggregate_calls.kicker().with_task_id(task.task_id).kiq(
        numbers=report_request.numbers,
        message_from='client_api',
        correlation_id=report_request.correlation_id,
    )
    await save_in_db_task
    return TaskStatusResponse(
        status=task.task_status,
        task_id=task.task_id,
        task_name=task_name,
        recived=task.recived,
    )


async def get_all_tasks_statuses(request: Request):
    tasks_client: TasksClient = request.app.tasks_client
    statuses = await tasks_client.get_statuses()
    return TaskStatusesListResponse(statuses=statuses)


async def get_task_status(request: Request, task_id: str):
    tasks_client: TasksClient = request.app.tasks_client
    task = await tasks_client.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatusResponse(**task.model_dump())


async def get_report_task_result(request: Request, task_id):
    tasks_client: TasksClient = request.app.tasks_client
    task = await tasks_client.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.task_status != TaskStatuses.COMPLETED or task.result is None:
        raise HTTPException(status_code=400, detail="Result is not ready")
    return ReportResponse(**task.result)
