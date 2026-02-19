class TaskSerializer:
    @staticmethod
    def to_dict(task):
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.is_completed
        }