from fastapi import APIRouter, HTTPException, Depends
from utils.task_serializer import TaskSerializer
from core.logging_config import logger
from schemas.task_schemas import TaskCreate
from utils.dependencies import get_current_user

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
async def get_single_task(task_id: str, user_id: str = Depends(get_current_user)):
    try:
        task = await service.get_single_task(task_id, user_id)
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

