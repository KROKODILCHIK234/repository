from pathlib import Path
import os
import sys

sys.path.append(os.path.join(Path(__file__).parent.parent, 'src'))

from settings_manager import settings_manager
from datetime import datetime
from storage.storage import storage
from Logic.start_factory import start_factory
from src.Logic.services.storage_sevice import storage_service
from src.Logic.storage_observer import storage_observer
from src.models.event_type import event_type
from error_proxy import error_proxy
from exceptions import argument_exception, operation_exception
from src.Logic.services.nomenclature_service import nomenclature_service
import unittest


class test_sevice(unittest.TestCase):

    # проверка работы получения оборота
    def test_check_get_block_turns(self):
        # Подготовка
        unit = settings_manager()
        address = os.path.join(Path(__file__).parent.parent, 'Jsons')
        unit.open('Tester.json', address)
        factory = start_factory(unit.settings)
        # при factory create автоматически сохраняет
        factory.create()

        key = storage.journal_key()
        sevice = storage_service(factory.storage.data[key])
        sevice.options = unit.settings

        # действие
        res = sevice.create_blocked_turns()

        # проверка
        assert res is not None
        assert len(res) > 0
        assert res[0].storage_id == factory.storage.data[storage.b_turn_key()][0].storage_id

    def test_check_date_turns(self):
        # Подготовка
        unit = settings_manager()
        address = os.path.join(Path(__file__).parent.parent, 'Jsons')
        unit.open('Tester.json', address)
        unit.settings.block_period = "2024-1-1"
        factory = start_factory(unit.settings)
        # при factory create автоматически сохраняет
        factory.create()

        key = storage.journal_key()
        sevice = storage_service(factory.storage.data[key])
        sevice.options = unit.settings

        # действие
        sevice.create_blocked_turns()
        res = sevice.create_turns(datetime(2022, 1, 1), datetime(2024, 1, 2)

        # проверка
        print(res)
        assert res is not None
        assert len(res) > 0

    def test_check_date_turns_nom(self):
        # Подготовка
        unit = settings_manager()
        address = os.path.join(Path(__file__).parent.parent, 'Jsons')
        unit.open('Tester.json', address)
        unit.settings.block_period = "2024-1-1"
        factory = start_factory(unit.settings)
        # при factory create автоматически сохраняет
        factory.create()

        key = storage.journal_key()
        sevice = storage_service(factory.storage.data[key])
        sevice.options = unit.settings

        # действие
        sevice.create_blocked_turns()
        res = sevice.create_turns_by_nomenclature(datetime(2022, 1, 1), datetime(2024, 1, 2),
                                                  factory.storage.data[storage.nomenclature_key()][4].id)

        # проверка
        print(res)
        assert res is not None
        assert len(res) > 0

    def test_check_observer_blocked_period(self):
        # Подготовка
        unit = settings_manager()
        address = os.path.join(Path(__file__).parent.parent, 'Jsons')
        unit.open('Tester.json', address)
        unit.settings.block_period = "2024-1-1"
        factory = start_factory(unit.settings)
        factory.create()
        key = storage.journal_key()
        transactions_data = factory.storage.data[key]
        service = storage_service(transactions_data)

        # Действие
        try:
            storage_observer.raise_event(event_type.changed_block_period())
            assert True
        except Exception as ex:
            print(f"{ex}")

    def test_check_delete_nom_observer(self):
        # Подготовка
        unit = settings_manager()
        address = os.path.join(Path(__file__).parent.parent, 'Jsons')
        unit.open('Tester.json', address)
        unit.settings.block_period = "2024-1-1"
        factory = start_factory(unit.settings)
        # при factory create автоматически сохраняет
        factory.create()

        key = storage.nomenclature_key()
        sevice = nomenclature_service(factory.storage.data[key])

        controll_rec = list(factory.storage.data[storage.reciepe_key()][0].ingridient_proportions.keys())
        controll_journal = factory.storage.data[storage.journal_key()]
        controll_blocked = factory.storage.data[storage.b_turn_key()]

        # действие
        print(factory.storage.data[key][0].name, factory.storage.data[key][0].id)
        factory.storage.data[key], res = sevice.delete_nom(str(factory.storage.data[key][0].id))

        # проверка
        print(res)
        print(controll_rec, list(factory.storage.data[storage.reciepe_key()][0].ingridient_proportions.keys()))

        assert controll_rec != list(factory.storage.data[storage.reciepe_key()][0].ingridient_proportions.keys())
        assert controll_journal != factory.storage.data[storage.journal_key()]
        assert controll_blocked != factory.storage.data[storage.b_turn_key()]