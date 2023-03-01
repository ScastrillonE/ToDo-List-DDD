from typing import List

from application.exceptions import TaskNotFoundException
from domain.entities import Task
from domain.repositories import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self._repository = task_repository

    def get_all_tasks(self) -> List[Task]:
        return self._repository.get_all()

    def get_task_by_id(self, task_id: int) -> Task:
        task = self._repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        return task

    def create_task(self, title: str, description: str) -> Task:
        task = Task(title=title, description=description, status="pending")
        self._repository.add(task)
        return task

    def update_task(self, task_id: int, title: str, description: str, status: str) -> Task:
        task = self.get_task_by_id(task_id)
        task.title = title
        task.description = description
        task.status = status
        self._repository.update(task)
        return task

    def delete_task(self, task_id: int):
        task = self.get_task_by_id(task_id)
        self._repository.delete(task.id)