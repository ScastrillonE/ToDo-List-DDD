class Task:
    def __init__(self, title: str, description: str, status: str, id: int = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status