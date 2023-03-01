from typing import List

from domain.entities import Task
from domain.repositories import TaskRepository
from infrastructure.database import Database


class SqliteTaskRepository(TaskRepository):
    def __init__(self, database: Database):
        self._database = database

    def get_all(self) -> List[Task]:
        cursor = self._database.execute("SELECT * FROM tasks")
        return [Task(**row) for row in cursor.fetchall()]

    def get_by_id(self, task_id: int) -> Task:
        cursor = self._database.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return Task(**row)

    def add(self, task: Task):
        cursor = self._database.execute(
            "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
            (task.title, task.description, task.status),
        )
        task.id = cursor.lastrowid

    def update(self, task: Task):
        self._database.execute(
            "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",
            (task.title, task.description, task.status, task.id),
        )

    def delete(self, task_id: int):
        self._database.execute("DELETE FROM tasks WHERE id = ?", (task_id,))