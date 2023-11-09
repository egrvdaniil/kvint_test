import os


class Settings:
    def __init__(self):
        self.MONGO_URI = os.environ["MONGO_URI"]
        self.DATABASE_NAME = os.environ["DATABASE_NAME"]
        self.RABBITMQ_URI = os.environ["RABBITMQ_URI"]


settings = Settings()
