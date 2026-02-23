from domain.interfaces import ITaskRepository
from domain.task import Task
from utils.task_validator import TaskValidator
from utils.task_serializer import TaskSerializer
from fastapi import Depends
from utils.dependencies import get_current_user

class TaskService:
    def __init__(self, repository: ITaskRepository):
        self.repository = repository

    async def create_task(self, title: str, description: str, user_id: str = Depends(get_current_user)):
        TaskValidator.validate_new_task(title, description, self.repository)
        new_task = await self.repository.add(title=title, description=description, user_id=user_id, is_completed=False)
        return new_task
    
    async def delete_task(self, id: str, user_id: str = Depends(get_current_user)):
        task = await TaskValidator.validate_task_exists(id, user_id, self.repository)
        await self.repository.delete_task(task.id, user_id)
        return task
        
    
    async def complete_task(self, id: str, user_id: str = Depends(get_current_user)):
        task = await TaskValidator.validate_task_exists(id, user_id, self.repository)
        await self.repository.complete(task.id)
        return task
    
    async def get_single_task(self, id: str, user_id: str = Depends(get_current_user)):
        task = await TaskValidator.validate_task_exists(id, user_id, self.repository)
        return TaskSerializer.to_dict(task)
    
    async def list_tasks(self, user_id: str = Depends(get_current_user)):
        return await self.repository.get_all(user_id)
