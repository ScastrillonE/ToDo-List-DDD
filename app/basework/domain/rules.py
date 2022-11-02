import pydantic

class BusinessRule(pydantic.BaseModel):
    """ This is a base class for implementing domain rules"""

    __message : str = "rule broken "

    def get_message(self) -> str:
        return self.__message
    
    def is_broken(self) -> bool:
        pass
    
    def __str__(self):
        return f"{self.__class__.__name__} {super().__str__()}"