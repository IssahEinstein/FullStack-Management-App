from typing import Protocol


class ITaskRepository(Protocol):
    
    def add(self, task):
        pass

    def get_all(self):
        pass

    def get_by_id(self, id: int):
        pass

class IUserRepository(Protocol):

    async def add(self, user):
        pass

    async def get_by_username(self, username: str):
        pass

    async def get_by_email(self, email: str):
        pass

class IRefreshtokenRepository(Protocol):

    def save(self, user_id: int, token: str):
        pass

    def get(self, user_id: int):
        pass

    def delete(self, user_id: int):
        pass