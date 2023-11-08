from api import setup_endpoints  # type:ignore
from broker_init import broker
from config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.clients import TasksClient
from motor import motor_asyncio


async def startup(app):
    app.db_client = motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_URI
    )
    app.database = app.db_client.get_database(settings.DATABASE_NAME)  # type:ignore
    app.tasks_client = TasksClient(database=app.database)
    if not app.broker.is_worker_process:
        await app.broker.startup()


async def shutdown(app):
    app.db_client.close()
    if not broker.is_worker_process:
        await broker.shutdown()


def init_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.broker = broker

    app.add_event_handler("startup", startup(app))
    app.add_event_handler("shutdown", shutdown(app))

    setup_endpoints(app)
    return app
