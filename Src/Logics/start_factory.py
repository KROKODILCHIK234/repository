from pathlib import Path
import os
import sys

sys.path.append(os.path.join(Path(__file__).parent.parent, 'models'))

from datetime import datetime
from models.range_model import range_model
from models.reciepe_model import reciepe_model
from storage.storage import storage
from exceptions import argument_exception
from models.nomenclature_model import nomenclature_model, nomenclature_group_model, range_model
from src.storage.storage_factory import storage_factory
from src.Logic.Reporting.Json_convert.reference_conventor import reference_conventor
from src.Logic.services.storage_service import storage_service
from src.storage.storage_turn_model import storage_turn_model
from storage.storage_model import storage_model
from settings import settings
from error_proxy import error_proxy
from src.Logic.services.post_processing_service import post_processing_service
import json

# Класс для инициализации начальных данных
class start_factory:
    __observer: post_processing_service = None
    __options: settings = None
    __storage: storage = None
    __storage_path = Path(__file__).parent.parent / 'storage' / 'saved_models'

    def __init__(self, options: settings, stor: storage = None):
        self.__options = options
        self.__storage = stor

    # Метод для сохранения данных в файл
    def __save(self):
        # Реализация метода
        pass

    # Метод для построения начальных данных
    def __build(self, nom: list):
        # Реализация метода
        pass

    # Метод для создания начальных данных
    def create(self):
        # Реализация метода
        pass

    # Метод для сохранения данных
    def save(self):
        # Реализация метода
        pass

    # Метод для загрузки моделей из файлов
    def __load_models(self):
        # Реализация метода
        pass

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        if not isinstance(value, settings):
            raise argument_exception("Неверный аргумент")

        self.__options = value