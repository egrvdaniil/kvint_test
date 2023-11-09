import asyncio
from db.models import CallAggregationResult, CallAggregation, CallDurationCount
from typing import Annotated, Optional
from taskiq import Context, TaskiqDepends, TaskiqEvents, TaskiqState
from db.clients import PhoneCallsClient, TasksClient
import time


async def aggregate_calls(
    numbers: list[str],
    context: Annotated[Context, TaskiqDepends()],
    message_from: str | None = None,
    correlation_id: str | None = None,
):
    start_time = time.time()
    task_id = context.message.task_id
    calls_client: PhoneCallsClient = context.state.calls_client
    tasks_client: TasksClient = context.state.tasks_client
    await tasks_client.set_in_work(task_id)
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
    )
    await tasks_client.save_results(task_id, result)
