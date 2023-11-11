# Тестовое задание на вакансию в компанию KVINT

## Архитектура

API написан с использованием FastAPI

Воркеры и брокер сообщений - [taskiq](https://taskiq-python.github.io)

В качестве очереди используется RabbitMQ

## Ендпоинты
```
GET /api/v1/tasks - Получение информации о всех тасках на создание отчета
GET /api/v1/tasks/{task_id} - Получение информации таске на создание отчета по id
POST /api/v1/report - Создание таски на создание отчета
GET /api/v1/report/{task_id} - Получение отчета по id таски

Подробнее в Swagger документации /docs
```

## Запуск API и воркеров

Клонируем проект:
```
git clone https://github.com/egrvdaniil/kvint_test.git
```

Переходим в папку backend:
```
cd backend
```
Создаем файл .env на основе .env.example:
```
cp .env.example .env
```

Запускам с помощью Docker-compose:
```
docker-compose up
```

## Запуск скрипт клиента

Переходим в папку script-client:
```
cd script-client
```

Устанавливаем зависимости:
```
poetry install
```

Запускаем скрипт:
```
poetry run python script.py
```

### Аргументы скрипта

```
options:
  -h, --help - show this help message and exit
  -u URL, --url URL - Адрес сервиса
  -c CONCURRENCY, --concurrency CONCURRENCY - Количество одновременных запросов
  -n NUMBER, --number NUMBER - Общее количество запросов
  -p PHONES, --phones PHONES - Номера телефонов через запятую
```

### Пример вывода скрипта

```
Result:  {
   "data":[
      {
         "phone":1,
         "cnt_all_attempts":100000,
         "cnt_att_dur":{
            "10_sec":9244,
            "10_30_sec":16715,
            "30_sec":74041
         },
         "min_price_att":0,
         "max_price_att":1200,
         "avg_dur_att":599.1029,
         "sum_price_att_over_15":58898330.0
      }
   ],
   "total_duration":0.4248208999633789,
   "received":"2023-11-10T14:36:22.958000",
   "task_from":"client_api",
   "task_to":"client",
   "correlation_id":"123123123"
}
Max task work duration: 0.44716429710388184
Min task work duration: 0.2892310619354248
Average task work duration: 0.35308352947235105
Total working time: 5.859595060348511
```

## Скорость работы сервиса
На сервис было отправлено 100 запросов на создание отчета по 10 запросов за раз.
В каждом запросе содержалось по 10 номеров,

```
Max task work duration: 4.0182812213897705
Min task work duration: 2.785856008529663
Average task work duration: 3.0934303307533266
Total working time: 38.3143208026886
```
Тест был сделан локально на MacBook Air 2022
