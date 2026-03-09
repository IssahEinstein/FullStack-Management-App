# from utils.dependencies import get_current_user


class RoleService:
    def __init__(self, repository):
        self.repository = repository

    async def assign_role(self, user_id: str, role_name: str):
        role = await self.repository.role.find_unique(where={"name": role_name})
        if not role:
            raise ValueError("Role does not exist")

        await self.repository.userrole.create(
            data={"userId": user_id, "roleId": role.id}
        )

    async def remove_role(self, user_id: str, role_name: str):
        role = await self.repository.role.find_unique(where={"name": role_name})
        if not role:
            raise ValueError("Role does not exist")

        await self.repository.userrole.delete_many(
            where={"userId": user_id, "roleId": role.id}
        )

    async def user_has_role(self, user_id: str, role_name: str) -> bool:
        return await self.repository.userrole.find_first(
            where={
                "userId": user_id,
                "role": {"name": role_name}
            }
        ) is not None

    async def get_roles(self, user_id: str) -> list[str]:
        records = await self.repository.userrole.find_many(
            where={"userId": user_id},
            include={"role": True}
        )
        return [r.role.name for r in records]