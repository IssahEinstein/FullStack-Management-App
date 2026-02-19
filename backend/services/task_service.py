from domain.interfaces import ITaskRepository
from domain.task import Task
from utils.task_validator import TaskValidator
from utils.task_serializer import TaskSerializer

class TaskService:
    def __init__(self, repository: ITaskRepository):
        self.repository = repository

    def create_task(self, title: str, description: str, user_id: int):
        TaskValidator.validate_new_task(title, description, self.repository)
        task = Task(id = 1, title=title, description=description, user_id = user_id)
        self.repository.add(task)
        return task
    
    def delete_task(self, id: int, user_id: int):
        task = TaskValidator.validate_task_exists(id, user_id, self.repository)
        self.repository.delete_task(task.id, user_id)
        return task
        
    
    def complete_task(self, id: int, user_id: int):
        task = TaskValidator.validate_task_exists(id, user_id, self.repository)
        task.complete()
        return task
    
    def get_single_task(self, id: int, user_id: int):
        task = TaskValidator.validate_task_exists(id, user_id, self.repository)
        return TaskSerializer.to_dict(task)
    
    def list_tasks(self, user_id):
        return self.repository.get_all(user_id)
