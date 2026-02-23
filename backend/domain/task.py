
class Task:
    def __init__(self, title: str, description: str, user_id: str, is_completed: bool = False, id = ""):
        self.id = id
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.user_id = user_id
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.is_completed
        }