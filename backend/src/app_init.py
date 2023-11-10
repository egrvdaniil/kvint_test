from api import setup_endpoints  # type:ignore
from broker_init import broker
from config import settings
from db.clients import TasksClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor import motor_asyncio


def startup_wrapper(app):
    async def startup():
        app.db_client = motor_asyncio.AsyncIOMotorClient(
            settings.MONGO_URI
        )
        app.database = app.db_client.get_database(settings.DATABASE_NAME)  # type:ignore
        app.tasks_client = TasksClient(database=app.database)
        if not app.broker.is_worker_process:
            await app.broker.startup()
    return startup


def shutdown_wrapper(app):
    async def shutdown():
        app.db_client.close()
        if not broker.is_worker_process:
            await broker.shutdown()
    return shutdown


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

    app.add_event_handler("startup", startup_wrapper(app))
    app.add_event_handler("shutdown", shutdown_wrapper(app))

    setup_endpoints(app)
    return app
