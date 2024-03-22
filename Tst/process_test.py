from Src.Storage import storage
from Src.Logics.process_factory import process_factory, process_storage_turn
from Src.settings_manager import settings_manager
from Src.Logics.start_factory import start_factory
import unittest


class process_test(unittest.TestCase):

    def test_process_factory(self):
        # подготовка
        manager = settings_manager()
        start = start_factory(manager.settings)
        start.create()
        process = process_factory()
        #действие
        turns = process.create_turns(start.storage.process_turn_key())
        turns.calculate(start.storage.data[start.storage.transaction_key()])
        
        # проверка
        assert process is not None