from broker_utils.events import shutdown, startup
from broker_utils.middlewares import ExceptionErrorHandlerMiddleware
from taskiq import AsyncBroker, TaskiqEvents


def setup_events(broker: AsyncBroker):
    broker.add_event_handler(TaskiqEvents.WORKER_STARTUP, startup)
    broker.add_event_handler(TaskiqEvents.WORKER_SHUTDOWN, shutdown)


def setup_middlewares(broker: AsyncBroker):
    broker.with_middlewares(ExceptionErrorHandlerMiddleware())
