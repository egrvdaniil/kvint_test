
from typing import Any

from db.clients import TasksClient
from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult


class ExceptionErrorHandlerMiddleware(TaskiqMiddleware):
    async def on_error(
        self,
        message: TaskiqMessage,
        result: TaskiqResult[Any],
        exception: BaseException,
    ):
        tasks_client: TasksClient = self.broker.state.tasks_client
        await tasks_client.error(message.task_id, str(exception))
