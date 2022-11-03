import abc
import typing
from app.domain import entities

class TaskRepository(abc.ABC):
    
    @abc.abstractmethod
    def get_tasks_by_user_id(self,task_id : str):
        raise NotImplementedError

    @abc.abstractmethod
    def create_task(self,task : entities.Task) -> typing.Optional[entities.Task]:
        raise NotImplementedError
