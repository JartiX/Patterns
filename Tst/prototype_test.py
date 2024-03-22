from Src.Logics.storage_prototype import storage_prototype
from Src.Logics.start_factory import start_factory
import unittest
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from datetime import datetime
from Src.Logics.storage_service import storage_service
class prototype_test(unittest.TestCase):
    
    
    def test_check_prototype(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        key = storage.storage_transaction_key()
        data = start.storage.data[ key ]
        
        start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
        stop_date = datetime.strptime("2024-01-10", "%Y-%m-%d")
        prototype = storage_prototype( data)
        
        
        # Дейтсвие
        result = prototype.filter(   start_date, stop_date ) 
        
        # Проверка
        assert isinstance(result, storage_prototype)
        assert prototype.is_empty

    def test_check_filter_nomen_and_period(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        key = storage.storage_transaction_key()
        data = start.storage.data[ key ]
        start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
        stop_date = datetime.strptime("2024-01-10", "%Y-%m-%d")
        nomen_id = data[1].nomenclature.id
        prototype = storage_prototype( data)
        
        
        # Дейтсвие
        result = prototype.filter(start_date, stop_date)
        result = result.filter_by_nomenclature(nomen_id) 
        
        # Проверка
        print(result)
        assert isinstance(result, storage_prototype)
        assert prototype.is_empty

    def test_check_filter_by_receipt_and_storage(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        key = storage.storage_transaction_key()
        data = start.storage.data[ key ]
        receipt = start.storage.data[storage.receipt_key()][0]
        storage_ = data[0].storage

        prototype = storage_prototype( data)
        
        
        # Дейтсвие
        result = prototype.filter_by_receipt(receipt)
        result = prototype.filter_by_storage(storage_)
        
        # Проверка
        assert len(result.data) == len(data)
        assert isinstance(result, storage_prototype)
        assert prototype.is_empty