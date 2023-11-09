from fastapi import FastAPI
from api.responses import TaskStatusResponse, TaskStatusesListResponse, ReportResponse
from api.endpoints import create_report, get_all_tasks_statuses, get_report_task_result, get_task_status

api_perfix = '/api/v1'


def setup_endpoints(app: FastAPI):
    app.get(api_perfix + "/tasks", response_model=TaskStatusesListResponse)(get_all_tasks_statuses)
    app.get(api_perfix + "/tasks/{task_id}", response_model=TaskStatusResponse)(get_task_status)
    app.post(api_perfix + "/report", response_model=TaskStatusResponse)(create_report)
    app.get(api_perfix + "/report/{task_id}", response_model=ReportResponse)(get_report_task_result)
