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
def get_tasks(user_id: int = Depends(get_current_user)):
    try:
        tasks = service.list_tasks(user_id)
        logger.info(f"All tasks retrieved successfully")
        return [TaskSerializer.to_dict(task) for task in tasks]
    except Exception as e:
        logger.error(f"Task Validation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/{task_id}")
def get_single_task(task_id: int, user_id: int = Depends(get_current_user)):
    # print("hello world")
    try:
        task = service.get_single_task(task_id, user_id)
        logger.info("A single task was retrieved successfully")
        return task
    except Exception as e:
        logger.error(f"Task Validation failed: {e}")
        raise HTTPException(status_code= 500, detail=str(e))

@router.post("/tasks")
def create_task(task_data: TaskCreate, user_id: int = Depends(get_current_user)):
    try:
        task = service.create_task(
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
def complete_task(task_id: int, user_id: int = Depends(get_current_user)):
    try:
        task = service.complete_task(task_id, user_id)
        logger.info(f"Task with id {task_id} completed")
        return TaskSerializer.to_dict(task)
    except Exception as e:
        logger.error(f"Task Validation failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/tasks/{task_id}/delete")
def delete_task(task_id: int, user_id: int = Depends(get_current_user)):
    try:
        task = service.delete_task(task_id, user_id)
        logger.info(f"Task with id {task_id} deleted successfully")
        return task
    except Exception as e:
        logger.error(f"Task Validation failed: {e}")
        raise HTTPException(status_code=200, detail=str(e))

