from motor.motor_asyncio import AsyncIOMotorClient
# from config import MONGO_DB
MONGO_DB="mongodb+srv://coderstrings:Admitnow%4012345@cluster0.zhngv.mongodb.net/coders?retryWrites=true&w=majority"
class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client.coders


async def connect_to_mongo():
   
    db.client = AsyncIOMotorClient(str(MONGO_DB),tls=True, tlsAllowInvalidCertificates=True)

async def close_mongo_connection():

    db.client.close()