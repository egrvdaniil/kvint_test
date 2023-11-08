
from pymongo.results import UpdateResult

from db.collections import PhoneCall
from taskiq import TaskiqResult
from pydantic.generics import GenericModel


class BaseClient:
    collection_name: str | None = None

    def __init__(self, database) -> None:
        if not self.collection_name:
            raise NotImplementedError(f'Invalid collection name: {self.collection_name}')
        self.database = database
        self.collection = database.get_collection(self.collection_name)


class PhoneCallsClient(BaseClient):
    collection_name = 'phone_calls'


class TasksClient(BaseClient):
    collection_name = 'tasks'

    async def get_task_by_id(self, task_id: str) -> TaskiqResult | None:
        result = await self.collection.find_one(
            {'task_id': task_id},
        )
        if result is None:
            return None
        return TaskiqResult(**result)

    async def save_or_update_task(self, task: TaskiqResult, task_id: str) -> UpdateResult:
        return await self.collection.update_one(
            {'task_id': task_id},
            task.model_dump(),
            upsert=True,
        )
