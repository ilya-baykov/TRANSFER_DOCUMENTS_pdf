from logging import getLogger
from typing import List, NamedTuple
from abc import ABC, abstractmethod
from utilities.row_info import RowDataFrame

loger = getLogger()


class ValidatorStatus(NamedTuple):
    status: bool
    error_message: str | None


class AccountValidator(ABC):
    """Абстрактный класс для проверки Лицевого счёта"""

    def __init__(self, account: str):
        """

        :param account: Лицевой счёт для проверки
        """
        self.account = account

    @abstractmethod
    def check(self) -> ValidatorStatus:
        pass


class AccountLengthValidator(AccountValidator):
    """Класс для проверки длины лицевого счёта"""

    def check(self):
        return ValidatorStatus(status=len(self.account) == 12,
                               error_message="Недопустимая длина номера лицевого счета")


class AccountDigitValidator(AccountValidator):
    """Класс для проверки отсутствия в лицевом счёте посторонних символов"""

    def check(self):
        return ValidatorStatus(status=self.account.replace(" ", "").isdigit(),
                               error_message="В номере лицевого счета есть нецифровые символы")


class BranchValidator:
    """Класс для проверки филиала, полученного по Лицевому счёту """

    def __init__(self, handbook_indexes):
        """

        :param handbook_indexes: Индексы строк таблицы справочника с информацией о филиале
        """
        self.handbook_indexes = handbook_indexes

    def check(self):
        return ValidatorStatus(status=bool(self.handbook_indexes),
                               error_message="Филиал не найден в справочнике филиалов")


class FillingRowValidator:
    """Класс для проверки заполнения полей строки"""

    def __init__(self, row: RowDataFrame):
        self.row = row
        self.filled_fields = self.__filling_fields()

    def __filling_fields(self) -> dict[str, str]:
        filled_fields = {}  # Заполненные поля строки таблицы
        for column, value in self.row:
            if value in ("", None):  # Проверка на отсутствие данных в строке
                loger.error(f"значение в строке {column} отсутствует: (value)='{value}'")
            else:
                filled_fields.setdefault(column, value)
        return filled_fields

    def check(self) -> bool:
        """Проверяет все ли поля строки таблицы заполнены"""
        return len(self.row) == len(self.filled_fields)


class ErrorCollector:
    """Класс - сборщик ошибок в таблице pdf-файла"""

    def __init__(self, *validators):
        """
        :param validators: Список объектов - валидаторов для сбора ошибок
        """
        self._validators = validators
        self._errors: List[str] = self.__collect_errors()

    def __collect_errors(self):
        """Формирует список сообщений об ошибках"""
        _error_messages = []
        for validator in self._validators:
            check_result: ValidatorStatus = validator.check()
            if not check_result.status:
                _error_messages.append(check_result.error_message)
        return _error_messages

    def get_errors(self) -> List[str]:
        return self._errors
