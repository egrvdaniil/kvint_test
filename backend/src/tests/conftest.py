from datetime import datetime
from typing import Any

import pytest_asyncio
from api import setup_endpoints
from db.clients import PhoneCallsClient, TasksClient
from db.collections import Task
from fastapi import FastAPI
from fastapi.testclient import TestClient
from montydb import MontyClient, MontyCollection  # type:ignore
from taskiq import InMemoryBroker
from tasks import setup_tasks
from broker_utils import setup_middlewares


class MongoCursorMock:
    def __init__(self, iterable):
        self.iterable = iterable

    async def get_generator(self):
        for value in self.iterable:
            yield value


class MongoCollectionMock:
    def __init__(self, collection: MontyCollection):
        self.collection = collection

    def aggregate(self, aggregation: Any):
        aggregation_result = [
            {
                "_id": 'phone',
                "cnt_all_attempts": 100000,
                "sec_10": 9108,
                "sec_10_30": 16496,
                "sec_30": 74396,
                "min_price_att": 0,
                "max_price_att": 1200,
                "avg_dur_att": 599.6278,
                "sum_price_att_over_15": 58974760
            }
        ]
        cursor_mock = MongoCursorMock(aggregation_result)
        return cursor_mock.get_generator()

    async def find_one(self, filter: Any):
        return self.collection.find_one(filter)

    async def update_one(self, filter, update_query, upsert=True):
        return self.collection.update_one(
            filter,
            update_query,
            upsert=upsert
        )

    async def find(self, filter: Any):
        cursor = self.collection.find(filter)
        cursor_mock = MongoCursorMock(cursor)
        return cursor_mock.get_generator()


class MongoDBMock:
    def __init__(self, client: MontyClient):
        self.client = client
        self.db = self.client.get_database("test")

    def get_collection(self, name: str):
        return MongoCollectionMock(self.db.get_collection(name))

    def clear_db(self):
        self.client.drop_database("test")


@pytest_asyncio.fixture
def test_result():
    return {
        "correlation_id": "13242421424214",
        "status": "Complete",
        "task_received": "2023-05-09 02:27:03.049772",
        "from": "api",
        "to": "client",
        "data": [
            {
                "phone": 2,
                "cnt_all_attempts": 12675,
                "cnt_att_dur": {
                    "sec_10": 9108,
                    "sec_10_30": 16496,
                    "sec_30": 74396,
                },
                "min_price_att": 30,
                "max_price_att": 1500,
                "avg_dur_att": 46.7,
                "sum_price_att_over_15": 2765.59
            },
            {
                "phone": 6,
                "cnt_all_attempts": 46759,
                "cnt_att_dur": {
                    "sec_10": 9108,
                    "sec_10_30": 16496,
                    "sec_30": 74396,
                },
                "min_price_att": 27,
                "max_price_att": 2876,
                "avg_dur_att": 123.7,
                "sum_price_att_over_15": 4075.62
            }
        ],
        "total_duration": 0.67844633636
    }


@pytest_asyncio.fixture(scope="session")
def db_client():
    return MontyClient(":memory:")


@pytest_asyncio.fixture
def database(db_client):
    db_mock = MongoDBMock(db_client)
    yield db_mock
    db_mock.clear_db()


@pytest_asyncio.fixture
def tasks_collection(database):
    return database.get_collection("tasks").collection


@pytest_asyncio.fixture
def calls_collection(database):
    return database.get_collection("phone_calls").collection


@pytest_asyncio.fixture
def test_task(tasks_collection):
    task = Task(
        task_id="some_id",
        task_status="pending",
        task_name="tasks.calls:aggregate_calls",
    )
    tasks_collection.insert_one(task.model_dump())
    return task


@pytest_asyncio.fixture
def completed_task(tasks_collection, test_result):
    task = Task(
        task_id="some_id",
        task_status="completed",
        task_name="tasks.calls:aggregate_calls",
        received=datetime.now(),
        completed=datetime.now(),
        result=test_result,
    )
    tasks_collection.insert_one(task.model_dump())
    return task


@pytest_asyncio.fixture
def broker(database):
    broker = InMemoryBroker()
    broker.state.database = database
    broker.state.tasks_client = TasksClient(database=database)
    broker.state.calls_client = PhoneCallsClient(database=database)
    setup_middlewares(broker)
    setup_tasks(broker)
    return broker


@pytest_asyncio.fixture
async def api_client(database, broker):
    app = FastAPI()
    app.broker = broker
    app.database = database
    app.tasks_client = TasksClient(database=database)
    app.calls_client = PhoneCallsClient(database=database)
    setup_endpoints(app)
    return TestClient(app)


@pytest_asyncio.fixture(autouse=True)
async def calls(calls_collection):
    calls_collection.insert_many(
        [
            {
                "phone": 1,
                "start_date": 1684957028364,
                "end_date": 1684957130364,
            },
            {
                "phone": 2,
                "start_date": 1684957028364,
                "end_date": 1684957084364,
            },
            {
                "phone": 3,
                "start_date": 1684957028364,
                'end_date': 1684957084364,
            }
        ],
    )