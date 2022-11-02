from sqlalchemy import Column, Integer, String
from typing import Union
from domain.entities import TaskStatus,Task
from basework.infrastructure import database


class TaskDTO(database.Base):
    __tablename__ = "task"
    self.task_id : Union[str,Column] = Column(String,primary_key=True,autoincrement=False)
    self.user_id : Union[str,Column] = Column(String, nullable=False)
    self.name : Union[str,Column] = Column(String, nullable=False)
    self.status: Union[TaskStatus,Column] = Column(String, nullable=False)

    def to_entity(self)->Task:
        return Task(
            task_id = self.task_id,
            user_id = self.user_id,
            name = self.name,
            status = self.status,
        )

    @staticmethod
    def from_entity(self,task:Task)->TaskDTO:
        return TaskDTO(
            task_id = task.task_id,
            user_id = task.user_id,
            name = task.name,
            status = task.status
        )
