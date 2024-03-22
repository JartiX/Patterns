from Src.reference import reference
from Src.exceptions import exception_proxy


class storage_type_model(reference):
    # Поступление True / Списание False
    __type: str = None

    def __init__(self, type):
        super().__init__(" ")
        self.__type = type

    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, value):
        self.__type = value
    