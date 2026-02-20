from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    # model_config = ConfigDict(from_attributes=True) ** think about adding this in relation to prisma objects and supabase
    id: int
    username: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
