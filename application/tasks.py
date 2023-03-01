from typing import List

from application.services import TaskService
from domain.entities import Task
from infrastructure.database import Database
from infrastructure.repositories import SqliteTaskRepository


def create_task_service() -> TaskService:
    database = Database()
    task_repository = SqliteTaskRepository(database)
    return TaskService(task_repository)


def list_tasks(task_service: TaskService):
    tasks = task_service.get_all_tasks()
    for task in tasks:
        print(f"{task.id}: {task.title} ({task.status})")


def create_task(task_service: TaskService, title: str, description: str):
    task = task_service.create_task(title, description, status="pending")
    print(f"Tarea creada: {task.id}: {task.title} ({task.status})")


def update_task(task_service: TaskService, task_id: int, title: str, description: str, status: str):
    task = task_service.update_task(task_id, title, description, status)
    print(f"Tarea actualizada: {task.id}: {task.title} ({task.status})")


def delete_task(task_service: TaskService, task_id: int):
    task_service.delete_task(task_id)
    print(f"Tarea eliminada: {task_id}")