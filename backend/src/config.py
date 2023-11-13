import os


class Settings:
    def __init__(self):
        if os.environ["IS_TEST"]:
            return
        self.MONGO_URI = os.environ["MONGO_URI"]
        self.DATABASE_NAME = os.environ["DATABASE_NAME"]
        self.RABBITMQ_URI = os.environ["RABBITMQ_URI"]


settings = Settings()
