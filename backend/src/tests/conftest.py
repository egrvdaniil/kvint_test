from fastapi.testclient import TestClient
from fastapi import FastAPI
from api import setup_endpoints
import pytest_asyncio


@pytest_asyncio.fixture
def database():
    pass


@pytest_asyncio.fixture
async def api_client(database):
    app = FastAPI()
    setup_endpoints(app)
    return TestClient(app)
