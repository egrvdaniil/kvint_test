from broker_init import broker
import asyncio


@broker.task
async def aggregate_calls():
    await asyncio.sleep(10)
    return {'result': 'result'}
