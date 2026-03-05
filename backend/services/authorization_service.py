from services.role_service import RoleService
from services.parent_child_service import ParentChildService

class AuthorizationService:
    def __init__(self, role_service: RoleService, parent_child_service: ParentChildService):
        self.role_service = role_service
        self.parent_child_service = parent_child_service

    async def can_manage_task(self, actor_id: str, task_owner_id: str) -> bool:
        if await self.role_service.user_has_role(actor_id, "admin"):
            return True

        if actor_id == task_owner_id:
            return True

        if await self.role_service.user_has_role(actor_id, "parent"):
            return await self.parent_child_service.is_parent_of(actor_id, task_owner_id)

        return False

    async def can_manage_user(self, actor_id: str, target_user_id: str) -> bool:
        if await self.role_service.user_has_role(actor_id, "admin"):
            return True

        if await self.role_service.user_has_role(actor_id, "parent"):
            return await self.parent_child_service.is_parent_of(actor_id, target_user_id)

        return False