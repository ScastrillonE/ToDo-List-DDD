from app.basework.domain import value_objects as shared_value_objects
from app.domain import value_objects 
from app.domain import entities

class TaskUC:
    def __init__(self, task_repo, user_repo=None):
        self._task_repo = task_repo

    def create_task(self, user_id, name)-> entities.Task:
        task_id = str(shared_value_objects.UUID)
        new_task = entities.Task(task_id = task_id, user_id = 0, name = name, status = value_objects.TaskStatus.TODO)
        self._task_repo.create_task(new_task)
        return new_task