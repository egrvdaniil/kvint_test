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


def test_get_task_info(api_client, tasks_collection, test_task):
    response = api_client.get(
        f"/api/v1/tasks/{test_task.task_id}",
    )

    assert response.json()["task_status"] == "pending"
    assert response.json()["task_id"] == test_task.task_id
