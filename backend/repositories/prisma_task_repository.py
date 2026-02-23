from prisma import Prisma
from domain.task import Task
from domain.interfaces import ITaskRepository


class PrismaTaskRepository(ITaskRepository):
    def __init__(self, db: Prisma):
        self.db = db

    async def add(self, title, description, user_id, is_completed):
        record = await self.db.task.create(
            data={
                "title": title,
                "description": description,
                "userId": user_id,
                "completed": is_completed
            }
        )
        return Task(
            title=record.title,
            description=record.description,
            user_id=record.userId,
            is_completed=record.completed,
            id=record.id            
        )
    
    async def delete_task(self, id: str, user_id: str) -> Task | None:
        # First fetch the task (ownership enforced)
        task = await self.get_by_id(id, user_id)
        if task is None:
            return None

        # Delete it from the DB
        await self.db.task.delete(
            where={"id": id}
        )

        return task


    async def get_all(self, user_id: str):
        records = await self.db.task.find_many(
            where={"userId": user_id}
        )
        return [
            Task(
                title=r.title,
                description=r.description,
                user_id=r.userId,
                is_completed=r.completed,
                id=r.id
            )
            for r in records
        ]
    
    async def get_by_id(self, id: str, user_id: str) -> Task | None:
        record = await self.db.task.find_first(
            where={
                "id": id,
                "userId": user_id
            }
        )

        if record is None:
            return None

        return Task(
            title=record.title,
            description=record.description,
            user_id=record.userId,
            is_completed=record.completed,
            id=record.id
        )
    
    async def complete(self, task_id):
        await self.db.task.update(
            where={"id": task_id},
            data={"completed": True}
            )
