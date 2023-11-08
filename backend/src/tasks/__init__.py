from taskiq import AsyncBroker
from tasks.calls import aggregate_calls


def setup_tasks(broker: AsyncBroker):
    broker.task(aggregate_calls)
