from fastapi import APIRouter, HTTPException, Depends, Response, Request
from core.logging_config import logger
from schemas.user_schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from utils.user_serializer import UserSerializer
from utils.jwt_handler import create_access_token, create_refresh_token, verify_refresh_token, InvalidTokenError, REFRESH_TOKEN_EXPIRE_DAYS
from utils.dependencies import get_current_user, get_refresh_token_repo
from repositories.in_memory_refresh_token_repository import InMemoryRefreshTokenRepository



router = APIRouter(prefix="/users", tags=["Users"])

# connecting user router to my business logic
service = None
def set_user_service(user_service):
    global service
    service = user_service

@router.get("/me", response_model=UserResponse)
def get_me(user_id: int = Depends(get_current_user)):
    try:
        user = service.get_single_user(user_id)
        logger.info(f"User with {user_id} successfully retrieved")
        return user
    except Exception as e:
        logger.error(f"User validation failed: {e}")
        return HTTPException(status_code=500, detail=str(e))

@router.post("/signup")
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

@router.post("/login")
def login(data: UserLogin, response: Response, refresh_repo: InMemoryRefreshTokenRepository = Depends(get_refresh_token_repo)):
    try:
        user = service.authenticate(
            data.username,
            data.password
        )
        logger.info(f"User with id {user.id} and email {user.email} has succussfully logged in")

        import secrets
        
        csrf_token = secrets.token_urlsafe(32)
        response.set_cookie(
            key="csrf_token",
            value=csrf_token,
            httponly=False,   # must be readable by JS
            secure=True,
            samesite="none",
            )


        access_token = create_access_token({"user_id": user.id})
        refresh_token = create_refresh_token(user.id)

        refresh_repo.save(user.id, refresh_token)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        logger.error("Invalid login attempt")
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/refresh")
def refresh_access_token(
    request: Request,
    response: Response,
    refresh_repo: InMemoryRefreshTokenRepository = Depends(get_refresh_token_repo),
):
    # VERIFY CSRF TOKEN before verifying refresh token
    csrf_cookie = request.cookies.get("csrf_token")
    csrf_header = request.headers.get("X-CSRF-Token")

    if not csrf_cookie or not csrf_header or csrf_cookie != csrf_header:
        raise HTTPException(status_code=403, detail="CSRF validation failed")
    

    cookie_token = request.cookies.get("refresh_token")
    if not cookie_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    


    try:
        user_id = verify_refresh_token(cookie_token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))

    stored_token = refresh_repo.get(user_id)

    if stored_token is None:
    # User logged out or token was revoked
        raise HTTPException(status_code=401, detail="Session expired")


    if stored_token != cookie_token:
        refresh_repo.delete(user_id)  # invalidate ALL sessions (- cryptographic intrusion detection system)

        raise HTTPException(status_code=401, detail="Suspicious activity detected")

    new_refresh = create_refresh_token(user_id)
    refresh_repo.save(user_id, new_refresh)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    new_access = create_access_token({"sub": str(user_id)})

    return {"access_token": new_access, "token_type": "bearer"}

@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    refresh_repo: InMemoryRefreshTokenRepository = Depends(get_refresh_token_repo),
    ):
    
    # VERIFYING CRSF TOKEN BEFORE VERIFYING REFRESH TOKEN TO PREVENT FORCED LOG-OUT
    csrf_cookie = request.cookies.get("csrf_token")
    csrf_header = request.headers.get("X-CSRF-Token")

    if not csrf_cookie or not csrf_header or csrf_cookie != csrf_header:
        raise HTTPException(status_code=403, detail="CSRF validation failed")

    cookie_token = request.cookies.get("refresh_token")

    if cookie_token:
        try:
            user_id = verify_refresh_token(cookie_token)
            refresh_repo.delete(user_id)
        except InvalidTokenError as e:
            raise HTTPException(status_code=401, detail=str(e))

    response.delete_cookie(
        key="refresh_token",
        samesite="none",
        secure=True,
    )

    return {"detail": "Logged out"}


