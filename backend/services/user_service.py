import hashlib
from domain.user import User
from utils.user_validator import UserValidator

class UserService:
    def __init__(self, repository):
        self.repository = repository

    def hash_password(self, password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username: str, email: str, password: str):
        UserValidator.validate_new_user(username, email, password, self.repository)

        password_hash = self.hash_password(password)

        user = User(
            id=0,
            username=username,
            email=email,
            password_hash=password_hash
        )

        self.repository.add(user)
        return user

    def authenticate(self, username: str, password: str):
        user = self.repository.get_by_username(username)
        if not user:
            return None

        if user.password_hash != self.hash_password(password):
            return None

        return user
    
    def get_single_user(self, user_id):
        user = UserValidator.validate_existing_user(user_id, self.repository)
        return user