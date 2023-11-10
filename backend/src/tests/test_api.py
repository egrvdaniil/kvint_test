def test_task_creation(api_client, tasks_collection):
    response = api_client.post(
        "/api/v1/report",
        json={
            "numbers": [11, 13],
            "correlation_id": "123123123"
        },
    )

    assert response.json()["task_status"] == "pending"
    assert response.json()["task_name"] == "tasks.calls:aggregate_calls"
    task = tasks_collection.find({"task_id": response.json()["task_id"]})
    assert task is not None


def test_get_task_info(api_client, test_task):
    response = api_client.get(
        f"/api/v1/tasks/{test_task.task_id}",
    )

    assert response.json()["task_status"] == "pending"
    assert response.json()["task_id"] == test_task.task_id


def test_get_result(api_client, completed_task, test_result):
    response = api_client.get(
        f"/api/v1/report/{completed_task.task_id}",
    )

    assert response.json()["correlation_id"] == test_result["correlation_id"]
