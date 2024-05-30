import motor.motor_asyncio
from fast_auth.auth.models import UserInDB, BlacklistToken
from datetime import datetime
from fast_auth.config import MONGO_URI, MONGO_DB_NAME


class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.users_collection = self.db["users"]
        self.blacklist_collection = self.db["blacklist"]

    async def create_user(self, user: UserInDB):
        await self.users_collection.insert_one(user.dict())

    async def get_user(self, email: str):
        return await self.users_collection.find_one({"email": email})

    async def add_token_to_blacklist(self, token: str):
        blacklist_token = BlacklistToken(token=token, blacklisted_on=datetime.utcnow())
        await self.blacklist_collection.insert_one(blacklist_token.dict())

    async def is_token_blacklisted(self, token: str) -> bool:
        token_in_blacklist = await self.blacklist_collection.find_one({"token": token})
        return token_in_blacklist is not None

db = MongoDB(MONGO_URI, MONGO_DB_NAME)
