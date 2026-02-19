from domain.task import Task
from domain.interfaces import ITaskRepository


class InMemoryTaskRepository(ITaskRepository):
    def __init__(self):
        self._tasks: list[Task] = []
        self.next_id = 1
    
    def add(self, task: Task) -> None:
        task.id = self.next_id
        self._tasks.append(task)
        self.next_id += 1
    
    def delete_task(self, id: int, user_id: int) -> Task:
        task = self.get_by_id(id, user_id)
        self._tasks.remove(task)

    def get_all(self, user_id: int) -> list[Task]:
        return [task for task in self._tasks if task.user_id == user_id]

    def get_by_id(self, id: int, user_id: int) -> Task | None:
        for task in self._tasks:
            if task.id == id and task.user_id == user_id:
                return task
        return None
