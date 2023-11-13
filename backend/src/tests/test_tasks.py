import pytest
from unittest.mock import Mock


@pytest.mark.asyncio
async def test_aggregate_task(broker, tasks_collection, test_task):
    aggregate_task = broker.find_task("tasks.calls:aggregate_calls")
    result = await aggregate_task.kicker().with_task_id(test_task.task_id).kiq(
        numbers=[1, 2, 3],
        message_from='client_api',
        correlation_id="correlation_id",
    )
    await result.wait_result()

    updated_task = tasks_collection.find_one({"task_id": test_task.task_id})
    assert updated_task['task_status'] == 'completed'
    assert updated_task['result']["data"] == [
        {
            'phone': 1,
            'cnt_all_attempts': 100000,
            'cnt_att_dur': {'sec_10': 9108, 'sec_10_30': 16496, 'sec_30': 74396},
            'min_price_att': 0,
            'max_price_att': 1200,
            'avg_dur_att': 599.6278,
            'sum_price_att_over_15': 58974760.0
        },
        {
            'phone': 2,
            'cnt_all_attempts': 100000,
            'cnt_att_dur': {'sec_10': 9108, 'sec_10_30': 16496, 'sec_30': 74396},
            'min_price_att': 0,
            'max_price_att': 1200,
            'avg_dur_att': 599.6278,
            'sum_price_att_over_15': 58974760.0
        },
        {
            'phone': 3,
            'cnt_all_attempts': 100000,
            'cnt_att_dur': {'sec_10': 9108, 'sec_10_30': 16496, 'sec_30': 74396},
            'min_price_att': 0,
            'max_price_att': 1200,
            'avg_dur_att': 599.6278,
            'sum_price_att_over_15': 58974760.0
        },
    ]


@pytest.mark.asyncio
async def test_aggregate_task_error(broker, tasks_collection, test_task):
    aggregate_task = broker.find_task("tasks.calls:aggregate_calls")
    result = await aggregate_task.kicker().with_task_id(test_task.task_id).kiq(
        numbers=[1, 2, 3, 4],
        message_from='client_api',
        correlation_id="correlation_id",
    )
    await result.wait_result()

    updated_task = tasks_collection.find_one({"task_id": test_task.task_id})
    assert updated_task['task_status'] == 'error'
    assert updated_task['error_message'] == 'Phones does not exists'
