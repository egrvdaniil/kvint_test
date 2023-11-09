from config import settings
from motor import motor_asyncio
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker  # type:ignore
from tasks import setup_tasks
from db.clients import TasksClient, PhoneCallsClient
import uuid


broker = AioPikaBroker(settings.RABBITMQ_URI).with_id_generator(lambda: str(uuid.uuid5))


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    db_client = motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_URI
    )
    state.db_client = db_client
    state.database = db_client.get_database(settings.DATABASE_NAME)
    state.tasks_client = TasksClient(database=state.database)
    state.calls_client = PhoneCallsClient(database=state.database)


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    state.db_client.close()


setup_tasks(broker)
