from exceptions import argument_exception, operation_exception
from datetime import datetime
from src.Logic.storage_observer import storage_observer
from src.models.event_type import event_type


# Класс для хранения настроек
class settings:
    __first_name = ""
    __first_start = True

    # Переменные для настроек
    __block_period = datetime(1, 1, 1)
    __INN = ""
    __account = ""
    __correspond_account = ""
    __BIK = ""
    __name = ""
    __property_type = ""
    __report_type = ""

    # Форматы отчетов
    __Report_format = {"CSV": "", "Markdown": "", "Json": ""}

    @property
    def Report_format(self):
        return self.__Report_format

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        # Устанавливаем полное имя
        if not isinstance(value, str):
            raise argument_exception("Некорректный аргумент!")

        self.__first_name = value.strip()

    @property
    def report_type(self):
        return self.__report_type

    @report_type.setter
    def report_type(self, value: str):
        # Устанавливаем тип отчета
        if not isinstance(value, str):
            raise argument_exception("Некорректный аргумент!")

        self.__report_type = value.strip()

    # Методы для установки и получения свойств

    # ...

    @block_period.setter
    def block_period(self, value: str):
        # Установка периода блокировки
        if not isinstance(value, str):
            raise argument_exception("Некорректный аргумент")

        # Проверка формата даты
        try:
            value = value.split(' ')[0]

            legacy = self.__block_period

            self.__block_period = datetime.strptime(value, "%Y-%m-%d")

            if legacy != self.__block_period:
                storage_observer.raise_event(event_type.changed_block_period())

        except Exception as ex:
            raise operation_exception(f'Не удалось сконвертировать дату: {ex}')

    # Метод для установки строки в виде даты (block_period)
    # while True:
    # ...