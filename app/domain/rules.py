from basework.domain.rules import BusinessRule
import value_objects

class TaskNotChangeStatus(BusinessRule):
    __message = "No se puede regresar a un estado anterior "

    task_status : TaskStatus

    def is_broken(self)-> bool:
        return task_status == value_objects.TaskStatus.DONE