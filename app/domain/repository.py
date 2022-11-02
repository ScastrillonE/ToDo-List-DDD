import abc
import typing
import entities 

class TaskRepository(abc.ABC):
    
    @abc.abstractmethod
    def find_by_id(self,task_id : str):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self,task : Task) -> typing.Optional[Task]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self,task : Task) -> typing.Optional[Task]:
        raise NotImplementedError