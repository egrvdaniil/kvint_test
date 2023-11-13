import uuid

from config import settings
from taskiq_aio_pika import AioPikaBroker  # type:ignore
from tasks import setup_tasks
from typing import Any
from broker_utils import setup_events, setup_middlewares



broker = AioPikaBroker(settings.RABBITMQ_URI).with_id_generator(lambda: str(uuid.uuid5))

setup_middlewares(broker)
setup_events(broker)
setup_tasks(broker)
