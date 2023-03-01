class TaskNotFoundException(Exception):
    def __init__(self, task_id: int):
        self.message = f"Task not found: {task_id}"
        super().__init__(self.message)