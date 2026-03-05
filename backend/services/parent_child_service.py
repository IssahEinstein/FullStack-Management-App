class ParentChildService:
    def __init__(self, db):
        self.db = db

    async def link_parent_child(self, parent_id: str, child_id: str):
        await self.db.parentchild.create(
            data={"parentId": parent_id, "childId": child_id}
        )

    async def unlink_parent_child(self, parent_id: str, child_id: str):
        await self.db.parentchild.delete_many(
            where={"parentId": parent_id, "childId": child_id}
        )

    async def is_parent_of(self, parent_id: str, child_id: str) -> bool:
        return await self.db.parentchild.find_first(
            where={"parentId": parent_id, "childId": child_id}
        ) is not None

    async def get_children(self, parent_id: str):
        records = await self.db.parentchild.find_many(
            where={"parentId": parent_id},
            include={"child": True}
        )
        return [r.child for r in records]