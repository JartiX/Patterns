import unittest
from Src.Models.group_model import group_model
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.reference import reference
from Src.Models.receipe_model import receipe_model
from Src.Models.receipe_row_model import receipe_row_model
from Src.Models.storage_model import storage_model
from Src.Models.storage_transaction_model import storage_transaction_model
from Src.Models.storage_type_model import storage_type_model

from Src.Logics.start_factory import start_factory
class transactions_test(unittest.TestCase):

    def test_create_transactions(self):
        start = start_factory.create_transactions()
        print(start[0].storage.address)
        assert len(start) > 0