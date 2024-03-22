from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.exceptions import exception_proxy, operation_exception
from Src.reference import reference
from Src.Logics.convertor import convertor

from datetime import datetime

from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipe_model import receipe_model
from Src.Models.storage_model import storage_model
from Src.Models.storage_transaction_model import storage_transaction_model
from Src.Models.storage_turn_model import storage_turn_model
from Src.Models.unit_model import unit_model
from Src.Models.storage_type_model import storage_type_model

#
# Конвертор reference в словарь
#
class reference_convertor(convertor):

    def deserialize(self, dictionary, model):
        super().deserialize(dictionary)

        factory = convert_factory()

        return factory.deserialize(dictionary, model)
    
    def serialize(self, field: str, object: reference) -> dict:
        """
            Подготовить словарь 
        Args:
            field (str): поле
            object (_type_): значение
        """
        super().serialize(field, object)
        
        factory = convert_factory()
        return factory.serialize(object)
    
#
# Фабрика для конвертация данных
#
class convert_factory:
    _maps = {}
    _dmaps = {}
    
    def __init__(self) -> None:
        # Связка с простыми типами
        self._maps[datetime] = datetime_convertor
        self._maps[int] = basic_convertor
        self._maps[str] = basic_convertor
        self._maps[bool] = basic_convertor
        
        # Связка для всех моделей
        for  inheritor in reference.__subclasses__():
            self._maps[inheritor] = reference_convertor
        
        self._dmaps['nomenclature'] = nomenclature_model
        self._dmaps['group'] = group_model
        self._dmaps['unit'] = unit_model
        self._dmaps['base_unit'] = unit_model
        self._dmaps['receipe'] = receipe_model
        self._dmaps['storage'] = storage_model
        self._dmaps['storage_turn'] = storage_turn_model
        self._dmaps['storage_transactios'] = storage_transaction_model
        self._dmaps['type'] = storage_type_model

    @staticmethod
    def create_dict(model):
        arr = {}
        if model == group_model:
            arr['name'] = ''
        elif model == unit_model:
            arr['name'] = ''
            arr['base_unit'] = ''
            arr['coefficient'] = ''
        elif model == nomenclature_model:
            arr['name'] = ''
            arr['group'] = ''
            arr['unit'] = ''
        elif model == receipe_model:
            arr['name'] = ''
            arr['comments'] = ''
            arr['items'] = ''
            arr['data'] = ''
        elif model == storage_model:
            arr['address'] = ''
        elif model == storage_turn_model:
            arr['storage'] = ''
            arr['size'] = ''
            arr['nomenclature'] = ''
            arr['name'] = ''
        elif model == storage_transaction_model:
            arr['nomenclature'] = ''
            arr['unit'] = ''
            arr['type'] = ''
            arr['size'] = ''
            arr['period'] = ''
            arr['storage'] = ''
        elif model == storage_type_model:
            arr['type'] = ''

        return arr
        
    def deserialize(self, dictionary: dict, model: reference):
        obj_fields = self.create_dict(model)
        another_obj_fields = {}

        for k, v in dictionary.items():
            if k in ('id', 'is_error', ''):
                continue
            elif v == "None":
                if k in obj_fields:
                    del obj_fields[k]
                continue
            
            if k == 'period':
                v = datetime.strptime(v, "%Y-%B-%d %H:%M")

            if k in obj_fields.keys():
                if isinstance(v, dict):
                    obj = self._dmaps[k]
                    v = self.deserialize(v, obj)
                obj_fields[k] = v
            else:
                if isinstance(v, dict):
                    obj = self._dmaps[k]
                    v = self.deserialize(v, obj)
                if v != "":
                    another_obj_fields[k] = v   

        kwargs = {k: v for k, v in obj_fields.items()}

        if model == receipe_model:
            model = model().create_receipts(**kwargs)
        elif model in  (storage_transaction_model, storage_turn_model):
            model = model(" ").create(**kwargs)
        else:
            if 'base_unit' in kwargs.keys():
                kwargs['base'] = kwargs['base_unit']
                del kwargs['base_unit']
            if 'coefficient' in kwargs.keys():
                kwargs['coeff'] = kwargs['coefficient']
                del kwargs['coefficient']
            model = model(**kwargs)
        if len(another_obj_fields) > 0:
            for k, v in another_obj_fields.items():
                setattr(model, k, v)
        
        return model

    
        
    def serialize(self, object) -> dict:
        """
            Подготовить словарь
        Args:
            object (_type_): произвольный тип

        Returns:
            dict: словарь
        """
        
        # Сконвертируем данные как список
        result = self.__convert_list("data", object)
        if result is not None:
            return result
        
        # Сконвертируем данные как значение
        result = {}
        fields = reference.create_fields(object)
        
        for field in fields:
            attribute = getattr(object.__class__, field)
            if isinstance(attribute, property):
                value = getattr(object, field)
                
                # Сконвертируем данные как список
                dictionary =  self.__convert_list(field, value)
                if dictionary is None:
                    # Сконвертируем данные как значение
                    dictionary = self.__convert_item(field, value)
                    
                if len(dictionary) == 1:
                    result[field] =  dictionary[field]
                else:
                    result[field] = dictionary       
          
        return result  
    
    def __convert_item(self, field: str,  source):
        """
            Сконвертировать элемент        
        Args:
            field (str): Наименование поля
            source (_type_): Значение

        Returns:
            dict: _description_
        """
        exception_proxy.validate(field, str)
        if source is None:
            return {field: "None"}
        
        if type(source) not in self._maps.keys():
            raise operation_exception(f"Не возможно подобрать конвертор для типа {type(source)}")

        # Определим конвертор
        convertor = self._maps[ type(source)]()
        dictionary = convertor.serialize( field, source )
        
        if not convertor.is_empty:
            raise operation_exception(f"Ошибка при конвертации данных {convertor.error}")

        
        return  dictionary
            
    def __convert_list(self, field: str,  source) -> list:
        """
            Сконвертировать список
        Args:
            source (_type_): _description_

        Returns:
            dict: _description_
        """
        exception_proxy.validate(field, str)
        
        # Сконвертировать список
        if isinstance(source, list):
            result = []
            for item in source:
                result.append( self.__convert_item( field,  item ))  
            
            return result 
        
        # Сконвертировать словарь
        if isinstance(source, dict):
            result = {}
            for key in source:
                object = source[key]
                value = self.__convert_item( key,  object )
                result[key] = value
                
            return result    
