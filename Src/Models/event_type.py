from src.models.abstract_reference import abstract_reference


# Класс для определения типов событий
class event_type(abstract_reference):

    @staticmethod
    def changed_block_period() -> str:
        """
            Метод для получения строки-идентификатора события изменения даты блокировки.
        Returns:
            str: Идентификатор события изменения даты блокировки.
        """
        return "changed_block_period"

    @staticmethod
    def deleted_nomenclature() -> str:
        """
            Метод для получения строки-идентификатора события удаления номенклатуры.
        Returns:
            str: Идентификатор события удаления номенклатуры.
        """
        return "deleted_nomenclature"