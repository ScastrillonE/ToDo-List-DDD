from typing import Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from domain.entities import Task
from domain.repository import TaskRepository

from .dtos import TaskDTO

class TaskRepositorySqlalchemy(TaskRepository):
    def __init__(self,session:Session):
        self.session : Session = session

    def find_by_id(self, id: str) -> Optional[Task]:
        try:
            task_dto = self.session.query(TaskDTO).filter_by(task_id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return task_dto.to_entity() 
    
    def create(self, task: Task):
        task_dto = TaskDTO.from_entity(task)
        try:
            self.session.add(task_dto)
        except:
            raise
        
    def update(self, task: Task):
        task_dto = TaskDTO.from_entity(task)
        try:
            _task = self.session.query(TaskDTO).filter_by(task_id=task_dto.task_id).one()
            _task.name = task_dto.name
            _task.user_id = task_dto.user_id
            _task.name = task_dto.name
            _task.status = task_dto.status
        except:
            raise