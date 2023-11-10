def test_task_creation(api_client, tasks_collection):
    response = api_client.post(
        "/api/v1/report",
        json={
            "numbers": [11, 13],
            "correlation_id": "123123123"
        },
    )

    assert response.json()["task_status"] == 'pending'
    assert response.json()["task_name"] == 'tasks.calls:aggregate_calls'
    task = tasks_collection.find({"task_id": response.json()["task_id"]})
    assert task is not None
