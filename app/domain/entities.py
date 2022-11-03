import dataclasses
from app.domain import value_objects
from app.basework.domain.entities import AggregateRoot
from app.basework.domain.events import DomainEvent


class Task(AggregateRoot):
    def __init__(self, task_id, user_id, name, status):
        assert isinstance(task_id, str)
        assert isinstance(user_id, int)
        assert isinstance(name, str)
        assert isinstance(status, value_objects.TaskStatus)
        self.task_id : str = task_id
        self.user_id : str = user_id
        self.name : str = name
        self.status : value_objects.TaskStatus = status


        def is_done(self):
            return self._status == value_objects.TaskStatus.DONE
        
        def is_todo(self):
            return self._status == value_objects.TaskStatus.TODO

        def mark_done(self):
            self._status = value_objects.TaskStatus.DONE

        def mark_todo(self):
            self._status = value_objects.TaskStatus.TODO