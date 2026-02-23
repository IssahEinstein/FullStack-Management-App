from prisma import Prisma
from domain.user import User
from domain.interfaces import IUserRepository

class PrismaUserRepository(IUserRepository):
    def __init__(self, db: Prisma):
        self.db = db

    async def add(self, username, email, password_hash):
        created_user = await self.db.user.create(
            data={
                "username": username,
                "email":email,
                "password_hash": password_hash
            }
        )
        return User(
        id=created_user.id,
        username=created_user.username,
        email=created_user.email,
        password_hash=created_user.password_hash
    )

    async def get_by_username(self, username: str):
        user = await self.db.user.find_unique(
            where={"username": username}
        )
        if user is None:
            return None

        return User(username=user.username, email=user.email, password_hash=user.password_hash, id=user.id)

    async def get_by_email(self, email: str):
        user = await self.db.user.find_unique(
            where={"email": email}
        )
        if user is None:
            return None
        
        return User(username=user.username, email=user.email, password_hash=user.password_hash, id=user.id)

    async def get_by_id(self, id: str):
        user = await self.db.user.find_unique(
            where={"id": id}
        )
        if user is None:
            return None
        
        return User(username=user.username, email=user.email, password_hash=user.password_hash, id=user.id)