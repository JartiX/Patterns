from Src.reference import reference
from Src.exceptions import exception_proxy
from datetime import datetime

class storage_transaction_model(reference):
    __nomenclature: reference = None
    __unit: reference = None
    __type: reference = None
    __storage: reference = None
    __size: int = None
    __period: datetime = None
    __name: str = None

    @classmethod
    def create(cls, nomenclature, unit, size, type, storage, period):
        obj = cls(' ')
        if exception_proxy.validate(nomenclature, reference):
            obj.__nomenclature = nomenclature
        if exception_proxy.validate(unit, reference):
            obj.__unit = unit
        if exception_proxy.validate(storage, reference):
            obj.__storage = storage
        if exception_proxy.validate(size, int) and size > 0:
            obj.__size = size
        if exception_proxy.validate(type, reference):
            obj.__type = type
        if exception_proxy.validate(period, datetime):
            obj.__period = period
        return obj

    @property
    def nomenclature(self):
        return self.__nomenclature
    @property
    def unit(self):
        return self.__unit
    @property
    def size(self):
        return self.__size
    @property
    def type(self):
        return self.__type
    @property
    def storage(self):
        return self.__storage
    @property
    def period(self):
        return self.__period
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value