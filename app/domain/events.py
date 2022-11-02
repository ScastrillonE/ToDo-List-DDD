from basework.domain.events import DomainEvent

class TaskChangeAttrEvent(DomainEvent):
    task_id : str