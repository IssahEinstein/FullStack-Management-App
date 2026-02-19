from fastapi import APIRouter, HTTPException
from core.logging_config import logger
from schemas.user_schemas import UserCreate, UserLogin
from utils.user_serializer import UserSerializer
from utils.jwt_handler import create_access_token


router = APIRouter()

# connecting user router to my business logic
service = None
def set_user_service(user_service):
    global service
    service = user_service

@router.post("/users/signup")
def signup(data: UserCreate):
    try:
        user = service.create_user(
            data.username,
            data.email,
            data.password
        )
        logger.info(f"User with id {user.id} and email {user.email} has been created successfully")
        return UserSerializer.to_dict(user)
    except Exception as e:
        logger.error(f"Signup failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/users/login")
def login(data: UserLogin):
    try:
        user = service.authenticate(
            data.username,
            data.password
        )
        logger.info(f"User with id {user.id} and email {user.email} has succussfully logged in")

        token = create_access_token({"user_id": user.id})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        logger.error("Invalid login attempt")
        raise HTTPException(status_code=401, detail="Invalid credentials")

