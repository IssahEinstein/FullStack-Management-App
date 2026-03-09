from fastapi import FastAPI
from repositories.prisma_task_repository import PrismaTaskRepository
from repositories.prisma_user_repository import PrismaUserRepository
from services.task_service import TaskService
from services.user_service import UserService
from services.role_service import RoleService
from services.invite_service import InviteService
from api.admin_routes import router as admin_router, set_admin_services
from api.task_routes import router as task_router, set_task_service
from api.user_routes import router as user_router, set_user_service
from api.auth_routes import router as auth_router, set_auth_services
from fastapi.middleware.cors import CORSMiddleware
from db import connect_db, disconnect_db, db

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

user_repo = PrismaUserRepository(db)
user_service = UserService(user_repo)
set_user_service(user_service)

task_repo = PrismaTaskRepository(db)
task_service = TaskService(task_repo)
set_task_service(task_service)

role_service = RoleService(db)
invite_service = InviteService(db)

set_admin_services(user_service, role_service, invite_service)

set_auth_services(user_service, invite_service)

app.include_router(task_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)

