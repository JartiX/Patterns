from Src.reference import reference
from Src.Storage.storage import storage
from Src.Models.storage_turn_model import storage_turn_model
class process_storage_turn():
    @staticmethod
    def calculate(transactions: reference):
        result = {}
        turns = []
        for transaction in transactions:
            key = (transaction.nomenclature, transaction.storage, transaction.unit)
            size = transaction.size * transaction.type.type
            if key in result.keys():
                result[key] += size
            else:
                result[key] = size
        for k, v in result.items():
            turn = storage_turn_model.create(k[1], v, key[0], k[2])
            turns.append(turn)
        return turns
        

class process_factory:
    __maps = {}

    def __init__(self) -> None:
       self.__build_structure()

    def __build_structure(self):
        pass
    
    def create(self, process_key:str) -> processing:
        """
            Подобрать нужный процессинг
        Args:
            process_key (str): Ключ
            data (list[storage_row_model]): Исходные данные
        Returns:
            processing: нужный процессинг
        """
        exception_proxy.validate(process_key , str)
        if process_key not in self.__maps.keys():
            raise argument_exception(f"Указанный процесс {process_key} не реализован!")
        
        current_processing = self.__maps[process_key]
        if current_processing is None:
            raise operation_exception("Некорректно сконфигурирована текущая фабрика!")
      
        return current_processing
    
    # Статические методы
        
    @staticmethod
    def turn_key() -> str:
        """
            Сформировать обороты
        Returns:
            str: _description_
        """
        return "turns" 
  
    
      
    # Код взят: https://github.com/UpTechCompany/GitExample/blob/6665bc70c4933da12f07c0a0d7a4fc638c157c40/storage/storage.py#L30
    
    @staticmethod
    def process_keys(cls):
        """
            Получить список ключей
        Returns:
            _type_: _description_
        """
        keys = []
        methods = [getattr(cls, method) for method in dir(cls) if callable(getattr(cls, method))]
        for method in methods:
            if method.__name__.endswith("_key") and callable(method):
                keys.append(method())
        return keys