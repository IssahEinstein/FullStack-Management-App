from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, ConfigDict
from services.invite_service import InviteService
from services.user_service import UserService
from services.role_service import RoleService

class CreateParentSchema(BaseModel):
    username: str
    email: str
    password: str

router = APIRouter(prefix="/admin", tags=["Admin"])


user_service: UserService = None
role_service: RoleService = None
invite_service: InviteService = None

def set_admin_services(u_service, r_service, i_service):
    global user_service, role_service, invite_service
    user_service = u_service
    role_service = r_service
    invite_service = i_service


FRONTEND_URL = "http://localhost:5173"

@router.post("/create-parent")
async def create_parent(data: CreateParentSchema):
    try:
        # 1. Create parent user
        parent = await user_service.create_parent(data.username, data.email, data.password)

        # 2. Assign parent role
        await role_service.assign_role(parent.id, "parent")

        # 3. Generate invite token
        token = await invite_service.create_parent_invite(parent.id)

        # 4. Build invite link
        invite_link = f"{FRONTEND_URL}/accept-invite?token={token}"
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    return {"invite_link": invite_link, "parent_id": parent.id}
    
    
