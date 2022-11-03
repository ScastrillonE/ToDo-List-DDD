from pydantic.dataclasses import dataclass
import uuid

UUID = uuid.uuid4()

@dataclass
class ValueObject:
    """
    Base class for value objects
    """
