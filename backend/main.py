from fastapi import FastAPI
from repositories.in_memory_task_repository import InMemoryTaskRepository
from repositories.in_memory_user_repository import InMemoryUseRepository
from services.task_service import TaskService
from services.user_service import UserService
from api.task_routes import router as task_router, set_task_service
from api.user_routes import router as user_router, set_user_service
from fastapi.middleware.cors import CORSMiddleware
from db import connect_db, disconnect_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

# cors
# allow_origins=[
#     "https://myapp.com",
#     "https://www.myapp.com"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_repo = InMemoryUseRepository()
user_service = UserService(user_repo)
set_user_service(user_service)

task_repo = InMemoryTaskRepository()
task_service = TaskService(task_repo)

set_task_service(task_service)

app.include_router(task_router)
app.include_router(user_router)



