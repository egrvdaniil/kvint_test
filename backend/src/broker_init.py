from config import settings
from motor import motor_asyncio
from result_backend import TasksResultBackend
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker  # type:ignore
from tasks import setup_tasks

result_backend = TasksResultBackend(
    uri=settings.MONGO_URI, database_name=settings.DATABASE_NAME,
)

broker = AioPikaBroker().with_result_backend(result_backend)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    db_client = motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_URI
    )
    state.db_client = db_client
    state.database = db_client.get_database(settings.DATABASE_NAME)


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    # Here we close our pool on shutdown event.
    await state.redis.disconnect()
    state.db_client.close()


setup_tasks(broker)
