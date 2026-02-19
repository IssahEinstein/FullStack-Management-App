from domain.interfaces import IUserRepository
from exceptions.user_exceptions import UserAlreadyExistsError, PasswordInvalidExistsError, EmaiAlreadyExistsError, InvalidEmailError, InvalidUsernameError

class UserValidator:

    @staticmethod
    def validate_new_user(username: str, email: str, password: str, repo: IUserRepository):
        if not username or len(username) < 3:
            raise InvalidUsernameError("Username must be at least 3 characters")

        if not email or "@" not in email:
            raise InvalidEmailError("Invalid email")

        if repo.get_by_username(username):
            raise UserAlreadyExistsError("Username already exists")

        if repo.get_by_email(email):
            raise EmaiAlreadyExistsError("Email already exists")

        if len(password) < 6:
            raise PasswordInvalidExistsError("Password must be at least 6 characters")
