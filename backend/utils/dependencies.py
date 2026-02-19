from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_handler import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))