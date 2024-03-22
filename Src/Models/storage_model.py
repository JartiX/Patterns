from Src.reference import reference
from Src.exceptions import exception_proxy

class storage_model(reference):
    __address: str = None

    def __init__(self, address):
        super().__init__(address)
        self.__address = address

    @property
    def address(self):
        return self.__address
    
    