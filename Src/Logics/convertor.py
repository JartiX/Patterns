import abc
from Src.errors import error_proxy
from Src.exceptions import exception_proxy

# 
# Абстрактный класс для конвертации данных в json
#
class convertor(error_proxy):
    
    @abc.abstractmethod
    def serialize(self, field: str, object) -> dict:
        """
            Сконвертировать объект в словарь
        Args:
            source (_type_): Любой тип данных
        """
        exception_proxy.validate(field, str)
        self.clear()


    @abc.abstractmethod
    def deserialize(self, dictionary) -> dict:
        exception_proxy.validate(dictionary, dict)
        self.clear()
         
        
        
        
        
    
