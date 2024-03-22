from Src.reference import reference
from Src.exceptions import exception_proxy


class storage_turn_model(reference):
    __storage: reference = None
    __size: int = None
    __nomenclature: reference = None
    __unit: reference = None

    @classmethod
    def create(cls, storage, size, nomenclature, unit, name=' '):
        obj = cls(name)
        if exception_proxy.validate(storage, reference):
            obj.__storage = storage
        if exception_proxy.validate(size, int):
            obj.__size = size
        if exception_proxy.validate(nomenclature, reference):
            obj.__nomenclature = nomenclature
        if exception_proxy.validate(unit, reference):
            obj.__unit = unit
        return obj
    
    @property
    def storage(self):
        return self.__storage
    @property
    def size(self):
        return self.__size
    @property
    def nomenclature(self):
        return self.__nomenclature
    @property
    def unit(self):
        return self.__unit