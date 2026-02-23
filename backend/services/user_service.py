import hashlib
from domain.user import User
from utils.user_validator import UserValidator

class UserService:
    def __init__(self, repository):
        self.repository = repository

    def hash_password(self, password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    async def create_user(self, username: str, email: str, password: str):
        await UserValidator.validate_new_user(username, email, password, self.repository)

        password_hash = self.hash_password(password)

        saved_user = await self.repository.add(username, email, password_hash)
        return saved_user
 
    async def authenticate(self, username: str, password: str):
        user = await self.repository.get_by_username(username)
        
        if user is None:
            raise ValueError("User not found") 

        if user.password_hash != self.hash_password(password):
            raise ValueError("Invalid password")

        return user
    
    async def get_single_user(self, user_id):
        user = await UserValidator.validate_existing_user(user_id, self.repository)
        return user
