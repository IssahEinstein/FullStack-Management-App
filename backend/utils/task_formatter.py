from domain.task import Task

class TaskFormatter:
    @staticmethod
    def to_string(task: Task) -> str:
        return f"{task.title} - {task.description} (Completed: {task.is_completed})"