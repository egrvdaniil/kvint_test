from api import setup_endpoints  # type:ignore
from broker_init import broker, result_backend
from config import settings
from database_init import database, db_client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


async def startup(app):
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

    app.db_client = db_client
    app.broker = broker
    app.result_backend = result_backend

    app.add_event_handler("startup", startup(app))
    app.add_event_handler("shutdown", shutdown(app))

    setup_endpoints(app)
    return app
