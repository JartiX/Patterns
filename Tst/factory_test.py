from Src.Logics.start_factory import start_factory
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from Src.Logics.report_factory import report_factory
from Src.Logics.convert_factory import convert_factory
import unittest
from Src.Models.storage_transaction_model import storage_transaction_model
#
# Набор автотестов для проверки работы фабричного метода
# 
class factory_test(unittest.TestCase):

    # 
    # Проверить метод storage_keys в хранилище
    #
    def test_check_method_storage_keys(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory( manager.settings )
        start.create()
        
        # Действия
        result = start.storage.storage_keys( start.storage  )
        
        # Проверки
        assert result is not None
        assert len(result) > 0
     
    #
    # Проверка работы фабрики для построения отчетности
    #
    def test_check_report_factory_create(self):
        # Подготовка
        manager = settings_manager()
        start = start_factory( manager.settings )
        start.create()
        factory = report_factory()
        key = storage.unit_key()

        # Действие
        report = factory.create( 
                                manager.settings.report_mode, 
                                start.storage.data)
        
        # Проверки
        assert report is not None
        print ( report.create(key) )
 
    #
    # Проверка создания начальных рецептов
    #    
    def test_check_create_receipts(self):
        # Подготовка
        items = start_factory.create_receipts()
        
        # Действие
        
        # Проверки
        assert len(items) > 0     
        
    # 
    # Проверка создание начальной номенклатуры
    #    
    def test_check_create_nomenclatures(self):
        # Подготовка
        items = start_factory.create_nomenclatures()
        
        # действие
        
        # Прверки
        assert len(items) > 0 
        
        
    #
    # Проверка создание списка единиц измерения
    #    
    def test_check_create_units(self):
        # Подготовка
        items = start_factory.create_units()
        
        # Действие
        
        # Проверки
        assert len(items) > 0    
     
    #
    # Проверка создания списка групп
    # 
    def test_check_create_groups(self):
        # Подготовка
        items = start_factory.create_groups()
        
        # Действие
        
        # Проверки    
        assert len(items) > 0
        
        
    #      
    # Проверка работы класса start_factory. Метод create
    #
    def test_check_factory_create(self):
        # Подготовка
        manager = settings_manager()
        factory = start_factory( manager.settings )
        
        
        # Действие
        result = factory.create()
        
        
        # Проверка
        if manager.settings.is_first_start == True:
            assert result == True
            assert not factory.storage is None
            assert storage.nomenclature_key() in factory.storage.data
            assert storage.receipt_key() in factory.storage.data
            assert storage.group_key() in factory.storage.data
            assert storage.unit_key() in factory.storage.data
        else:
            assert result == False    


    def test_deserialize(self):
        fac = convert_factory()

        data = {
        "description": "",
        "id": "e884f48467574ff8b27e52a5a71385a8",
        "is_error": False,
        "name": " ",
        "nomenclature": {
            "description": "",
            "group": {
                "description": "",
                "id": "3244242696044347875a3063d854b2f4",
                "is_error": False,
                "name": "Ингредиенты"
            },
            "id": "e8cbbd8b6fd4417c9c24b7b2531c8a24",
            "is_error": False,
            "name": "Яйца",
            "unit": {
                "base_unit": {
                    "base_unit": "None",
                    "coefficient": 1,
                    "description": "",
                    "id": "80444714752849149b69dca38b6d1316",
                    "is_error": False,
                    "name": "штука"
                },
                "coefficient": 10,
                "description": "",
                "id": "5df8b0adff564ac7ab80209bb4ca5dda",
                "is_error": False,
                "name": "десяток"
            }
        },
        "period": "2024-January-03 00:00",
        "size": 3,
        "storage": {
            "address": "Lermontova, 126",
            "description": "",
            "id": "0a2dbcec7a5d441cb72ac4ae2d901244",
            "is_error": False,
            "name": "Lermontova, 126"
        },
        "type": {
            "description": "",
            "id": "d6141534ef1242a7ab6ba335b6907c61",
            "is_error": False,
            "name": "type",
            "type": True
        },
        "unit": {
            "base_unit": {
                "base_unit": "None",
                "coefficient": 1,
                "description": "",
                "id": "80444714752849149b69dca38b6d1316",
                "is_error": False,
                "name": "штука"
            },
            "coefficient": 10,
            "description": "",
            "id": "5df8b0adff564ac7ab80209bb4ca5dda",
            "is_error": False,
            "name": "десяток"
        }
        }
        obj = fac.deserialize(data, storage_transaction_model)
        print(type(obj))

        
                     
        
       
