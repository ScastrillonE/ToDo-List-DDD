import dataclasses
import enum
from basework.domain.entities import AggregateRoot
from basework.domain.events import DomainEvent

class TaskStatus(enum.Enum):
    todo = "todo"
    done = "done"


class Task(AggregateRoot):
    def __init__(self, task_id, user_id, name, status):
        assert isinstance(task_id, str)
        assert isinstance(user_id, int)
        assert isinstance(name, basestring)
        assert isinstance(status, TaskStatus)
        self.task_id : str = task_id
        self.user_id : str = user_id
        self.name : str = name
        self.status : TaskStatus = status

