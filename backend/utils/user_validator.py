from domain.interfaces import IUserRepository
from exceptions.user_exceptions import UserAlreadyExistsError, PasswordInvalidExistsError, EmaiAlreadyExistsError, InvalidEmailError, InvalidUsernameError, UserDoesNotExistError

class UserValidator:

    @staticmethod
    async def validate_new_user(username: str, email: str, password: str, repo: IUserRepository):
        if not username or len(username) < 3:
            raise InvalidUsernameError("Username must be at least 3 characters")

        if not email or "@" not in email:
            raise InvalidEmailError("Invalid email")
        
        validate_by_username = await repo.get_by_username(username)
        if validate_by_username:
            raise UserAlreadyExistsError("Username already exists")

        validate_by_email = await repo.get_by_email(email)
        if validate_by_email:
            raise EmaiAlreadyExistsError("Email already exists")

        if len(password) < 6:
            raise PasswordInvalidExistsError("Password must be at least 6 characters")

    @staticmethod
    async def validate_existing_user(user_id: str, repo: IUserRepository):
        user = await repo.get_by_id(user_id)
        if user is None:
            raise UserDoesNotExistError(f"User with 'id: {user_id}' does not exist")
        return user