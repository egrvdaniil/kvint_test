import asyncio
import time
from typing import Annotated

from choices import TaskStatuses
from db.clients import PhoneCallsClient, TasksClient
from db.collections import Task
from db.models import CallAggregationResult
from taskiq import Context, TaskiqDepends


async def aggregate_calls(
    numbers: list[int],
    context: Annotated[Context, TaskiqDepends()],
    message_from: str | None = None,
    correlation_id: str | None = None,
):
    start_time = time.time()
    task_id = context.message.task_id
    calls_client: PhoneCallsClient = context.state.calls_client
    tasks_client: TasksClient = context.state.tasks_client
    create_task = asyncio.create_task(
        _create_task_if_not_exists(
            task_id=task_id,
            task_name=context.message.task_name,
            tasks_client=tasks_client,
        ),
    )
    is_exists = await calls_client.check_numbers(numbers)
    received = await create_task
    if is_exists is False:
        raise Exception("Phones does not exists")
    tasks = []
    for number in numbers:
        tasks.append(
            asyncio.create_task(
                calls_client.aggregate_call(number=number),
            ),
        )
    tasks_results = await asyncio.gather(*tasks)
    result = CallAggregationResult(
        data=tasks_results,
        total_duration=time.time() - start_time,
        task_from=message_from,
        task_to='client',
        correlation_id=correlation_id,
        received=received,
    )
    await tasks_client.save_results(task_id, result)


async def _create_task_if_not_exists(
    task_id: str,
    task_name: str,
    tasks_client: TasksClient,
):
    current_task = await tasks_client.get_task_by_id(task_id)
    if current_task is None:
        current_task = Task(
            task_name=task_name,
            task_id=task_id,
            task_status=TaskStatuses.PENDING,
        )
        await tasks_client.save_or_update_task(
            task_id=task_id,
            task_data=current_task,
        )
    await tasks_client.set_in_work(task_id)
    return current_task.received
