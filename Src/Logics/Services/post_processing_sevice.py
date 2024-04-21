from pathlib import Path
from datetime import datetime
import os
import json
import uuid
import sys

sys.path.append(os.path.join(Path(__file__).parent, 'src'))

# Импортируем необходимые модули
from error_proxy import error_proxy
from pathlib import Path
from storage.storage import storage
from settings import settings
from Logic.storage_prototype import storage_prototype
from src.Logic.Reporting.Json_convert.reference_conventor import reference_conventor
from exceptions import argument_exception
from src.Logic.storage_observer import storage_observer
from src.Logic.process_factory import process_factory
from src.models.event_type import event_type

# Для работы с референсами
from src.storage.storage_turn_model import storage_turn_model
from models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.nomenclature_group_model import nomenclature_group_model
from models.recipe_model import recipe_model
from src.storage.storage_factory import storage_factory
from storage.storage_journal_row import storage_journal_row
from src.storage.storage_journal_transaction import storage_journal_transaction
from src.Logic.services.abstract_service import abstract_service


# Класс для работы с хранилищем
class storage_service(abstract_service):
    __data = []
    __options = None
    __blocked = []

    # Конструктор
    def __init__(self, data: list):
        if len(data) == 0:
            raise argument_exception("Wrong argument")

        self.__data = data
        storage_observer.observers.append(self)

    # Свойство опций
    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value: settings):
        if not isinstance(value, settings):
            raise argument_exception("неверный аргумент")
        self.__options = value

    # Метод для объединения оборотов
    @staticmethod
    def _collide_turns(base_turns: list, added_turns: list):
        if len(added_turns) == 0:
            return base_turns
        for index, cur_base_turn in enumerate(base_turns):
            for added_index, cur_added_turn in enumerate(added_turns):
                if cur_base_turn.nomenclature == cur_added_turn.nomenclature and cur_base_turn.storage_id == cur_added_turn.storage_id:
                    base_turns[index].amount += cur_added_turn.amount
                    added_turns.pop(added_index)
                    break

        for cur_added_turn in added_turns:
            base_turns.append(cur_added_turn)
        return base_turns

    # Метод для получения оборотов за период по номенклатуре
    def create_turns_by_nomenclature(self, start_date: datetime, finish_date: datetime, id: uuid.UUID) -> dict:
        # Реализация метода
        pass

    # Метод для получения оборотов за период
    def create_turns(self, start_date: datetime, finish_date: datetime) -> dict:
        # Реализация метода
        pass

    # Метод для получения оборотов по номенклатуре
    def create_id_turns(self, id: uuid.UUID) -> dict:
        # Реализация метода
        pass

    # Метод для создания транзакций по рецепту
    def create_recipe_transactions(self, recipe: recipe_model) -> dict:
        # Реализация метода
        pass

    # Метод для рейтинга номенклатуры по складам и айди
    def create_id_turns_storage(self, nomenclature_id: uuid.UUID, storage_id: str) -> dict:
        # Реализация метода
        pass

    # Метод для получения оборотов до периода блокировки
    def create_blocked_turns(self) -> dict:
        # Реализация метода
        pass

    # Обработчик события
    def handle_event(self, handle_type: str):
        super().handle_event(handle_type)

        if handle_type == event_type.changed_block_period():
            self.create_blocked_turns()

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