
from datetime import datetime

from choices import TaskStatuses
from db.aggregations import get_phone_aggregation
from db.collections import Task
from db.models import CallAggregation, CallDurationCount
from pydantic import BaseModel
from pymongo import ASCENDING
from pymongo.results import UpdateResult


class BaseClient:
    collection_name: str | None = None
    indexes: list[tuple[str, int]] | None = None

    def __init__(self, database) -> None:
        if not self.collection_name:
            raise NotImplementedError(f'Invalid collection name: {self.collection_name}')
        self.database = database
        self.collection = database.get_collection(self.collection_name)

    async def create_indexes(self):
        if self.indexes is None:
            return
        await self.collection.create_index(self.indexes)


class PhoneCallsClient(BaseClient):
    collection_name = "phone_calls"
    indexes = [('phone', ASCENDING)]

    async def aggregate_call(self, number: int):
        cursor = self.collection.aggregate(
            get_phone_aggregation(number)
        )
        aggregation_result = await anext(cursor)

        call_duration_count = CallDurationCount(
            sec_10=aggregation_result["sec_10"],
            sec_10_30=aggregation_result["sec_10_30"],
            sec_30=aggregation_result["sec_30"],
        )
        return CallAggregation(
            phone=number,
            cnt_all_attempts=aggregation_result["cnt_all_attempts"],
            cnt_att_dur=call_duration_count,
            min_price_att=aggregation_result["min_price_att"],
            max_price_att=aggregation_result["max_price_att"],
            avg_dur_att=aggregation_result["avg_dur_att"],
            sum_price_att_over_15=aggregation_result["sum_price_att_over_15"],
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

    async def error(self, task_id: str, error_message: str):
        return await self.collection.update_one(
            {"task_id": task_id},
            {
                "$set": {
                    "task_status": TaskStatuses.IN_WORK,
                    "error_message": error_message,
                },
            },
        )
