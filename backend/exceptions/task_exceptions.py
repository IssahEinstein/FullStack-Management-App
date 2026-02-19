class TaskError(Exception):
    """Base class for all task-related errors."""
    pass

class TaskAlreadyExistsError(TaskError):
    """Raised when attempting to create a task with an ID that already exists."""
    pass

class TaskNotFoundError(TaskError):
    """Raised when a task with the given ID does not exist."""
    pass

class InvalidTaskDataError(TaskError):
    """Raised when task data (title, description, etc.) is invalid."""
    pass