from pathlib import Path
import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.join(Path(__file__).parent.parent,'src'))

from settings import settings
from settings_manager import settings_manager
from storage.storage import storage
from Logic.start_factory import start_factory
from src.Logic.services.storage_sevice import storage_service
from src.Logic.storage_observer import storage_observer
from src.models.event_type import event_type

import unittest

class test_settings(unittest.TestCase):

    def test_check_create_manager(self):
        # Подготовка
        manager1 = settings_manager()
        manager2 = settings_manager()

        # Действие

        # Проверки
        print(str(manager1.number))
        print(str(manager2.number))

        assert manager1.number == manager2.number

    # Проверка корректности заполнения поля first_name
    def test_check_first_name(self):
        # Подготовка
        item = settings()

        # Действие
        item.first_name = "a  "

        # Проверка
        assert item.first_name == "a"

    # Проверка INN
    def test_INN_check(self):
        item = settings()
        item.INN = "    000000123456          "
        assert item.INN == "000000123456"

    # Проверка account
    def test_account_check(self):
        item = settings()
        item.account = "       12345678901"
        assert item.account == "12345678901"

    # Проверка корреспондентского счета
    def test_cor_account_check(self):
        item = settings()
        item.correspond_account = "        12345678901                "
        assert item.correspond_account == "12345678901"

    # Проверка BIK
    def test_BIK_check(self):
        item = settings()
        item.BIK = "       123456789        "
        assert item.BIK == "123456789"

    # Проверка названия
    def test_name_check(self):
        item = settings()
        item.name = "abcx asd       "
        assert item.name == "abcx asd"

    # Проверка типа собственности
    def test_property_type_check(self):
        item = settings()
        item.property_type = "'000'   "
        assert item.property_type == "'000'"

    def test_block_period_check(self):
        # Подготовка
        item = settings()
        # Действие
        item.block_period = "2024-1-1"
        # Проверка
        print(datetime(2024, 4, 5), item.block_period)
        assert item.block_period == datetime(2024, 1, 1)

    # Проверка INN с пробелами
    def test_INN_check_spaces(self):
        item = settings()
        item.INN = "    000 00 0123 456          "
        assert item.INN == "000000123456"

    # Проверка account с пробелами
    def test_account_check_spaces(self):
        item = settings()
        item.account = "       1234 56   7 8 90 1"
        assert item.account == "12345678901"

    # Проверка корреспондентского счета с пробелами
    def test_cor_account_check_spaces(self):
        item = settings()
        item.correspond_account = "        12 34 56 78 901                "
        assert item.correspond_account == "12345678901"

    # Проверка BIK с пробелами
    def test_BIK_check_spaces(self):
        item = settings()
        item.BIK = "       1234 56 78 9        "
        assert item.BIK == "123456789"

    def test_check_manager_convert(self):
        # Подготовка
        manager = settings_manager()

        # Действия
        A = manager.open("settings.json")

        # Проверка
        assert A == True

    def test_check_open_settings(self):
        # Подготовка
        manager = settings_manager()

        # Действие
        result = manager.open()

        # Проверка
        print(manager.data)

        assert result == True

    # Загрузка настроек из другой папки и с другим названием
    def test_check_open_other_dir_settings(self):
        # Подготовка
        manager = settings_manager()
        # Адрес
        address = os.path.join(Path(__file__).parent.parent, 'Jsons')
        print(address)
        result = manager.open("Tester.json", address)
        assert result == True

    # Тест на сохранение (сохранение считается правильным, при прохождении остальных автотестов)
    def test_check_save_settings(self):
        # Подготовка
        manager = settings_manager()
        # Адрес
        address = os.path.join(Path(__file__).parent.parent, 'Jsons')
        result = manager.open("Tester.json", address)
        # Действие
        dic = manager.save_settings()
        # Проверка
        assert dic == True

    # Тест наблюдателя
    def test_check_observer_event(self):
        # Подготовка
        unit = settings_manager()
        address = os.path.join(Path(__file__).parent.parent, 'Jsons')
        unit.open('Tester.json', address)
        factory = start_factory(unit.settings)
        factory.create()
        key = storage.b_turn_key()
        transactions_data_control = factory.storage.data[key]

        # Действие
        unit.settings.block_period = "2024-5-5"
        transactions_data = factory.storage.data[key]

        # Проверка
        assert len(transactions_data_control) != len(transactions_data)