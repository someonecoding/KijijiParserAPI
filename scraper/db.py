import motor.motor_asyncio
from os import getenv

DATABASE_NAME = getenv('MONGO_INITDB_DATABASE')
DATABASE_USER = getenv('MONGO_INITDB_ROOT_USERNAME')
DATABASE_PASSWORD = getenv('MONGO_INITDB_ROOT_PASSWORD')
DATABASE_URI = f'mongodb://{DATABASE_USER}:{DATABASE_PASSWORD}@mongodb:27017'

print(DATABASE_URI)

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]

async def insert_data(collection_name, data):
    result = await db[collection_name].insert_one(data)
    return result
