from Logic.Services.abstract_service import abstract_sevice
from Storage.storage_journal_row import storage_journal_row
from Models.nomenclature_group_model import nomenclature_group_model
from Models.range_model import range_model
from Models.nomenclature_model import nomenclature_model
from Storage.storage_turn_model import storage_turn_model
from exceptions import argument_exception
from Logic.Reporting.Json_convert.reference_conventor import reference_conventor
from error_proxy import error_proxy
from pathlib import Path
import os
import json
import uuid
import sys
from Logic.storage_observer import storage_observer
from Models.event_type import event_type
from Storage import storage
from Logic.Services.post_processing_service import post_processing_service
sys.path.append(os.path.join(Path(__file__).parent, 'Src'))


class nomenclature_service(abstract_sevice):
    __data = []

    def __init__(self, data: list):
        if len(data) == 0:
            raise argument_exception("Wrong argument")
        self.__data = data

    def add_nom(self, nom: nomenclature_model):
        self.__data.append(nom)
        return self.__data

    def change_nome(self, nom: nomenclature_model):
        for index, cur_nom in enumerate(self.__data):
            if cur_nom.id == nom.id:
                self.__data[index] = nom
                break
        return self.__data

    def get_nom(self, id: uuid.UUID):
        id = uuid.UUID(id)
        for cur_nom in self.__data:
            if id == cur_nom.id:
                reference = reference_conventor(nomenclature_model,
                                                error_proxy,
                                                nomenclature_group_model,
                                                range_model,
                                                storage_journal_row,
                                                storage_turn_model)
                return cur_nom

    def delete_nom(self, id: str):
        id = uuid.UUID(id)
        res = False

        obs = post_processing_service(
            storage().data[storage.nomenclature_key()])
        obs.nomenclature_id = id

        for index, cur_nom in enumerate(self.__data):
            if cur_nom.id == id:
                self.__data.pop(index)
                res = True
                storage_observer.raise_event(event_type.deleted_nomenclature())
                break
        return self.__data, res

    @staticmethod
    def create_response(data: dict, app):

        if app is None:
            raise argument_exception()
        json_text = json.dumps(data)

        result = app.response_class(
            response=f"{json_text}",
            status=200,
            mimetype="application/json; charset=utf-8"
        )
        return result
