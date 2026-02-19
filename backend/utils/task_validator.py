from domain.task import Task
from domain.interfaces import ITaskRepository
from exceptions.task_exceptions import TaskAlreadyExistsError, TaskNotFoundError, InvalidTaskDataError

class TaskValidator:
    @staticmethod
    def validate_new_task(title: str, description: str, repository: ITaskRepository):
        if not title or title.strip() == "":
            raise InvalidTaskDataError("Title cannot be empty.")

        if not description or len(description.strip()) < 5:
            raise InvalidTaskDataError("Description needs at least 5 characters")

        # if repository.get_by_id(id) is not None:
        #     raise TaskAlreadyExistsError(f"Task with id {id} already exists.")

    @staticmethod
    def validate_task_exists(id: int, user_id: int, repository: ITaskRepository) -> Task:
        task = repository.get_by_id(id, user_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id {id} does not exist.") # specify user whose task failed vallidation
        return task