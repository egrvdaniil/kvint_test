from config import settings
from result_backend import TasksResultBackend
from taskiq_aio_pika import AioPikaBroker  # type:ignore
from database_init import database  # type:ignore


result_backend = TasksResultBackend(
    uri=settings.MONGO_URI, database_name=settings.DATABASE_NAME,
)

broker = AioPikaBroker().with_result_backend(result_backend)
