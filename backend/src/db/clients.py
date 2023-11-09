
from pymongo.results import UpdateResult

from db.collections import Task


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

    async def get_task_by_id(self, task_id: str) -> Task | None:
        result = await self.collection.find_one(
            {'task_id': task_id},
        )
        if result is None:
            return None
        return Task(**result)

    async def save_or_update_task(self, task_data: Task, task_id: str, upsert: bool = True) -> UpdateResult:
        return await self.collection.update_one(
            {'task_id': task_id},
            {"$set": task_data.model_dump()},
            upsert=upsert,
        )

    async def get_statuses(self):
        cursor = self.collection.find({})
        return [status async for status in cursor]
