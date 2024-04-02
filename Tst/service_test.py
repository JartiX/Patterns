from Src.Logics.storage_prototype import storage_prototype
from Src.Logics.start_factory import start_factory
import unittest
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
<<<<<<< Updated upstream
=======
from Src.exceptions import operation_exception

>>>>>>> Stashed changes
from datetime import datetime
from Src.Logics.storage_service import storage_service

class service_test(unittest.TestCase):

    def test_storage_service(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        key = storage.storage_transaction_key()
        data = start.storage.data[ key ]

        start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
        stop_date = datetime.strptime("2024-01-10", "%Y-%m-%d")
        service = storage_service(data)

        # Действие
        filtered = service.create_turns(start_date, stop_date)

        # Проверка
        print(filtered)

        assert filtered is not None
        assert len(filtered) > 0
        assert isinstance(filtered, list)


    def test_service_filter(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        key = storage.storage_transaction_key()
        data = start.storage.data[ key ]
<<<<<<< Updated upstream
=======
        service = storage_service(data)
        start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
        stop_date = datetime.strptime("2024-01-30", "%Y-%m-%d")
>>>>>>> Stashed changes
        
        start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
        stop_date = datetime.strptime("2024-01-30", "%Y-%m-%d")
        nomen_id = data[0].nomenclature.id
        service = storage_service(data)
        
        
        # Дейтсвие
        result = service.create_turns_by_nomen(start_date, stop_date, nomen_id) 
        
        # Проверка
        print(result)
        assert len(result) > 0
<<<<<<< Updated upstream

    def test_service_transactions(self):
=======
        
    #
    # Проверить метод  build_debits_by_receipt. Ошибочный сценарий.
    #   
    def test_check_build_debits_by_receipt_fail(self):
>>>>>>> Stashed changes
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        key = storage.storage_transaction_key()
<<<<<<< Updated upstream
        data = start.storage.data[ key ]
        receipt = start.storage.data[storage.receipt_key()][0]
        service = storage_service(data)
        storage_ = data[0].storage
        
        # Дейтсвие
        result = service.create_transactions(receipt, storage_)
        
        # Проверка
        print(result)
        assert len(result) > 0
=======
        transactions_data = start.storage.data[ key ]
        service = storage_service(transactions_data)
        
        if len(transactions_data) == 0:
            raise operation_exception("Набор данных пуст!")
        
        key = storage.receipt_key()
        receipts_data = start.storage.data[ key ]
        
        if len(receipts_data) == 0:
            raise operation_exception("Набор данных пуст!")
        
        # -> Цезарь с курицей
        receipt = receipts_data[1]
        
        # Действие и проверка
        with self.assertRaises(operation_exception):
            service.build_debits_by_receipt( receipt )
            
            
    #
    # Проверить метод  build_debits_by_receipt. Корректный сценарий
    #   
    def test_check_build_debits_by_receipt_pass(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        key = storage.storage_transaction_key()
        transactions_data = start.storage.data[ key ]
        start_len_transaction = len(transactions_data)
        service = storage_service(transactions_data)
        
        if len(transactions_data) == 0:
            raise operation_exception("Набор данных пуст!")
        
        key = storage.receipt_key()
        receipts_data = start.storage.data[ key ]
        
        if len(receipts_data) == 0:
            raise operation_exception("Набор данных пуст!")
        
        # -> Вафли хрустящие в вафильнице
        receipt = receipts_data[0]
        
        # Действие и проверка
        service.build_debits_by_receipt( receipt ) 
        stop_len_transaction = len(start.storage.data[  storage.storage_transaction_key() ])
          
        # Проверка (транзакций должно быть больше)   
        assert start_len_transaction < stop_len_transaction   
        
            
        
            
            
        
        
>>>>>>> Stashed changes
