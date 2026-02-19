
class Task:
    def __init__(self, id: int, title: str, description: str, user_id: int, is_completed: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.user_id = user_id
    
    def complete(self):
        self.is_completed = True

    def __str__(self):
        status = "Task Completed ✅" if self.is_completed else "Pending ⏳"
        return f"Task : {self.title} | Status: {status}\tDescription: {self.description}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.is_completed
        }