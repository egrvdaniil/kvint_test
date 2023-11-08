from motor import motor_asyncio

from config import settings

db_client = motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_URI
)

database = db_client.get_database(settings.DATABASE_NAME)  # type:ignore
