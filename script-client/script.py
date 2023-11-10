import argparse
import asyncio
import httpx
import time

async def get_tasks_ids(responses: list[httpx.Response]) -> list[str]:
    ids: list[str] = []
    for response in responses:
        ids.append(response.json()['task_id'])
    return ids

async def wait_for_task(task_id: str, client: httpx.AsyncClient, url: str):
    while True:
        response = await client.get(url + f"/api/v1/tasks/{task_id}")
        if response.json()["task_status"] == "completed":
            break
        await asyncio.sleep(0.5)
        print(f"{task_id}: is not ready, sleep for 0.5 seconds")

async def wait_until_tasks_complete(tasks_ids: list[str], client: httpx.AsyncClient, url: str):
    tasks = []
    for task_id in tasks_ids:
        tasks.append(asyncio.create_task(wait_for_task(task_id, client, url)))
    await asyncio.gather(*tasks)

async def main(args: argparse.Namespace):
    start_time = time.time()
    url = args.url
    concurrency = int(args.concurrency)
    number = int(args.number)
    phones = [int(phone) for phone in args.phones.split(',')]
    data = {
        "numbers": phones,
        "correlation_id": "123123123"
    }
    reports = []
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(number):
            tasks.append(
                asyncio.create_task(client.post(url+"/api/v1/report", json=data))
            )
            if i % concurrency == concurrency-1 or i == number-1:
                print(f"sended {i+1} requests")
                responses = await asyncio.gather(*tasks)
                task_ids = await get_tasks_ids(responses)
                await wait_until_tasks_complete(task_ids, client, url)
                reports_tasks = []
                for task_id in task_ids:
                    reports_tasks.append(asyncio.create_task(client.get(url + f"/api/v1/report/{task_id}")))
                reports_responses = await asyncio.gather(*reports_tasks)
                reports += [report.json() for report in reports_responses]
                tasks = []
    total_times_list = [report['total_duration'] for report in reports]
    print("Result: ", reports[0])
    print(f"Max task work duration: {max(total_times_list)}")
    print(f"Min task work duration: {min(total_times_list)}")
    print(f"Average task work duration: {sum(total_times_list) / len(total_times_list)}")
    print(f"Total working time: {time.time() - start_time}")
    print(len(reports))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Скрипт-клиент для проверки работы сервиса генерации отчета')
    parser.add_argument('-u', '--url', help='Адрес сервиса', default="http://127.0.0.1:8000")
    parser.add_argument('-c', '--concurrency', help='Количество одновременных запросов', default="10")
    parser.add_argument('-n', '--number', help='Общее количество запросов', default="100")
    parser.add_argument('-p', '--phones', help='Номера телефонов через запятую', default="1,2,3,4,5,6,7,8,9,10")
    args = parser.parse_args()
    asyncio.run(main(args))