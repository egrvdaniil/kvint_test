
from pymongo.results import UpdateResult

from db.collections import Task
from db.models import CallDurationCount, CallAggregation
import asyncio
from pydantic import BaseModel
from datetime import datetime
from choices import TaskStatuses


class BaseClient:
    collection_name: str | None = None

    def __init__(self, database) -> None:
        if not self.collection_name:
            raise NotImplementedError(f'Invalid collection name: {self.collection_name}')
        self.database = database
        self.collection = database.get_collection(self.collection_name)


class PhoneCallsClient(BaseClient):
    collection_name = "phone_calls"

    async def aggregate_call(self, number: str):
        await asyncio.sleep(10)
        call_duration_count = CallDurationCount(
            sec_10=1,
            sec_10_30=2,
            sec_30=3,
        )
        return CallAggregation(
            phone=number,
            cnt_all_attempts=4,
            cnt_att_dur=call_duration_count,
            min_price_att=5,
            max_price_att=6,
            avg_dur_att=7.0,
            sum_price_att_over_15=8.0
        )


class TasksClient(BaseClient):
    collection_name = "tasks"

    async def get_task_by_id(self, task_id: str) -> Task | None:
        result = await self.collection.find_one(
            {"task_id": task_id},
        )
        if result is None:
            return None
        return Task(**result)

    async def save_or_update_task(self, task_data: Task, task_id: str, upsert: bool = True) -> UpdateResult:
        return await self.collection.update_one(
            {"task_id": task_id},
            {"$set": task_data.model_dump()},
            upsert=upsert,
        )

    async def get_statuses(self):
        cursor = self.collection.find({})
        return [status async for status in cursor]

    async def save_results(self, task_id: str, results: BaseModel):
        return await self.collection.update_one(
            {"task_id": task_id},
            {
                "$set": {
                    "task_status": TaskStatuses.COMPLETED,
                    "completed": datetime.now(),
                    "result": results.model_dump(),
                },
            },
        )

    async def set_in_work(self, task_id: str):
        return await self.collection.update_one(
            {"task_id": task_id},
            {
                "$set": {
                    "task_status": TaskStatuses.IN_WORK,
                },
            },
        )
