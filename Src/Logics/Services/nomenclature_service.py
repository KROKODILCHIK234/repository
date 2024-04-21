from pathlib import Path
from datetime import datetime
import os
import json
import uuid
import sys

# Добавляем путь к модулям в переменную sys.path
sys.path.append(os.path.join(Path(__file__).parent, 'src'))

# Импортируем необходимые модули
from error_proxy import error_proxy
from pathlib import Path
from storage.storage import storage
from Logic.storage_prototype import storage_prototype
from src.Logic.Reporting.Json_convert.reference_conventor import reference_conventor
from exceptions import argument_exception
from src.Logic.process_factory import process_factory
from src.Logic.storage_observer import storage_observer
from src.models.event_type import event_type

# Импортируем модели и сервисы
from src.storage.storage_turn_model import storage_turn_model
from models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.nomenclature_group_model import nomenclature_group_model
from models.reciepe_model import reciepe_model
from src.storage.storage_factory import storage_factory
from storage.storage_journal_row import storage_journal_row
from src.storage.storage_journal_transaction import storage_journal_transaction
from src.Logic.services.abstract_service import abstract_sevice
from src.Logic.services.post_processing_sevice import post_processing_service


# Класс для работы с номенклатурой
class nomenclature_service(abstract_sevice):

    # Конструктор класса
    def __init__(self, data: list):
        if len(data) == 0:
            raise argument_exception("Wrong argument")
        self.__data = data

    # Метод для добавления номенклатуры
    def add_nom(self, nom: nomenclature_model):
        self.__data.append(nom)
        return self.__data

    # Метод для изменения номенклатуры
    def change_nome(self, nom: nomenclature_model):
        for index, cur_nom in enumerate(self.__data):
            if cur_nom.id == nom.id:
                self.__data[index] = nom
                break
        return self.__data

    # Метод для получения номенклатуры по идентификатору
    def get_nom(self, id: uuid.UUID):
        id = uuid.UUID(id)
        for cur_nom in self.__data:
            if id == cur_nom.id:
                reference = reference_conventor(nomenclature_model, error_proxy, nomenclature_group_model, range_model,
                                                storage_journal_row, storage_turn_model)
                return cur_nom

    # Метод для удаления номенклатуры по идентификатору
    def delete_nom(self, id: str):
        id = uuid.UUID(id)
        res = False

        obs = post_processing_service(storage().data[storage.nomenclature_key()])
        obs.nomenclature_id = id

        for index, cur_nom in enumerate(self.__data):
            if cur_nom.id == id:
                self.__data.pop(index)
                res = True
                storage_observer.raise_event(event_type.deleted_nomenclature())
                break
        return self.__data, res

    # Статический метод для создания ответа
    @staticmethod
    def create_response(data: dict, app):
        if app is None:
            raise argument_exception()
        json_text = json.dumps(data)

        # Подготовить ответ
        result = app.response_class(
            response=f"{json_text}",
            status=200,
            mimetype="application/json; charset=utf-8"
        )
        return result