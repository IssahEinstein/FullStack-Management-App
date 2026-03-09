from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.invite_service import InviteService
from services.user_service import UserService
from db import db


class AcceptInviteSchema(BaseModel):
    token: str
    password: str


router = APIRouter(prefix="/auth", tags=["Auth"])

user_service: UserService = None
invite_service: InviteService = None

def set_auth_services(u_service, i_service):
    global user_service, invite_service
    user_service = u_service
    invite_service = i_service



@router.post("/accept-invite")
async def accept_invite(data: AcceptInviteSchema):
    # 1. Validate the invite
    invite = await invite_service.validate_invite(data.token)
    if not invite:
        raise HTTPException(400, "Invalid or expired invite")

    # 2. Hash the new password
    hashed_pw = user_service.hash_password(data.password)

    # 3. Activate the user
    await db.user.update(
        where={"id": invite.userId},
        data={
            "password_hash": hashed_pw,
            # "is_active": True,
        }
    )

    # 4. Mark invite as used
    await invite_service.consume_invite(data.token)

    return {"message": "Account activated successfully"}