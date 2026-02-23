import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from exceptions.refresh_token_exceptions import InvalidTokenError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

ALGORITHM = "HS256"

# take the user_id as a dictionary to create a token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    
def create_refresh_token(user_id: str) -> str:
    """
    Refresh token is long-lived and only used to get new access tokens.
    """
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

            #REFRESH TOKEN

def verify_refresh_token(token: str) -> str:
    """
    Returns user_id if valid, otherwise raises InvalidTokenError.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise InvalidTokenError("Invalid token type")

        return payload["sub"]

    except jwt.ExpiredSignatureError:
        raise InvalidTokenError("Refresh token expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid refresh token")
