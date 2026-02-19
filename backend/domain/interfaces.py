from typing import Protocol


class ITaskRepository(Protocol):
    
    def add(self, task):
        pass

    def get_all(self):
        pass

    def get_by_id(self, id: int):
        pass

class IUserRepository(Protocol):

    def add(self, user):
        pass

    def get_by_username(self, username: str):
        pass

    def get_by_email(self, email: str):
        pass