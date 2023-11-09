import asyncio
from db.models import CallAggregationResult, CallAggregation, CallDurationCount
from typing import Annotated, Optional
from taskiq import Context, TaskiqDepends, TaskiqEvents, TaskiqState
from db.clients import PhoneCallsClient, TasksClient
from db.collections import Task
import time
from datetime import datetime
from choices import TaskStatuses


async def aggregate_calls(
    numbers: list[str],
    context: Annotated[Context, TaskiqDepends()],
    message_from: str | None = None,
    correlation_id: str | None = None,
    received: datetime | None = None,
):
    start_time = time.time()
    task_id = context.message.task_id
    calls_client: PhoneCallsClient = context.state.calls_client
    tasks_client: TasksClient = context.state.tasks_client
    create_or_update_task = asyncio.create_task(
        _create_task_if_not_exists(
            task_id=task_id,
            task_name=context.message.task_name,
            tasks_client=tasks_client,
        ),
    )
    tasks = [create_or_update_task]
    for number in numbers:
        tasks.append(
            asyncio.create_task(
                calls_client.aggregate_call(number=number),
            ),
        )
    tasks_results = await asyncio.gather(*tasks)
    result = CallAggregationResult(
        data=tasks_results[1:],
        total_duration=time.time() - start_time,
        task_from=message_from,
        task_to='client',
        correlation_id=correlation_id,
        received=received,
    )
    await tasks_client.save_results(task_id, result)


async def _create_task_if_not_exists(task_id: str, task_name: str, tasks_client: TasksClient):
    current_task = await tasks_client.get_task_by_id(task_id)
    if current_task is None:
        await tasks_client.save_or_update_task(
            task_id=task_id,
            task_data=Task(
                task_name=task_name,
                task_id=task_id,
                task_status=TaskStatuses.PENDING,
            )
        )
    await tasks_client.set_in_work(task_id)
