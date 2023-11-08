from fastapi import FastAPI
from api.responses import TaskStatusResponse, TaskStatusesListResponse

api_perfix = 'api/v1'


def setup_endpoints(app: FastAPI):
    app.get(api_perfix + "/tasks", response_model=TaskStatusesListResponse)()  # type:ignore
    app.post(api_perfix + "/report", response_model=TaskStatusResponse)()  # type:ignore
