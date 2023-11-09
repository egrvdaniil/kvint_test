from fastapi import FastAPI
from api.responses import TaskStatusResponse, TaskStatusesListResponse
from api.endpoints import create_report, get_tasks_info

api_perfix = '/api/v1'


def setup_endpoints(app: FastAPI):
    app.get(api_perfix + "/tasks", response_model=TaskStatusesListResponse)(get_tasks_info)
    app.post(api_perfix + "/report", response_model=TaskStatusResponse)(create_report)
