from fastapi import APIRouter, HTTPException, Depends
from utils.task_serializer import TaskSerializer
from core.logging_config import logger
from schemas.task_schemas import TaskCreate
from utils.dependencies import get_current_user, get_task_repo, get_auth_service
from repositories.prisma_user_repository import PrismaUserRepository

router = APIRouter()

# connecting router to my business logic
service = None
def set_task_service(task_service):
    global service
    service = task_service

@router.get("/tasks")
async def get_tasks(user_id: str = Depends(get_current_user)):
    try:
        tasks = await service.list_tasks(user_id)
        logger.info(f"All tasks retrieved successfully")
        return [TaskSerializer.to_dict(task) for task in tasks]
    except Exception as e:
        logger.error(f"Task Validation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/{task_id}")
async def get_single_task(task_id: str, user_id: str = Depends(get_current_user), task_repo: PrismaUserRepository =  Depends(get_task_repo), auth_service: bool = Depends(get_auth_service)):
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    
    if not await auth_service.can_manage_task(user_id, task.user_id):
        raise HTTPException(403, "Forbidden")

    try:
        logger.info("A single task was retrieved successfully")
        return task
    except Exception as e:
        logger.error(f"Task Validation failed: {e}")
        raise HTTPException(status_code= 500, detail=str(e))

@router.post("/tasks")
async def create_task(task_data: TaskCreate, user_id: str = Depends(get_current_user)):
    try:
        task = await service.create_task(
            task_data.title,
            task_data.description,
            user_id = user_id
        )
        logger.info(f"Task with title {task.title} and ID {task.id} created successfully") # checkpoint for error in case id error raised
        return TaskSerializer.to_dict(task)
    except Exception as e:
        logger.error(f"Task Validation failed: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/tasks/{task_id}/complete")
async def complete_task(task_id: str, user_id: str = Depends(get_current_user)):
    try:
        task = await service.complete_task(task_id, user_id)
        logger.info(f"Task with id {task_id} completed")
        return TaskSerializer.to_dict(task)
    except Exception as e:
        logger.error(f"Task Validation failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/tasks/{task_id}/delete")
async def delete_task(task_id: str, user_id: str = Depends(get_current_user)):
    try:
        task = await service.delete_task(task_id, user_id)
        logger.info(f"Task with id {task_id} deleted successfully")
        return task
    except Exception as e:
        logger.error(f"Task Validation failed: {e}")
        raise HTTPException(status_code=200, detail=str(e))

