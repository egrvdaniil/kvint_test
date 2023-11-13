from config import settings
from db.clients import PhoneCallsClient, TasksClient
from motor import motor_asyncio
from taskiq import TaskiqState


async def startup(state: TaskiqState) -> None:
    db_client = motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_URI
    )
    state.db_client = db_client
    state.database = db_client.get_database(settings.DATABASE_NAME)
    state.tasks_client = TasksClient(database=state.database)
    state.calls_client = PhoneCallsClient(database=state.database)
    await state.calls_client.create_indexes()


async def shutdown(state: TaskiqState) -> None:
    state.db_client.close()
