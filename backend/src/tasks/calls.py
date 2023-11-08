from broker_init import broker
import asyncio


async def aggregate_calls():
    await asyncio.sleep(10)
    return {'result': 'result'}
