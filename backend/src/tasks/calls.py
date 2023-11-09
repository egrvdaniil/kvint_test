import asyncio
from db.models import CallAggregationResult, CallAggregation, CallDurationCount


async def aggregate_calls(
    numbers: list[str],
    message_from: str | None = None,
    correlation_id: str | None = None,
):
    await asyncio.sleep(10)
    return {"result": "result"}
