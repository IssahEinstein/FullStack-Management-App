from domain.task import Task
from domain.interfaces import ITaskRepository
from exceptions.task_exceptions import TaskAlreadyExistsError, TaskNotFoundError, InvalidTaskDataError

class TaskValidator:
    @staticmethod
    def validate_new_task(title: str, description: str, repository: ITaskRepository):
        if not title or title.strip() == "":
            raise InvalidTaskDataError("Title cannot be empty.")

    @staticmethod
    async def validate_task_exists(id: str, user_id: str, repository: ITaskRepository) -> Task:
        task = await repository.get_by_id(id, user_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id {id} does not exist.") # specify user whose task failed vallidation
        return task