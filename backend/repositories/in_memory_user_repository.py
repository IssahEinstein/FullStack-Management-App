from domain.interfaces import IUserRepository
from domain.user import User

class InMemoryUseRepository(IUserRepository):
    def __init__(self):
        self.users = []
        self.next_id = 1
    
    def add(self, user: User):
        user.id = self.next_id
        self.next_id += 1
        self.users.append(user)

    def get_by_username(self, username: str):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def get_by_email(self, email: str):
        for user in self.users:
            if user.email == email:
                return user
        return None
    
    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None