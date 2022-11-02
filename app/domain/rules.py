from basework.domain.rules import BusinessRule
from .entities import TaskStatus

class TaskNotModifiable(BusinessRule):
    __message = "No se puede modificar una tarea con estado 'done' "

    task_status : TaskStatus

    def is_broken(self)-> bool:
        return task_status == TaskStatus.done