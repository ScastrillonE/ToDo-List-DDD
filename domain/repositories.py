from abc import ABC, abstractmethod
from typing import List

from domain.entities import Task


class TaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task:
        pass

    @abstractmethod
    def add(self, task: Task):
        pass

    @abstractmethod
    def update(self, task: Task):
        pass

    @abstractmethod
    def delete(self, task_id: int):
        pass