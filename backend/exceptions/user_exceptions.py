class UserError(Exception):
    """Base class for all user-related errors."""
    pass

class InvalidUsernameError(UserError):
    """Raised when username is empty or less than 3 characters"""
    pass

class UserAlreadyExistsError(UserError):
    """Raised when attempting to create a username that already exists."""
    pass

class InvalidEmailError(UserError):
    """Raised when email has no '@' or not entred at all or an email that already exists"""
    pass

class EmaiAlreadyExistsError(UserError):
    """Raised when attempting to create an email that already exists."""
    pass

class PasswordInvalidExistsError(UserError):
    """Raised when password is less than 6 characters long"""
    pass