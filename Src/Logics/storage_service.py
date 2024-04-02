from Src.Logics.convert_factory import convert_factory
from Src.Logics.process_factory import process_factory
from Src.Logics.storage_prototype import storage_prototype
from Src.exceptions import argument_exception, exception_proxy, operation_exception
from datetime import datetime
import json
from Src.Models.receipe_model import receipe_model
from Src.Models.storage_model import storage_model
class storage_service:
    __data = []
    
    def __init__(self, data: list) -> None:
        if len(data) == 0:
            raise argument_exception("Некорректно переданы параметры!")
        
        self.__data = data
        
    def __processing(self, data: list) -> list:
        """
            Сформировать обороты
        Args:
            data (list): _description_

        Returns:
            list: _description_
        """
        if len(data) == 0:
            raise argument_exception("Некорректно переданы параметры!")
        
        # Подобрать процессинг    
        key_turn = process_factory.turn_key()
        processing = process_factory().create( key_turn  )
    
        # Обороты
        turns =  processing().process( data )
        return turns
            
        
    def create_turns(self, start_period: datetime, stop_period:datetime ) -> dict:
        """
            Получить обороты за период
        Args:
            start_period (datetime): _description_
            stop_period (datetime): _description_

        Returns:
            dict: _description_
        """
        exception_proxy.validate(start_period, datetime)
        exception_proxy.validate(stop_period, datetime)
        
        if start_period > stop_period:
            raise argument_exception("Некорректно переданы параметры!")
        
        # Фильтруем      
        prototype = storage_prototype(  self.__data )  
<<<<<<< Updated upstream
        filter = prototype.filter( start_period, stop_period)
            
        # Подобрать процессинг    
        key_turn = process_factory.turn_key()
        processing = process_factory().create( key_turn  )
    
        # Обороты
        turns =  processing().process( filter.data )
        return turns
    

    def create_turns_by_nomen(self, start_period: datetime, stop_period:datetime, nomen_id: str) -> dict:
=======
        filter = prototype.filter_by_period( start_period, stop_period)
        
        return self.__processing( filter. data )
            
        
    def create_turns_by_nomenclature(self, start_period: datetime, stop_period: datetime, nomenclature: nomenclature_model) -> list:
>>>>>>> Stashed changes
        """
            Получить обороты за период по номенклатуре
        Args:
            start_period (datetime): _description_
            stop_period (datetime): _description_

        Returns:
            dict: _description_
        """
        exception_proxy.validate(start_period, datetime)
        exception_proxy.validate(stop_period, datetime)
        
        if start_period > stop_period:
            raise argument_exception("Некорректно переданы параметры!")
        
        # Фильтруем      
        prototype = storage_prototype(  self.__data )  
        filter = prototype.filter( start_period, stop_period)
        filter = filter.filter_by_nomenclature(nomen_id)
            
<<<<<<< Updated upstream
        # Подобрать процессинг    
        key_turn = process_factory.turn_key()
        processing = process_factory().create( key_turn  )
    
        # Обороты
        turns =  processing().process( filter.data )
        return turns

    def create_transactions(self, receipt: receipe_model, storage: storage_model):


        prototype = storage_prototype(  self.__data )  
        filter = prototype.filter_by_receipt(receipt)
        filter = filter.filter_by_storage(storage)
        if len(self.__data) != len(filter.data):
            raise operation_exception("Невозможность списания! Элемент отсутствует в списке номенклатуры")
        
        data = receipt.consist.values()

        # Подобрать процессинг    
        transaction_key = process_factory.transaction_key()
        processing = process_factory().create( transaction_key )
=======
        return self.__processing( filter. data )    
>>>>>>> Stashed changes
    
        # Транзакции
        transactions =  processing().process( data )
        return transactions

<<<<<<< Updated upstream

=======
        Returns:
            list: Обороты
        """
        exception_proxy.validate(nomenclature, nomenclature_model)
        prototype = storage_prototype(  self.__data )  
        filter = prototype.filter_by_nomenclature( nomenclature )
        if not filter.is_empty:
            raise operation_exception(f"Невозможно сформировать обороты по указанным данных: {filter.error}")
         
        return self.__processing( filter. data )   
    
    def create_turns_by_receipt(self, receipt: receipe_model) -> list:
        """
            Сформировать обороты по указанному рецепту
        Args:
            receipt (receipe_model): _description_

        Returns:
            list: _description_
        """
        exception_proxy.validate(receipt, receipe_model)
        
        if len(receipt.consist) == 0:
            raise operation_exception("Переданный рецепт некорректный. Не содержит в себе список номенклатуры!")
        
        # Отфильтровать по рецепту
        transactions = []
        filter =  storage_prototype(  self.__data )
        for item in receipt.rows():
            filter =  filter.filter_by_nomenclature( item.nomenclature )
            if filter.is_empty:
                for transaction in filter.data:
                    transactions.append( transaction )
                    
            filter.data = self.__data        
            
        return self.__processing( transactions )     
            
    
    def build_debits_by_receipt(self, receipt: receipe_model) -> list:
        """
            Сформировать проводки списания по рецепту
        Args:
            receipt (receipe_model): _description_

        Returns:
            list: _description_
        """
        exception_proxy.validate(receipt, receipe_model)
        
        if len(receipt.consist) == 0:
            raise operation_exception("Переданный рецепт некорректный. Не содержит в себе список номенклатуры!")
        
        turns = self.create_turns_by_receipt(receipt)
        if len(turns) <= 0:
            raise operation_exception("По указанному рецепту не найдеты обороты!")
        
        if len(receipt.rows()) > len(turns):
            raise operation_exception("Невозможно сформировать список транзакций для списания т.к. нет достаточно остатков!")
        
        # Формируем список проводок на списание
        processing = process_factory().create( process_factory.debit_key() )
        transactions = processing().process( receipt.rows() )
        key = storage.storage_transaction_key()
        
        data = storage().data[ key ]
        for transaction in transactions:
            data.append ( transaction )
    
    # Набор основных методов        
    
    def data(self) -> list:
        """
            Получить отфильтрованные данные
        Returns:
            list: _description_
        """
        return self.__data    
        
>>>>>>> Stashed changes
    @staticmethod        
    def create_response( data: list, app):
        """"
            Сформировать данные для сервера
        """
        if app is None:
            raise argument_exception("Некорректно переданы параметры!")

        # Преоброзование
        data = convert_factory().serialize( data )
        json_text = json.dumps( data, sort_keys = True, indent = 4,  ensure_ascii = False)  
   
        # Подготовить ответ    
        result = app.response_class(
            response = f"{json_text}",
            status = 200,
            mimetype = "application/json; charset=utf-8"
        )
        
        return result