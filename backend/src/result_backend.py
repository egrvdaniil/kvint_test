from typing import Any

from taskiq import TaskiqResult
from taskiq.abc.result_backend import AsyncResultBackend
from db.clients import TasksClient
from motor import motor_asyncio
from motor.core import AgnosticClient


class TasksResultBackend(AsyncResultBackend):
    def __init__(self, uri: str, database_name: str) -> None:
        super().__init__()
        self.uri = uri
        self.database_name = database_name
        self.db_client: AgnosticClient | None = None
        self.tasks_client: TasksClient | None = None

    async def startup(self) -> None:
        self.db_client = motor_asyncio.AsyncIOMotorClient(self.uri)
        self.tasks_client = TasksClient(
            database=self.db_client.get_database(self.database_name),
        )

    async def shutdown(self) -> None:
        if self.db_client:
            self.db_client.close()

    async def set_result(
        self,
        task_id: str,
        result: TaskiqResult,
    ) -> None:
        if not self.tasks_client:
            raise Exception('Backend is not started')
        await self.tasks_client.save_or_update_task(
            task=result,
            task_id=task_id,
        )

    async def get_result(
        self,
        task_id: str,
        with_logs: bool = False,
    ) -> TaskiqResult:
        if not self.tasks_client:
            raise Exception('Backend is not started')
        result = await self.tasks_client.get_task_by_id(
            task_id=task_id,
        )
        if result is None:
            raise ValueError('Task does not exist')
        return result

    async def is_result_ready(
        self,
        task_id: str,
    ) -> bool:
        if not self.tasks_client:
            raise Exception('Backend is not started')
        result = await self.tasks_client.get_task_by_id(
            task_id=task_id,
        )
        if result:
            return True
        return False
